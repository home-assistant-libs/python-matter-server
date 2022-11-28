"""Client."""
from __future__ import annotations

import asyncio
from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from functools import partial
import json
import logging
from operator import itemgetter
import pprint
from types import TracebackType
from typing import Any, DefaultDict, Dict, List
import uuid
from enum import Enum
from aiohttp import ClientSession, ClientWebSocketResponse, WSMsgType, client_exceptions

from ..common.helpers.json import json_loads, json_dumps
from ..common.helpers.util import dataclass_from_dict, chip_clusters_version

from ..common.models.server_information import ServerInfo
from ..common.models.message import (
    CommandMessage,
    ErrorResultMessage,
    MessageType,
    ResultMessageBase,
    EventMessage,
    SuccessResultMessage,
    parse_message,
)
from .const import MIN_SCHEMA_VERSION
from .exceptions import (
    CannotConnect,
    ConnectionClosed,
    ConnectionFailed,
    FailedCommand,
    InvalidMessage,
    InvalidServerVersion,
    InvalidState,
    NotConnected,
)


# Message IDs
SET_API_SCHEMA_MESSAGE_ID = "api-schema-id"
GET_INITIAL_LOG_CONFIG_MESSAGE_ID = "get-initial-log-config"
START_LISTENING_MESSAGE_ID = "listen-id"

LISTEN_MESSAGE_IDS = (
    GET_INITIAL_LOG_CONFIG_MESSAGE_ID,
    SET_API_SCHEMA_MESSAGE_ID,
    START_LISTENING_MESSAGE_ID,
)


class MatterClient:
    """Manage a Matter server over Websockets."""

    def __init__(self, ws_server_url: str, aiohttp_session: ClientSession):
        """Initialize the Client class."""
        self.ws_server_url = ws_server_url
        self.logger = logging.getLogger(__package__)
        self.aiohttp_session = aiohttp_session
        # server info is retrieved on connect
        self.server_info: ServerInfo | None = None
        self._ws_client: ClientWebSocketResponse | None = None
        self._loop = asyncio.get_running_loop()
        self._result_futures: Dict[str, asyncio.Future] = {}

    @property
    def connected(self) -> bool:
        """Return if we're currently connected."""
        return self._ws_client is not None and not self._ws_client.closed

    async def async_send_command(
        self,
        command: str,
        args: dict[str, Any],
        require_schema: int | None = None,
    ) -> dict:
        """Send a command and get a response."""
        if require_schema is not None and require_schema > self.server_info.schema_version:
            raise InvalidServerVersion(
                "Command not available due to incompatible server version. Update the Matter "
                f"Server to a version that supports at least api schema {require_schema}."
            )

        message = CommandMessage(
            messageId=uuid.uuid4().hex,
            command=command,
            args=args,
        )
        future: asyncio.Future[dict] = self._loop.create_future()
        self._result_futures[message.messageId] = future
        await self._send_message(message)
        try:
            return await future
        finally:
            self._result_futures.pop(message.messageId)

    async def async_send_command_no_wait(
        self, command: str, args: dict[str, Any], require_schema: int | None = None
    ) -> None:
        """Send a command without waiting for the response."""
        if require_schema is not None and require_schema > self.server_info.schema_version:
            raise InvalidServerVersion(
                "Command not available due to incompatible server version. Update the Matter "
                f"Server to a version that supports at least api schema {require_schema}."
            )
        message = CommandMessage(
            messageId=uuid.uuid4().hex,
            command=command,
            args=args,
        )
        await self._send_message(message)

    async def connect(self) -> None:
        """Connect to the websocket server."""
        if self._ws_client is not None:
            raise InvalidState("Already connected")

        self.logger.debug("Trying to connect")
        try:
            self._ws_client = await self.aiohttp_session.ws_connect(
                self.ws_server_url,
                heartbeat=55,
                compress=15,
                max_msg_size=0,
            )
        except (
            client_exceptions.WSServerHandshakeError,
            client_exceptions.ClientError,
        ) as err:
            raise CannotConnect(err) from err

        # at connect, the server sends a single message with the server info
        msg = await self._receive_message_or_raise()
        self.server_info = info = dataclass_from_dict(ServerInfo, msg.result)

        # sdk version must match exactly
        if info.sdk_version != chip_clusters_version():
            await self._ws_client.close()
            raise InvalidServerVersion(
                f"Matter Server SDK version is incompatible: {info.sdk_version} "
                f"version on the client is {chip_clusters_version()} "
            )

        # basic check for server schema version compatibility
        if info.schema_version < MIN_SCHEMA_VERSION:
            # server version is too low, raise exception
            await self._ws_client.close()
            raise InvalidServerVersion(
                f"Matter Server schema version is incompatible: {info.schema_version} "
                f"a version is required that supports at least api schema {MIN_SCHEMA_VERSION} "
                " - update the Matter Server to a more recent version."
            )
        if self.server_info.schema_version > MIN_SCHEMA_VERSION:
            # server version is higher than expected, log only
            self.logger.warning(
                f"Matter Server detedted with schema version {info.schema_version} "
                f"which is higher than the preferred api schema {MIN_SCHEMA_VERSION} of this client"
                " - you may run into compatibility issues."
            )

        self.logger.info(
            "Connected to Matter Fabric %s (%s), Schema version %s, CHIP SDK Version %s",
            info.fabricId,
            info.compressedFabricId,
            info.schema_version,
            info.sdk_version
        )

    async def listen(self, driver_ready: asyncio.Event) -> None:
        """Start listening to the websocket (and receive initial state)."""
        if not self.connected:
            raise InvalidState("Not connected when start listening")

        try:
            self.logger.info("Matter client initialized.")
            driver_ready.set()

            while not self._ws_client.closed:
                msg = await self._receive_message_or_raise()
                self._handle_incoming_message(msg)
        except ConnectionClosed:
            pass
        finally:
            await self.disconnect()

    async def disconnect(self) -> None:
        """Disconnect the client."""
        self.logger.debug("Closing client connection")
        # cancel all command-tasks awaiting a result
        for future in self._result_futures.values():
            future.cancel()
        # close the client if is still connected
        if self._ws_client is not None and not self._ws_client.closed:
            await self._ws_client.close()

    async def _receive_message_or_raise(self) -> MessageType:
        """Receive (raw) message or raise."""
        assert self._ws_client
        ws_msg = await self._ws_client.receive()

        if ws_msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSED, WSMsgType.CLOSING):
            raise ConnectionClosed("Connection was closed.")

        if ws_msg.type == WSMsgType.ERROR:
            raise ConnectionFailed()

        if ws_msg.type != WSMsgType.TEXT:
            raise InvalidMessage(f"Received non-Text message: {ws_msg.type}")

        try:
            msg: MessageType = parse_message(json_loads(ws_msg.data))
        except TypeError as err:
            raise InvalidMessage(f"Received unsupported JSON: {err}") from err
        except ValueError as err:
            raise InvalidMessage("Received invalid JSON.") from err

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("Received message:\n%s\n", pprint.pformat(ws_msg))

        return msg

    def _handle_incoming_message(self, msg: MessageType) -> None:
        """
        Handle incoming message.

        Run all async tasks in a wrapper to log appropriately.
        """
        # handle result message
        if isinstance(msg, ResultMessageBase):

            future = self._result_futures.get(msg.messageId)

            if future is None:
                # no listener for this result
                return

            if isinstance(msg, SuccessResultMessage):
                msg: SuccessResultMessage = msg
                future.set_result(msg.result)
                return
            if isinstance(msg, ErrorResultMessage):
                msg: ErrorResultMessage = msg
                future.set_exception(FailedCommand(msg.messageId, msg.errorCode))
                return

        # handle EventMessage
        if isinstance(msg, EventMessage):
            self.logger.debug("Received event: %s", msg)
            return

        # Log anything we can't handle here
        self.logger.debug(
            "Received message with unknown type '%s': %s",
            type(msg),
            msg,
        )

    async def _send_message(self, message: CommandMessage) -> None:
        """
        Send a CommandMessage to the server.

        Raises NotConnected if client not connected.
        """
        if not self.connected:
            raise NotConnected

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("Publishing message:\n%s\n", pprint.pformat(message))

        assert self._ws_client
        assert isinstance(message, CommandMessage)

        await self._ws_client.send_json(message, dumps=json_dumps)

    async def __aenter__(self) -> "MatterClient":
        """Initialize and connect the Matter Websocket client."""
        await self.connect()
        return self

    async def __aexit__(
        self, exc_type: Exception, exc_value: str, traceback: TracebackType
    ) -> None:
        """Disconnect from the websocket."""
        await self.disconnect()

    def __repr__(self) -> str:
        """Return the representation."""
        prefix = "" if self.connected else "not "
        return f"{type(self).__name__}(ws_server_url={self.ws_server_url!r}, {prefix}connected)"