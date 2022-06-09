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

from aiohttp import ClientSession, ClientWebSocketResponse, WSMsgType, client_exceptions

from ..common.json_utils import CHIPJSONDecoder, CHIPJSONEncoder
from ..common.model.message import (
    CommandMessage,
    ErrorResultMessage,
    Message,
    ResultMessage,
    ServerInformation,
    SubscriptionReportMessage,
    SuccessResultMessage,
)
from ..common.model.version import VersionInfo
from .const import MAX_SERVER_SCHEMA_VERSION, MIN_SERVER_SCHEMA_VERSION
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
from .model.driver import Driver

SIZE_PARSE_JSON_EXECUTOR = 8192

# Message IDs
SET_API_SCHEMA_MESSAGE_ID = "api-schema-id"
GET_INITIAL_LOG_CONFIG_MESSAGE_ID = "get-initial-log-config"
START_LISTENING_MESSAGE_ID = "listen-id"

LISTEN_MESSAGE_IDS = (
    GET_INITIAL_LOG_CONFIG_MESSAGE_ID,
    SET_API_SCHEMA_MESSAGE_ID,
    START_LISTENING_MESSAGE_ID,
)


class Client:
    """Class to manage the connection to the Matter server."""

    def __init__(
        self,
        ws_server_url: str,
        aiohttp_session: ClientSession,
        schema_version: int = MAX_SERVER_SCHEMA_VERSION,
        record_messages: bool = False,
    ):
        """Initialize the Client class."""
        self.ws_server_url = ws_server_url
        self.aiohttp_session = aiohttp_session
        self.driver: Driver | None = None
        # The WebSocket client
        self._client: ClientWebSocketResponse | None = None
        # Version of the connected server
        self.version: VersionInfo | None = None
        self.server_info: ServerInformation | None = None
        self.schema_version: int = schema_version
        self.logger = logging.getLogger(__package__)
        self._loop = asyncio.get_running_loop()
        self._result_futures: Dict[str, asyncio.Future] = {}
        self._shutdown_complete_event: asyncio.Event | None = None
        self._record_messages = record_messages
        self._recorded_commands: DefaultDict[str, dict] = defaultdict(dict)
        self._recorded_events: List[dict] = []

    def __repr__(self) -> str:
        """Return the representation."""
        prefix = "" if self.connected else "not "
        return f"{type(self).__name__}(ws_server_url={self.ws_server_url!r}, {prefix}connected)"

    @property
    def connected(self) -> bool:
        """Return if we're currently connected."""
        return self._client is not None and not self._client.closed

    @property
    def recording_messages(self) -> bool:
        """Return True if messages are being recorded."""
        return self._record_messages

    async def async_send_command(
        self,
        command: str,
        args: dict[str, Any],
        require_schema: int | None = None,
    ) -> dict:
        """Send a command and get a response."""
        if require_schema is not None and require_schema > self.schema_version:
            raise InvalidServerVersion(
                "Command not available due to incompatible server version. Update the Z-Wave "
                f"JS Server to a version that supports at least api schema {require_schema}."
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
        if require_schema is not None and require_schema > self.schema_version:
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
        if self.driver is not None:
            raise InvalidState("Re-connected with existing driver")

        self.logger.debug("Trying to connect")
        try:
            self._client = await self.aiohttp_session.ws_connect(
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

        self.version = version = await self._receive_message_or_raise()

        # basic check for server schema version compatibility
        if (
            self.version.min_schema_version > MIN_SERVER_SCHEMA_VERSION
            or self.version.max_schema_version < MIN_SERVER_SCHEMA_VERSION
        ):
            await self._client.close()
            raise InvalidServerVersion(
                f"Matter Server version is incompatible: {self.version.server_version} "
                "a version is required that supports at least "
                f"api schema {MIN_SERVER_SCHEMA_VERSION}"
            )
        # store the (highest possible) schema version we're going to use/request
        # this is a bit future proof as we might decide to use a pinned version at some point
        # for now we just negotiate the highest available schema version and
        # guard incompatibility with the MIN_SERVER_SCHEMA_VERSION
        if self.version.max_schema_version < MAX_SERVER_SCHEMA_VERSION:
            self.schema_version = self.version.max_schema_version

        await self._send_message(
            CommandMessage(
                messageId="server-get-info",
                command="server.GetInfo",
                args={},
            )
        )
        msg = await self._receive_message_or_raise()

        if (
            not isinstance(msg, SuccessResultMessage)
            or not isinstance(msg.result, ServerInformation)
            or msg.messageId != "server-get-info"
        ):
            raise InvalidMessage(
                "Expected a SuccessResultMessage with messageId 'server-get-info'"
            )

        self.server_info = msg.result

        self.logger.info(
            "Connected to Server %s, Driver %s, Using Schema %s",
            version.server_version,
            version.driver_version,
            self.schema_version,
        )

    async def listen(self, driver_ready: asyncio.Event) -> None:
        """Start listening to the websocket."""
        if not self.connected:
            raise InvalidState("Not connected when start listening")

        assert self._client

        try:
            self.driver = Driver(self, self.server_info)

            self.logger.info("Matter initialized.")
            driver_ready.set()

            while not self._client.closed:
                data = await self._receive_message_or_raise()

                self._handle_incoming_message(data)
        except ConnectionClosed:
            pass

        finally:
            self.logger.debug("Listen completed. Cleaning up")

            for future in self._result_futures.values():
                future.cancel()

            if not self._client.closed:
                await self._client.close()

            if self._shutdown_complete_event:
                self._shutdown_complete_event.set()

    async def disconnect(self) -> None:
        """Disconnect the client."""
        self.logger.debug("Closing client connection")

        if not self.connected:
            return

        assert self._client

        # 'listen' was never called
        if self.driver is None:
            await self._client.close()
            return

        self._shutdown_complete_event = asyncio.Event()
        await self._client.close()
        await self._shutdown_complete_event.wait()

        self._shutdown_complete_event = None
        self.driver = None

    def begin_recording_messages(self) -> None:
        """Begin recording messages for replay later."""
        if self._record_messages:
            raise InvalidState("Already recording messages")

        self._record_messages = True

    def end_recording_messages(self) -> List[dict]:
        """End recording messages and return messages that were recorded."""
        if not self._record_messages:
            raise InvalidState("Not recording messages")

        self._record_messages = False

        data = sorted(
            (*self._recorded_commands.values(), *self._recorded_events),
            key=itemgetter("ts"),
        )
        self._recorded_commands.clear()
        self._recorded_events.clear()

        return list(data)

    async def _receive_message_or_raise(self) -> Message:
        """Receive message or raise."""
        assert self._client
        msg = await self._client.receive()

        if msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSED, WSMsgType.CLOSING):
            raise ConnectionClosed("Connection was closed.")

        if msg.type == WSMsgType.ERROR:
            raise ConnectionFailed()

        if msg.type != WSMsgType.TEXT:
            raise InvalidMessage(f"Received non-Text message: {msg.type}")

        try:
            if len(msg.data) > SIZE_PARSE_JSON_EXECUTOR:
                obj: dict = await self._loop.run_in_executor(
                    None, lambda: json.loads(msg.data, cls=CHIPJSONDecoder)
                )
            else:
                obj = json.loads(msg.data, cls=CHIPJSONDecoder)
        except ValueError as err:
            raise InvalidMessage("Received invalid JSON.") from err

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("Received message:\n%s\n", pprint.pformat(msg))

        return obj

    def _handle_incoming_message(self, msg: Any) -> None:
        """Handle incoming message.

        Run all async tasks in a wrapper to log appropriately.
        """
        if isinstance(msg, ResultMessage):
            msg: ResultMessage = msg
            future = self._result_futures.get(msg.messageId)

            if future is None:
                # no listener for this result
                return

            if self._record_messages and msg.messageId not in LISTEN_MESSAGE_IDS:
                self._recorded_commands[msg.messageId].update(
                    {
                        "result_ts": datetime.utcnow().isoformat(),
                        "result_msg": deepcopy(msg),
                    }
                )

            if isinstance(msg, SuccessResultMessage):
                msg: SuccessResultMessage = msg
                future.set_result(msg.result)
                return
            elif isinstance(msg, ErrorResultMessage):
                msg: ErrorResultMessage = msg
                future.set_exception(FailedCommand(msg.messageId, msg.errorCode))
            else:
                raise InvalidMessage("Invalid ResultMessage.")

            return
        elif isinstance(msg, SubscriptionReportMessage):
            self.logger.debug(
                "Received subscription report: %s",
                msg,
            )

            if self._record_messages:
                self._recorded_events.append(
                    {
                        "record_type": "subscription_report",
                        "ts": datetime.utcnow().isoformat(),
                        "payload": deepcopy(msg),
                    }
                )

            self.driver.read_subscriptions.receive_event(msg.payload)
        else:
            # Can't handle
            self.logger.debug(
                "Received message with unknown type '%s': %s",
                type(msg),
                msg,
            )
            return

    async def _send_message(self, message: CommandMessage) -> None:
        """Send a message.

        Raises NotConnected if client not connected.
        """
        if not self.connected:
            raise NotConnected

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("Publishing message:\n%s\n", pprint.pformat(message))

        assert self._client
        assert isinstance(message, CommandMessage)

        if self._record_messages and message.messageId not in LISTEN_MESSAGE_IDS:
            # We don't need to deepcopy command_msg because it is always released by
            # the caller after the command is sent.
            self._recorded_commands[message.messageId].update(
                {
                    "record_type": "command",
                    "ts": datetime.utcnow().isoformat(),
                    "command": message["command"],
                    "command_msg": message,
                }
            )

        await self._client.send_json(
            message, dumps=partial(json.dumps, cls=CHIPJSONEncoder)
        )

    async def __aenter__(self) -> "Client":
        """Connect to the websocket."""
        await self.connect()
        return self

    async def __aexit__(
        self, exc_type: Exception, exc_value: str, traceback: TracebackType
    ) -> None:
        """Disconnect from the websocket."""
        await self.disconnect()
