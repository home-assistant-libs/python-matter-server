from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING
import weakref

from aiohttp import web

from .active_connection import ActiveConnection

if TYPE_CHECKING:
    from .matter_stack import MatterStack


class MatterServer:
    """Serve Matter over WS."""

    def __init__(self, stack: MatterStack):
        self.stack = stack
        self.logger = logging.getLogger(__name__)
        self.app = web.Application()
        self.loop = asyncio.get_running_loop()
        self.clients = weakref.WeakSet()
        self.app.on_shutdown.append(self._handle_shutdown)

        self.app.router.add_route("GET", "/chip_ws", self._handle_chip_ws)

    async def _handle_chip_ws(self, request):
        connection = ActiveConnection(self, request)
        try:
            self.clients.add(connection)
            return await connection.handle_request()
        finally:
            self.clients.remove(connection)

    async def _handle_shutdown(self, app):
        for client in set(self.clients):
            await client.disconnect()

    def run(self, host, port):
        """Run the server."""
        web.run_app(self.app, host=host, port=port, loop=self.loop)
