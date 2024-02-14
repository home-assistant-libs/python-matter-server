"""Implementation of a Websocket-based server to proxy Matter support (using CHIP SDK)."""

from __future__ import annotations

import asyncio
import ipaddress
import logging
import weakref
from typing import Any, Callable, Set, cast

from aiohttp import web

from matter_server.server.helpers.custom_web_runner import MultiHostTCPSite

from ..common.const import SCHEMA_VERSION
from ..common.errors import VersionMismatch
from ..common.helpers.api import APICommandHandler, api_command
from ..common.helpers.json import json_dumps
from ..common.helpers.util import chip_clusters_version, chip_core_version
from ..common.models import (
    APICommand,
    EventCallBackType,
    EventType,
    ServerDiagnostics,
    ServerInfoMessage,
)
from ..server.client_handler import WebsocketClientHandler
from .const import MIN_SCHEMA_VERSION
from .device_controller import MatterDeviceController
from .stack import MatterStack
from .storage import StorageController
from .vendor_info import VendorInfo


def mount_websocket(server: MatterServer, path: str) -> None:
    """Mount the websocket endpoint."""
    clients: weakref.WeakSet[WebsocketClientHandler] = weakref.WeakSet()

    async def _handle_ws(request: web.Request) -> web.WebSocketResponse:
        connection = WebsocketClientHandler(server, request)
        try:
            clients.add(connection)
            return await connection.handle_client()
        finally:
            clients.remove(connection)

    async def _handle_shutdown(app: web.Application) -> None:
        # pylint: disable=unused-argument
        for client in set(clients):
            await client.disconnect()

    server.app.on_shutdown.append(_handle_shutdown)
    server.app.router.add_route("GET", path, _handle_ws)


class MatterServer:
    """Serve Matter stack over WebSockets."""

    # pylint: disable=too-many-instance-attributes

    _runner: web.AppRunner | None = None
    _http: MultiHostTCPSite | None = None

    def __init__(
        self,
        storage_path: str,
        vendor_id: int,
        fabric_id: int,
        port: int,
        listen_addresses: list[str] | None = None,
        primary_interface: str | None = None,
    ) -> None:
        """Initialize the Matter Server."""
        self.storage_path = storage_path
        self.vendor_id = vendor_id
        self.fabric_id = fabric_id
        self.port = port
        self.listen_addresses = listen_addresses
        self.primary_interface = primary_interface
        self.logger = logging.getLogger(__name__)
        self.app = web.Application()
        self.loop: asyncio.AbstractEventLoop | None = None
        # Instantiate the Matter Stack using the SDK using the given storage path
        self.stack = MatterStack(self)
        # Initialize our (intermediate) device controller which keeps track
        # of Matter devices and their subscriptions.
        self.device_controller = MatterDeviceController(self)
        self.storage = StorageController(self)
        self.vendor_info = VendorInfo(self)
        # we dynamically register command handlers
        self.command_handlers: dict[str, APICommandHandler] = {}
        self._subscribers: Set[EventCallBackType] = set()
        self._register_api_commands()

    async def start(self) -> None:
        """Start running the Matter server."""
        self.logger.info("Starting the Matter Server...")
        # safety shield: make sure we use same clusters and core packages!
        if chip_clusters_version() != chip_core_version():
            raise VersionMismatch(
                "CHIP Core version does not match CHIP Clusters version."
            )
        self.loop = asyncio.get_running_loop()
        await self.device_controller.initialize()
        await self.storage.start()
        await self.device_controller.start()
        await self.vendor_info.start()
        mount_websocket(self, "/ws")
        self.app.router.add_route("GET", "/", self._handle_info)
        self._runner = web.AppRunner(self.app, access_log=None)
        await self._runner.setup()
        self._http = MultiHostTCPSite(
            self._runner, host=self.listen_addresses, port=self.port
        )
        await self._http.start()
        self.logger.debug("Webserver initialized.")

    async def stop(self) -> None:
        """Stop running the server."""
        self.logger.info("Stopping the Matter Server...")
        if self._http is None or self._runner is None:
            raise RuntimeError("Server not started.")

        self.signal_event(EventType.SERVER_SHUTDOWN)
        await self._http.stop()
        await self._runner.cleanup()
        await self.app.shutdown()
        await self.app.cleanup()
        await self.device_controller.stop()
        await self.storage.stop()
        self.stack.shutdown()
        self.logger.debug("Cleanup complete")

    def subscribe(
        self, callback: Callable[[EventType, Any], None]
    ) -> Callable[[], None]:
        """
        Subscribe to events.

        Returns handle to remove subscription.
        """

        def unsub() -> None:
            self._subscribers.remove(callback)

        self._subscribers.add(callback)
        return unsub

    @api_command(APICommand.SERVER_INFO)
    def get_info(self) -> ServerInfoMessage:
        """Return (version)info of the Matter Server."""
        assert self.device_controller.compressed_fabric_id is not None
        return ServerInfoMessage(
            fabric_id=self.fabric_id,
            compressed_fabric_id=self.device_controller.compressed_fabric_id,
            schema_version=SCHEMA_VERSION,
            min_supported_schema_version=MIN_SCHEMA_VERSION,
            sdk_version=chip_clusters_version(),
            wifi_credentials_set=self.device_controller.wifi_credentials_set,
            thread_credentials_set=self.device_controller.thread_credentials_set,
        )

    @api_command(APICommand.SERVER_DIAGNOSTICS)
    def get_diagnostics(self) -> ServerDiagnostics:
        """Return a full dump of the server (for diagnostics)."""
        return ServerDiagnostics(
            info=self.get_info(),
            nodes=self.device_controller.get_nodes(),
            events=list(self.device_controller.event_history),
        )

    def signal_event(self, evt: EventType, data: Any = None) -> None:
        """Signal event to listeners."""
        for callback in self._subscribers:
            if asyncio.iscoroutinefunction(callback):
                asyncio.create_task(callback(evt, data))
            else:
                callback(evt, data)

    def scope_ipv6_lla(self, ip_addr: str) -> str:
        """Scope IPv6 link-local addresses to primary interface.

        IPv6 link-local addresses received through the websocket might have no
        scope_id or a scope_id which isn't valid on this device. Just assume the
        device is connected on the primary interface.
        """
        ip_addr_parsed = ipaddress.ip_address(ip_addr)
        if not ip_addr_parsed.is_link_local or ip_addr_parsed.version != 6:
            return ip_addr

        ip_addr_parsed = cast(ipaddress.IPv6Address, ip_addr_parsed)

        if ip_addr_parsed.scope_id is not None:
            # This type of IPv6 manipulation is not supported by the ipaddress lib
            ip_addr = ip_addr.split("%")[0]

        # Rely on host OS routing table
        if self.primary_interface is None:
            return ip_addr

        self.logger.debug(
            "Setting scope of link-local IP address %s to %s",
            ip_addr,
            self.primary_interface,
        )
        return f"{ip_addr}%{self.primary_interface}"

    def register_api_command(
        self,
        command: str,
        handler: Callable,
    ) -> None:
        """Dynamically register a command on the API."""
        assert command not in self.command_handlers, "Command already registered"
        self.command_handlers[command] = APICommandHandler.parse(command, handler)

    def _register_api_commands(self) -> None:
        """Register all methods decorated as api_command."""
        for cls in (self, self.device_controller, self.vendor_info):
            for attr_name in dir(cls):
                if attr_name.startswith("__"):
                    continue
                val = getattr(cls, attr_name)
                if not hasattr(val, "api_cmd"):
                    continue
                if hasattr(val, "mock_calls"):
                    # filter out mocks
                    continue
                # method is decorated with our api decorator
                self.register_api_command(val.api_cmd, val)

    async def _handle_info(self, request: web.Request) -> web.Response:
        """Handle info endpoint to serve basic server (version) info."""
        # pylint: disable=unused-argument
        return web.json_response(self.get_info(), dumps=json_dumps)
