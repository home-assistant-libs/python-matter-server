"""Matter Client implementation."""
from __future__ import annotations

import asyncio
import logging
from types import TracebackType
from typing import TYPE_CHECKING, Any, Callable, Dict, Final, NoReturn, Optional, cast
import uuid

from aiohttp import ClientSession

from ..common.helpers.util import dataclass_from_dict
from ..common.models.api_command import APICommand
from ..common.models.events import EventType
from ..common.models.message import (
    CommandMessage,
    ErrorResultMessage,
    EventMessage,
    MessageType,
    ResultMessageBase,
    SuccessResultMessage,
)
from ..common.models.node import MatterAttribute, MatterNode
from ..common.models.server_information import ServerDiagnostics, ServerInfo
from .connection import MatterClientConnection
from .devices import MatterClientDeviceController
from .exceptions import (
    ConnectionClosed,
    FailedCommand,
    InvalidServerVersion,
    InvalidState,
    CannotConnect,
)

SUB_WILDCARD: Final = "*"

LOGGER = logging.getLogger(__package__)


class MatterClient:
    """Python Matter Server - Client implementation."""

    def __init__(self, ws_server_url: str, aiohttp_session: ClientSession):
        """Initialize the Matter Client class."""
        self.loop: asyncio.AbstractEventLoop | None = None
        self.connection = MatterClientConnection(ws_server_url, aiohttp_session)
        self.devices = MatterClientDeviceController(self)
        self._result_futures: Dict[str, asyncio.Future] = {}
        self._subscribers: dict[str, list[Callable[[EventType, Any], None]]] = {}
        self._listen_task: asyncio.Task | None = None
        self._stop_called = False

    @property
    def server_info(self) -> ServerInfo | None:
        """Return info of the server we're currently connected to."""
        return self.connection.server_info

    async def connect(self) -> None:
        """Connect to the Websocket Server."""
        if self.connection.connected:
            # already connected
            return
        await self.connection.connect()
        # connect will raise when connecting failed,
        # otherwise signal connected event
        self._signal_event(EventType.CONNECTED)

    async def start(self) -> None:
        """Start listening to the websocket (and receive initial state)."""
        self.loop = asyncio.get_running_loop()
        if self._listen_task is not None:
            raise InvalidState("Listen task is already running")
        await self.connect()
        message = CommandMessage(
            message_id=uuid.uuid4().hex, command=APICommand.START_LISTENING
        )
        await self.connection.send_message(message)
        nodes_msg = cast(
            SuccessResultMessage, await self.connection.receive_message_or_raise()
        )
        # a full dump of all nodes will be the result of the start_listening command
        nodes = {
            x["node_id"]: dataclass_from_dict(MatterNode, x) for x in nodes_msg.result
        }
        self.devices.nodes = nodes

        # start task that keeps reading incoming messages
        self._listen_task = asyncio.create_task(self.__listen())
        # once we've hit this point we're all set
        self._signal_event(EventType.INITIALIZED)
        LOGGER.info("Matter client initialized.")

    async def stop(self) -> None:
        """Gracefully shutdown the Matter client."""
        self._stop_called = True
        # cancel all command-tasks awaiting a result
        for future in self._result_futures.values():
            future.cancel()
        # stop the listen task
        if self._listen_task is not None and not self._listen_task.cancelled():
            self._listen_task.cancel()
            await self._listen_task
        # close the client if it is still connected
        await self.connection.disconnect()

    def subscribe(
        self,
        callback: Callable[[EventType, Any], None],
        event_filter: Optional[EventType] = None,
        node_filter: Optional[int] = None,
        attr_path_filter: Optional[str] = None,
    ) -> Callable[[], None]:
        """
        Subscribe to node and server events.

        Optionally filter by specific events or node attributes.
        Returns:
            function to unsubscribe.
        """
        # for fast lookups we create a key based on the filters, allowing
        # a "catch all" with a wildcard (*).
        _event_filter: str
        if event_filter is None:
            _event_filter = SUB_WILDCARD
        else:
            _event_filter = event_filter.value

        _node_filter: str
        if node_filter is None:
            _node_filter = SUB_WILDCARD
        else:
            _node_filter = str(node_filter)

        if attr_path_filter is None:
            attr_path_filter = SUB_WILDCARD

        key = f"{_event_filter}/{_node_filter}/{attr_path_filter}"
        self._subscribers.setdefault(key, [])
        self._subscribers[key].append(callback)

        def unsubscribe() -> None:
            self._subscribers[key].remove(callback)

        return unsubscribe

    async def get_diagnostics(self, code: str) -> ServerDiagnostics:
        """Return a full dump of the server (for diagnostics)."""
        data = await self.send_command(APICommand.SERVER_DIAGNOSTICS)
        return dataclass_from_dict(ServerDiagnostics, data)

    async def send_command(
        self,
        command: str,
        require_schema: int | None = None,
        **kwargs: Any,
    ) -> Any:
        """Send a command and get a response."""
        if not self.server_info:
            raise InvalidState("Not connected")

        if (
            require_schema is not None
            and require_schema > self.server_info.schema_version
        ):
            raise InvalidServerVersion(
                "Command not available due to incompatible server version. Update the Matter "
                f"Server to a version that supports at least api schema {require_schema}."
            )

        message = CommandMessage(
            message_id=uuid.uuid4().hex,
            command=command,
            args=kwargs,
        )
        future: asyncio.Future[Any] = self.loop.create_future()
        self._result_futures[message.message_id] = future
        await self.connection.send_message(message)
        try:
            return await future
        finally:
            self._result_futures.pop(message.message_id)

    async def send_command_no_wait(
        self,
        command: str,
        require_schema: int | None = None,
        **kwargs: Any,
    ) -> None:
        """Send a command without waiting for the response."""
        if not self.server_info:
            raise InvalidState("Not connected")

        if (
            require_schema is not None
            and require_schema > self.server_info.schema_version
        ):
            raise InvalidServerVersion(
                "Command not available due to incompatible server version. Update the Matter "
                f"Server to a version that supports at least api schema {require_schema}."
            )
        message = CommandMessage(
            message_id=uuid.uuid4().hex,
            command=command,
            args=kwargs,
        )
        await self.connection.send_message(message)

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
                future.set_result(msg.result)
                return
            if isinstance(msg, ErrorResultMessage):
                future.set_exception(
                    FailedCommand(msg.message_id, str(msg.error_code.value))
                )
                return

        # handle EventMessage
        if isinstance(msg, EventMessage):
            LOGGER.debug("Received event: %s", msg)
            self._handle_event_message(msg)
            return

        # Log anything we can't handle here
        LOGGER.debug(
            "Received message with unknown type '%s': %s",
            type(msg),
            msg,
        )

    def _handle_event_message(self, msg: EventMessage) -> None:
        """Handle incoming event from the server."""
        if msg.event == EventType.NODE_ADDED:
            node = dataclass_from_dict(MatterNode, msg.data)
            self.devices.nodes[node.node_id] = node
            self._signal_event(EventType.NODE_ADDED, node)
            return
        if msg.event == EventType.ATTRIBUTE_UPDATED:
            attr = dataclass_from_dict(MatterAttribute, msg.data)
            self.devices.nodes[attr.node_id].attributes[attr.path] = attr
            self._signal_event(
                EventType.ATTRIBUTE_UPDATED, attr, attr.node_id, attr.path
            )
            return
        # TODO: handle any other events ?
        self._signal_event(msg.event, msg.data)

    def _signal_event(
        self,
        event: EventType,
        data: Any = None,
        node_id: Optional[int] = None,
        attribute_path: Optional[str] = None,
    ) -> None:
        """Signal event to all subscribers."""
        # instead of iterating all subscribers we iterate over subscription keys
        # each callback is stored under a specific key based on the filters
        for evt_key in (event.value, SUB_WILDCARD):
            for node_key in (node_id, SUB_WILDCARD):
                if node_key is None:
                    continue
                for attribute_path_key in (attribute_path, SUB_WILDCARD):
                    if attribute_path_key is None:
                        continue
                    key = f"{evt_key}/{node_key}/{attribute_path_key}"
                    for callback in self._subscribers.get(key, []):
                        callback(event, data)

    async def __listen(self) -> NoReturn:
        """Read incoming messages until stopped."""
        try:
            # keep reading incoming messages
            while self.connection.connected:
                msg = await self.connection.receive_message_or_raise()
                self._handle_incoming_message(msg)
        except ConnectionClosed:
            pass
        finally:
            await self.connection.disconnect()
        if not self._stop_called:
            LOGGER.warning(
                "Connection to Matter Server lost, will reconnect in 5 seconds."
            )
            # signal event so subscribers know we've lost the connection and act on it
            # e.g. HA mark entities unavailable while reconnecting.
            self._signal_event(EventType.CONNECTION_LOST)
            self._listen_task = None
            self.loop.call_later(5, asyncio.create_task, self.__handle_reconnect())

    async def __handle_reconnect(self, attempt=1) -> None:
        """Call when (initialized) connection is lost."""
        try:
            await self.connection.connect()
        except CannotConnect:
            LOGGER.debug(
                "Reconnect attempt %s failed, retrying in 30 seconds...", attempt
            )
            attempt += 1
            # reschedule self
            self.loop.call_later(
                30, asyncio.create_task, self.__handle_reconnect(attempt)
            )
        else:
            # re-initialize when we're reconnected
            # this will re-fetch the complete state
            await self.start()

    async def __aenter__(self) -> "MatterClient":
        """Initialize and connect to the Matter server."""
        await self.start()
        return self

    async def __aexit__(
        self, exc_type: Exception, exc_value: str, traceback: TracebackType
    ) -> None:
        """Gracefully stop/close the MatterClient instance.."""
        await self.stop()

    def __repr__(self) -> str:
        """Return the representation."""
        return f"{type(self).__name__}(ws_server_url={self.ws_server_url!r}"
