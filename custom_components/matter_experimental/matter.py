"""Matter base class."""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from homeassistant.core import callback

from matter_server.client.client import Client
from matter_server.client.exceptions import BaseMatterServerError, FailedCommand

if TYPE_CHECKING:
    from .adapter import AbstractMatterAdapter

from .node import MatterNode


class Matter:
    def __init__(
        self,
        adapter: AbstractMatterAdapter,
    ):
        self.adapter = adapter
        self.client = Client(adapter.get_server_url(), adapter.get_client_session())
        self.driver_ready = asyncio.Event()
        self._listen_task = None
        self._commission_lock = asyncio.Lock()

    def get_node(self, node_id: int) -> MatterNode:
        """Get a node."""
        node = self.adapter.get_storage().nodes[node_id]
        if node is None:
            raise ValueError(f"Node {node_id} not interviewed")
        return node

    def get_nodes(self) -> list[MatterNode]:
        """Get nodes."""
        # node is None if not interviewed
        return [node for node in self.adapter.get_storage().nodes.values() if node]

    async def connect(self):
        """Connect to the server."""
        await self.client.connect()

        # TODO verify server is same fabric ID or else reset storage.
        # expected_fabric_id = ...

        await self.adapter.get_storage().async_initialize()

    async def disconnect(self):
        """Disconnect from the server."""
        self._listen_task.cancel()
        await self._listen_task

    async def commission(self, code: str) -> None:
        """Commission a new device."""
        async with self._commission_lock:
            node_id = self.adapter.get_storage().next_node_id
            await self.client.driver.device_controller.CommissionWithCode(code, node_id)
            await self.adapter.get_storage().register_node()

        await self._interview_node(node_id)

    async def finish_pending_work(self) -> None:
        """Finish pending work."""
        to_interview = [
            node_id
            for node_id, info in self.adapter.get_storage().nodes.items()
            if info is None
        ]
        if not to_interview:
            return

        self.adapter.logger.info("Nodes that still need interviewing: %s", to_interview)

        for node_id in to_interview:
            await self._interview_node(node_id)

    async def _interview_node(self, node_id: int) -> None:
        """Interview a node."""
        self.adapter.logger.info("Interviewing node %s", node_id)
        try:
            node_info = await self.client.driver.device_controller.Read(
                node_id, attributes="*", events="*", returnClusterObject=True
            )
        except FailedCommand as err:
            self.adapter.logger.error("Failed to interview node: %s", err)
            return

        node = self.adapter.get_storage().update_node(node_id, node_info)
        await self.adapter.setup_node(node)

    @callback
    def listen(self):
        """Start listening to changes."""
        self._listen_task = asyncio.create_task(self._client_listen())

    async def _client_listen(self) -> None:
        """Listen with the client."""
        should_reload = True
        try:
            await self.client.listen(self.driver_ready)
        except asyncio.CancelledError:
            should_reload = False
        except BaseMatterServerError as err:
            self.adapter.logger.error("Failed to listen: %s", err)
        except Exception as err:  # pylint: disable=broad-except
            # We need to guard against unknown exceptions to not crash this task.
            self.adapter.logger.exception("Unexpected exception: %s", err)

        await self.adapter.handle_server_disconnected(should_reload)
