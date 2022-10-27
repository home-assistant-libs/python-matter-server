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

from matter_server.common.model.server_information import ServerInfo, VersionInfo
from matter_server.server.client_handler import WebsocketClientHandler

from ..common.json_utils import CHIPJSONDecoder, CHIPJSONEncoder
from ..common.model.message import CommandMessage, EventType

if TYPE_CHECKING:
    from .server import MatterServer
    from .stack import MatterStack


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

    def __init__(self, stack: MatterStack) -> None:
        self.stack = stack
        self.logger = logging.getLogger(__name__)
        self.app = web.Application()
        self.loop = asyncio.get_running_loop()
        self._subscribers: Set[EventCallBackType] = set()
        self.app.router.add_route("GET", "/info", self._handle_info)
        mount_websocket(self, "/ws")

    def run(self, host: str, port: int) -> None:
        """Run the websocket server."""
        web.run_app(self.app, host=host, port=port, loop=self.loop)

    @property
    def info(self) -> ServerInfo:
        """Return (version)info of the Matter Server."""
        return (
            ServerInfo(
                fabricId=self.stack.fabric_id,
                compressedFabricId=self.stack.compressed_fabric_id,
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
