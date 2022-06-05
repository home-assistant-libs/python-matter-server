from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from aiohttp import web

from .websocket import mount_websocket

if TYPE_CHECKING:
    from .matter_stack import MatterStack


class MatterServer:
    """Serve Matter over WS."""

    def __init__(self, stack: MatterStack):
        self.stack = stack
        self.logger = logging.getLogger(__name__)
        self.app = web.Application()
        self.loop = asyncio.get_running_loop()
        mount_websocket(self, "/chip_ws")

    def run(self, host, port):
        """Run the server."""
        web.run_app(self.app, host=host, port=port, loop=self.loop)
