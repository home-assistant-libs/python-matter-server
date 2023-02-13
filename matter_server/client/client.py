"""Matter Client implementation."""
from __future__ import annotations

import asyncio
import logging
from types import TracebackType
from typing import TYPE_CHECKING, Any, Callable, Dict, Final, Optional, cast
import uuid

from aiohttp import ClientSession

from ..common.helpers.util import dataclass_from_dict, dataclass_to_dict
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
from .exceptions import (
    ConnectionClosed,
    FailedCommand,
    InvalidServerVersion,
    InvalidState,
)

if TYPE_CHECKING:
    from chip.clusters.Objects import ClusterCommand

SUB_WILDCARD: Final = "*"


class MatterClient:
    """Manage a Matter server over WebSockets."""

    def __init__(self, ws_server_url: str, aiohttp_session: ClientSession):
        """Initialize the Client class."""
        self.connection = MatterClientConnection(ws_server_url, aiohttp_session)
        self.logger = logging.getLogger(__package__)
        self._nodes: Dict[int, MatterNode] = {}
        self._result_futures: Dict[str, asyncio.Future] = {}
        self._subscribers: dict[str, list[Callable[[EventType, Any], None]]] = {}
        self._stop_called: bool = False
        self._loop: asyncio.AbstractEventLoop | None = None

    @property
    def server_info(self) -> ServerInfo | None:
        """Return info of the server we're currently connected to."""
        return self.connection.server_info

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

    async def get_nodes(self) -> list[MatterNode]:
        """Return all Matter nodes."""
        if self._nodes:
            # if start_listening is called this dict will be kept up to date
            return list(self._nodes.values())
        data = await self.send_command(APICommand.GET_NODES)
        return [dataclass_from_dict(MatterNode, x) for x in data]

    async def get_node(self, node_id: int) -> MatterNode:
        """Return Matter node by id."""
        if node_id in self._nodes:
            # if start_listening is called this dict will be kept up to date
            return self._nodes[node_id]
        data = await self.send_command(APICommand.GET_NODE, node_id=node_id)
        return dataclass_from_dict(MatterNode, data)

    async def commission_with_code(self, code: str) -> MatterNode:
        """
        Commission a device using QRCode or ManualPairingCode.

        Returns full NodeInfo once complete.
        """
        data = await self.send_command(APICommand.COMMISSION_WITH_CODE, code=code)
        return dataclass_from_dict(MatterNode, data)

    async def commission_on_network(self, setup_pin_code: int) -> MatterNode:
        """
        Commission a device already connected to the network.

        Returns full NodeInfo once complete.
        """
        data = await self.send_command(
            APICommand.COMMISSION_ON_NETWORK, setup_pin_code=setup_pin_code
        )
        return dataclass_from_dict(MatterNode, data)

    async def set_wifi_credentials(self, ssid: str, credentials: str) -> None:
        """Set WiFi credentials for commissioning to a (new) device."""
        await self.send_command(
            APICommand.SET_WIFI_CREDENTIALS, ssid=ssid, credentials=credentials
        )

    async def set_thread_operational_dataset(self, dataset: str) -> None:
        """Set Thread Operational dataset in the stack."""
        await self.send_command(APICommand.SET_THREAD_DATASET, dataset=dataset)

    async def open_commissioning_window(
        self,
        node_id: int,
        timeout: int = 300,
        iteration: int = 1000,
        option: int = 0,
        discriminator: Optional[int] = None,
    ) -> int:
        """
        Open a commissioning window to commission a device present on this controller to another.

        Returns code to use as discriminator.
        """
        return cast(
            int,
            await self.send_command(
                APICommand.OPEN_COMMISSIONING_WINDOW,
                node_id=node_id,
                timeout=timeout,
                iteration=iteration,
                option=option,
                discriminator=discriminator,
            ),
        )

    async def send_device_command(
        self,
        node_id: int,
        endpoint: int,
        command: ClusterCommand,
        response_type: Any | None = None,
        timed_request_timeout_ms: int | None = None,
        interaction_timeout_ms: int | None = None,
    ) -> Any:
        """Send a command to a Matter node/device."""
        payload = dataclass_to_dict(command)
        return await self.send_command(
            APICommand.DEVICE_COMMAND,
            node_id=node_id,
            endpoint=endpoint,
            payload=payload,
            response_type=response_type,
            timed_request_timeout_ms=timed_request_timeout_ms,
            interaction_timeout_ms=interaction_timeout_ms,
        )

    async def remove_node(self, node_id: int) -> None:
        """Remove a Matter node/device from the fabric."""
        await self.send_command(APICommand.REMOVE_NODE, node_id=node_id)

    async def send_command(
        self,
        command: str,
        require_schema: int | None = None,
        **kwargs: Any,
    ) -> Any:
        """Send a command and get a response."""
        if not self.connection.connected or not self._loop:
            raise InvalidState("Not connected")

        if (
            require_schema is not None
            and self.server_info is not None
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
        future: asyncio.Future[Any] = self._loop.create_future()
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

    async def get_diagnostics(self) -> ServerDiagnostics:
        """Return a full dump of the server (for diagnostics)."""
        data = await self.send_command(APICommand.SERVER_DIAGNOSTICS)
        return dataclass_from_dict(ServerDiagnostics, data)

    async def connect(self) -> None:
        """Connect to the Matter Server (over Websockets)."""
        self._loop = asyncio.get_running_loop()
        if self.connection.connected:
            # already connected
            return
        # NOTE: connect will raise when connecting failed
        await self.connection.connect()

    async def start_listening(self, init_ready: asyncio.Event | None = None) -> None:
        """Start listening to the websocket (and receive initial state)."""
        await self.connect()

        try:
            message = CommandMessage(
                message_id=uuid.uuid4().hex, command=APICommand.START_LISTENING
            )
            await self.connection.send_message(message)
            nodes_msg = cast(
                SuccessResultMessage, await self.connection.receive_message_or_raise()
            )
            # a full dump of all nodes will be the result of the start_listening command
            nodes = {
                x["node_id"]: dataclass_from_dict(MatterNode, x)
                for x in nodes_msg.result
            }
            self._nodes = nodes
            # once we've hit this point we're all set
            self.logger.info("Matter client initialized.")
            if init_ready is not None:
                init_ready.set()

            # keep reading incoming messages
            while not self._stop_called:
                msg = await self.connection.receive_message_or_raise()
                self._handle_incoming_message(msg)
        except ConnectionClosed:
            pass
        finally:
            await self.disconnect()

    async def disconnect(self) -> None:
        """Disconnect the client and cleanup."""
        self._stop_called = True
        # cancel all command-tasks awaiting a result
        for future in self._result_futures.values():
            future.cancel()
        await self.connection.disconnect()

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
            self.logger.debug("Received event: %s", msg)
            self._handle_event_message(msg)
            return

        # Log anything we can't handle here
        self.logger.debug(
            "Received message with unknown type '%s': %s",
            type(msg),
            msg,
        )

    def _handle_event_message(self, msg: EventMessage) -> None:
        """Handle incoming event from the server."""
        if msg.event == EventType.NODE_ADDED:
            node = dataclass_from_dict(MatterNode, msg.data)
            self._nodes[node.node_id] = node
            self._signal_event(EventType.NODE_ADDED, node)
            return
        if msg.event == EventType.ATTRIBUTE_UPDATED:
            attr = dataclass_from_dict(MatterAttribute, msg.data)
            self._nodes[attr.node_id].attributes[attr.path] = attr
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
        url = self.connection.ws_server_url
        prefix = "" if self.connection.connected else "not "
        return f"{type(self).__name__}(ws_server_url={url!r}, {prefix}connected)"
