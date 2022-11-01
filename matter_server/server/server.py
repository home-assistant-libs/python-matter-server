"""Implementation of a Websocket-based server to proxy Matter support (using CHIP SDK)."""
from __future__ import annotations

import asyncio
from concurrent import futures
from contextlib import suppress
import json
import logging
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Final, Set
import weakref

from aiohttp import WSMsgType, web
import async_timeout

from ..common.model.server_information import ServerInfo, VersionInfo
from ..server.client_handler import WebsocketClientHandler

from ..common.json_utils import CHIPJSONDecoder, CHIPJSONEncoder
from ..common.model.message import CommandMessage
from ..common.model.event import EventType
from .stack import MatterStack
from .storage import StorageController
from .device_controller import MatterDeviceController


def mount_websocket(server: MatterServer, path: str) -> None:
    """Mount the websocket endpoint."""
    clients: Set[WebsocketClientHandler] = weakref.WeakSet()

    async def _handle_ws(request: web.Request):
        connection = WebsocketClientHandler(server, request)
        try:
            clients.add(connection)
            return await connection.handle_client()
        finally:
            clients.remove(connection)

    async def _handle_shutdown(app: web.Application):
        for client in set(clients):
            await client.disconnect()

    server.app.on_shutdown.append(_handle_shutdown)
    server.app.router.add_route("GET", path, _handle_ws)


EventCallBackType = Callable[[EventType, Any], None]


class MatterServer:
    """Serve Matter stack over Websockets."""

    def __init__(self, storage_path: str, host: str, port: int) -> None:
        """Initialize the Matter Server."""
        self.host = host
        self.port = port
        self.logger = logging.getLogger(__name__)
        self.app = web.Application()
        self.loop: asyncio.AbstractEventLoop | None = None
        # Instantiate the Matter Stack using the SDK using the given storage path
        self.stack = MatterStack(storage_path)
        # Initialize our (intermediate) device controller which keeps track
        # of Matter devices and their subscriptions.
        self.device_controller = MatterDeviceController(self)
        self.storage = StorageController(storage_path)
        self._subscribers: Set[EventCallBackType] = set()

    async def start(self) -> None:
        """Start running the Matter server."""
        self.logger.info("Starting the Matter Server...")
        self.loop = asyncio.get_running_loop()
        await self.storage.start()
        await self.device_controller.start()
        mount_websocket(self, "/ws")
        self.app.router.add_route("GET", "/", self._handle_info)
        self._runner = web.AppRunner(self.app, access_log=None)
        await self._runner.setup()
        # set host to None to bind to all addresses on both IPv4 and IPv6
        self._http = web.TCPSite(self._runner, host=None, port=self.port)
        await self._http.start()
        self.logger.debug("Webserver initialized.")

    async def stop(self) -> None:
        """Stop running the server."""
        self.logger.info("Stopping the Matter Server...")
        self.signal_event(EventType.SERVER_SHUTDOWN)
        await self._http.stop()
        await self._runner.cleanup()
        await self.app.shutdown()
        await self.app.cleanup()
        await self.device_controller.stop()
        await self.storage.stop()
        self.stack.shutdown()
        self.logger.debug("Cleanup complete")

    @property
    def info(self) -> ServerInfo:
        """Return (version)info of the Matter Server."""
        return (
            ServerInfo(
                fabricId=self.device_controller.fabric_id,
                compressedFabricId=self.device_controller.compressed_fabric_id,
                version=VersionInfo(
                    # TODO: send correct versions here
                    sdk_version=0,
                    server_version=0,
                    min_schema_version=1,
                    max_schema_version=1,
                ),
            ),
        )

    def subscribe(self, callback: Callable[[EventType, Any], None]) -> None:
        """
        Subscribe to events.

        Returns handle to remove subscription.
        """

        def unsub():
            self._subscribers.remove(callback)

        self._subscribers.add(callback)

    def signal_event(self, evt: EventType, data: Any = None) -> None:
        """Signal event to listeners."""
        for callback in self._subscribers:
            if asyncio.iscoroutinefunction(callback):
                asyncio.create_task(callback(type, data))
            else:
                callback(type, data)

    async def _handle_info(self, request: web.Request) -> web.Response:
        """Handle info endpoiunt to serve basic server (version) info."""
        return web.json_response(self.info)
