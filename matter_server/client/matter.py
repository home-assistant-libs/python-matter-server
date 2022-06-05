"""Matter base class."""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from matter_server.common.json_utils import asdict_typed

from .client import Client
from .exceptions import BaseMatterServerError, FailedCommand
from .model.node import MatterNode

if TYPE_CHECKING:
    from .adapter import AbstractMatterAdapter


class Matter:

    next_node_id: int
    _nodes: dict[int, MatterNode | None]

    def __init__(
        self,
        adapter: AbstractMatterAdapter,
    ):
        self.adapter = adapter
        self.client = Client(adapter.get_server_url(), adapter.get_client_session())
        self.driver_ready = asyncio.Event()
        self._listen_task = None
        self._handle_driver_ready_task = None
        self._commission_lock = asyncio.Lock()

    def get_node(self, node_id: int) -> MatterNode:
        """Get a node."""
        node = self._nodes[node_id]
        if node is None:
            raise ValueError(f"Node {node_id} not interviewed")
        return node

    def get_nodes(self) -> list[MatterNode]:
        """Get nodes."""
        # node is None if not interviewed
        return [node for node in self._nodes.values() if node]

    async def connect(self):
        """Connect to the server."""
        data = await self.adapter.load_data()

        if data is None:
            data = {"next_node_id": 4335, "nodes": {}}

        self.next_node_id = data["next_node_id"]
        # JSON stores dictionary keys as strings, convert to int
        self._nodes = {
            int(node_id): MatterNode(self, node_info) if node_info else None
            for node_id, node_info in data["nodes"].items()
        }

        await self.client.connect()

        # TODO verify server is same fabric ID or else reset storage.
        # expected_fabric_id = ...

    async def disconnect(self):
        """Disconnect from the server."""
        self._listen_task.cancel()
        await self._listen_task

    async def commission(self, code: str):
        """Commission a new device."""
        async with self._commission_lock:
            node_id = self.next_node_id
            await self.client.driver.device_controller.commission_with_code(
                code, node_id
            )
            self._nodes[node_id] = None
            self.next_node_id += 1
            # Save right away because we don't want to lose node IDs
            await self.adapter.save_data(self._data_to_save())

        await self._interview_node(node_id)

    async def delete_node(self, node_id: int) -> None:
        """Delete a node."""
        # TODO notify anyone using MatterNode
        # TODO can we factory reset node_id so it can be commissioned again?
        self._nodes.pop(node_id)
        self.adapter.delay_save_data(self._data_to_save)

    async def _interview_node(self, node_id: int) -> None:
        """Interview a node."""
        self.adapter.logger.info("Interviewing node %s", node_id)
        try:
            await self.client.driver.device_controller.resolve_node(node_id)
            node_info = await self.client.driver.device_controller.read(
                node_id, attributes="*", events="*", returnClusterObject=True
            )
        except FailedCommand as err:
            self.adapter.logger.error("Failed to interview node: %s", err)
            return

        node_info["node_id"] = node_id

        if self._nodes[node_id]:
            self._nodes[node_id].update_data(node_info)
        else:
            self._nodes[node_id] = MatterNode(self, node_info)

        self.adapter.delay_save_data(self._data_to_save)

        await self.adapter.setup_node(self._nodes[node_id])

    def listen(self):
        """Start listening to changes."""
        self._listen_task = asyncio.create_task(self._client_listen())
        self._handle_driver_ready_task = asyncio.create_task(
            self._handle_driver_ready()
        )

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

        self._handle_driver_ready_task.cancel()

        await self.adapter.handle_server_disconnected(should_reload)

    async def _handle_driver_ready(self) -> None:
        """Handle driver ready."""
        await self.driver_ready.wait()
        tasks = [self.adapter.setup_node(node) for node in self.get_nodes()]

        if tasks:
            await asyncio.gather(*tasks)

        to_interview = [
            node_id for node_id, info in self._nodes.items() if info is None
        ]
        if not to_interview:
            return

        self.adapter.logger.info("Nodes that still need interviewing: %s", to_interview)

        for node_id in to_interview:
            await self._interview_node(node_id)

    def _data_to_save(self) -> dict:
        return {
            "next_node_id": self.next_node_id,
            "nodes": {
                node_id: node.raw_data if node else None
                for node_id, node in self._nodes.items()
            },
        }
