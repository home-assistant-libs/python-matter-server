"""Logic to manage the WebSocket connection to the Matter server."""
from __future__ import annotations

import asyncio
import logging
import pprint
from typing import Any, Callable, Dict, Final, cast

from aiohttp import ClientSession, ClientWebSocketResponse, WSMsgType, client_exceptions

from ..common.helpers.json import json_dumps, json_loads
from ..common.helpers.util import chip_clusters_version, parse_message
from ..common.models.events import EventType
from ..common.models.message import CommandMessage, MessageType, ServerInfoMessage
from ..common.models.node import MatterNode
from ..common.models.server_information import ServerInfo
from .const import MIN_SCHEMA_VERSION
from .exceptions import (
    CannotConnect,
    ConnectionClosed,
    ConnectionFailed,
    InvalidMessage,
    InvalidServerVersion,
    InvalidState,
    NotConnected,
)

LOGGER = logging.getLogger(f"{__package__}.connection")
SUB_WILDCARD: Final = "*"


class MatterClientConnection:
    """Manage a Matter server over WebSockets."""

    def __init__(
        self,
        ws_server_url: str,
        aiohttp_session: ClientSession,
    ):
        """Initialize the Client class."""
        self.ws_server_url = ws_server_url
        self.aiohttp_session = aiohttp_session
        # server info is retrieved on connect
        self.server_info: ServerInfo | None = None
        self._ws_client: ClientWebSocketResponse | None = None
        self._nodes: Dict[int, MatterNode] = {}
        self._result_futures: Dict[str, asyncio.Future] = {}
        self._subscribers: dict[str, list[Callable[[EventType, Any], None]]] = {}

    @property
    def connected(self) -> bool:
        """Return if we're currently connected."""
        return self._ws_client is not None and not self._ws_client.closed

    async def connect(self) -> None:
        """Connect to the websocket server."""
        if self._ws_client is not None:
            raise InvalidState("Already connected")

        LOGGER.debug("Trying to connect")
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
        info = cast(ServerInfoMessage, await self.receive_message_or_raise())
        self.server_info = info

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
            LOGGER.warning(
                "Matter Server detected with schema version %s "
                "which is higher than the preferred api schema %s of this client"
                " - you may run into compatibility issues.",
                info.schema_version,
                MIN_SCHEMA_VERSION,
            )

        LOGGER.info(
            "Connected to Matter Fabric %s (%s), Schema version %s, CHIP SDK Version %s",
            info.fabric_id,
            info.compressed_fabric_id,
            info.schema_version,
            info.sdk_version,
        )

    async def disconnect(self) -> None:
        """Disconnect the client."""
        LOGGER.debug("Closing client connection")
        if self._ws_client is not None and not self._ws_client.closed:
            await self._ws_client.close()
        self._ws_client = None

    async def receive_message_or_raise(self) -> MessageType:
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
            msg = parse_message(json_loads(ws_msg.data))
        except TypeError as err:
            raise InvalidMessage(f"Received unsupported JSON: {err}") from err
        except ValueError as err:
            raise InvalidMessage("Received invalid JSON.") from err

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("Received message:\n%s\n", pprint.pformat(ws_msg))

        return msg

    async def send_message(self, message: CommandMessage) -> None:
        """
        Send a CommandMessage to the server.

        Raises NotConnected if client not connected.
        """
        if not self.connected:
            raise NotConnected

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("Publishing message:\n%s\n", pprint.pformat(message))

        assert self._ws_client
        assert isinstance(message, CommandMessage)

        await self._ws_client.send_json(message, dumps=json_dumps)

    def __repr__(self) -> str:
        """Return the representation."""
        prefix = "" if self.connected else "not "
        return f"{type(self).__name__}(ws_server_url={self.ws_server_url!r}, {prefix}connected)"
