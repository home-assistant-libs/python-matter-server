"""Client."""
from __future__ import annotations

import asyncio
from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from enum import Enum
from functools import partial
import json
import logging
from operator import itemgetter
import pprint
from types import TracebackType
from typing import TYPE_CHECKING, Any, DefaultDict, Dict, List, Type
import uuid

from aiohttp import ClientSession, ClientWebSocketResponse, WSMsgType, client_exceptions

from ..common.helpers.json import json_dumps, json_loads
from ..common.helpers.util import (
    chip_clusters_version,
    dataclass_from_dict,
    parse_value,
)
from ..common.models.api_command import APICommand
from ..common.models.message import (
    CommandMessage,
    ErrorResultMessage,
    EventMessage,
    MessageType,
    ResultMessageBase,
    SuccessResultMessage,
    parse_message,
)
from ..common.models.node import MatterNode
from ..common.models.server_information import ServerInfo
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

if TYPE_CHECKING:
    from chip.clusters import ClusterCommand


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
        self._nodes: Dict[int, MatterNode] = {}
        self._result_futures: Dict[str, asyncio.Future] = {}

    @property
    def connected(self) -> bool:
        """Return if we're currently connected."""
        return self._ws_client is not None and not self._ws_client.closed

    async def get_nodes(self) -> list[MatterNode]:
        """Return all Matter nodes."""
        if self._nodes:
            # if start_listening is called this dict will be kept up to date
            return list(self._nodes.values())
        data = await self.send_command(APICommand.GET_NODES)
        return [MatterNode.from_dict(x) for x in data]

    async def get_node(self, node_id: int) -> MatterNode:
        """Return Matter node by id."""
        if node_id in self._nodes:
            # if start_listening is called this dict will be kept up to date
            return self._nodes[node_id]
        data = await self.send_command(APICommand.GET_NODE, node_id=node_id)
        return MatterNode.from_dict(data)

    async def commission_with_code(self, code: str) -> MatterNode:
        """
        Commission a device using QRCode or ManualPairingCode.

        Returns full NodeInfo once complete.
        """
        data = await self.send_command(APICommand.COMMISSION_WITH_CODE, code=code)
        return MatterNode.from_dict(data)

    async def commission_on_network(self, setup_pin_code: int) -> MatterNode:
        """
        Commission a device already connected to the network.

        Returns full NodeInfo once complete.
        """
        data = await self.send_command(APICommand.COMMISSION_ON_NETWORK, setup_pin_code=setup_pin_code)
        return MatterNode.from_dict(data)

    async def set_wifi_credentials(self, setup_pin_code: int) -> None:
        """Set WiFi credentials for commissioning to a (new) device."""
        await self.send_command(APICommand.SET_WIFI_CREDENTIALS, setup_pin_code=setup_pin_code)

    async def send_device_command(self, node_id: int, endpoint: int, payload: ClusterCommand) -> Any:
        """Send a command to a Matter node/device."""
        return await self.send_command(APICommand.DEVICE_COMMAND, node_id=node_id, endpoint=endpoint, payload=payload)

    async def send_command(
        self,
        command: str,
        require_schema: int | None = None,
        **kwargs
    ) -> Any:
        """Send a command and get a response."""
        if require_schema is not None and require_schema > self.server_info.schema_version:
            raise InvalidServerVersion(
                "Command not available due to incompatible server version. Update the Matter "
                f"Server to a version that supports at least api schema {require_schema}."
            )

        message = CommandMessage(
            message_id=uuid.uuid4().hex,
            command=command,
            args=kwargs,
        )
        future: asyncio.Future[dict] = self._loop.create_future()
        self._result_futures[message.message_id] = future
        await self._send_message(message)
        try:
            return await future
        finally:
            self._result_futures.pop(message.message_id)

    async def send_command_no_wait(
        self, command: str, require_schema: int | None = None, **kwargs
    ) -> None:
        """Send a command without waiting for the response."""
        if require_schema is not None and require_schema > self.server_info.schema_version:
            raise InvalidServerVersion(
                "Command not available due to incompatible server version. Update the Matter "
                f"Server to a version that supports at least api schema {require_schema}."
            )
        message = CommandMessage(
            message_id=uuid.uuid4().hex,
            command=command,
            args=kwargs,
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

    async def start_listening(self, driver_ready: asyncio.Event) -> None:
        """Start listening to the websocket (and receive initial state)."""
        if not self.connected:
            raise InvalidState("Not connected when start listening")

        try:
            nodes = await self.send_command(APICommand.START_LISTENING)
            self._nodes = nodes

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

            future = self._result_futures.get(msg.message_id)

            if future is None:
                # no listener for this result
                return

            if isinstance(msg, SuccessResultMessage):
                msg: SuccessResultMessage = msg
                future.set_result(msg.result)
                return
            if isinstance(msg, ErrorResultMessage):
                msg: ErrorResultMessage = msg
                future.set_exception(FailedCommand(msg.message_id, msg.errorCode))
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
