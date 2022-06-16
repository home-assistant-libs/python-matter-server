"""Matter base class."""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Callable

from .client import Client
from .exceptions import BaseMatterServerError, FailedCommand
from .model.node import MatterNode

if TYPE_CHECKING:
    from .adapter import AbstractMatterAdapter


INTERVIEW_RETRY_TIME = 60  # seconds


class Matter:

    next_node_id: int
    _nodes: dict[int, MatterNode | None]
    _listen_task: asyncio.Task | None = None
    _handle_driver_ready_task: asyncio.Task | None = None
    _reinterview_unsub: Callable[[], None] | None = None
    _reinterview_nodes: set[int] | None = None
    _commission_lock: asyncio.Lock | None = None

    def __init__(
        self,
        adapter: AbstractMatterAdapter,
    ):
        self.adapter = adapter
        self.client = Client(adapter.get_server_url(), adapter.get_client_session())
        self.driver_ready = asyncio.Event()

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
        await self.client.connect()

        data = await self.adapter.load_data()

        if (
            data
            and data.get("compressed_fabric_id")
            != self.client.server_info.compressedFabricId
        ):
            self.adapter.logger.warning(
                "Connected to a server with a new fabric ID (current: %s, server: %s). Resetting data",
                data.get("compressed_fabric_id"),
                self.client.server_info.compressedFabricId,
            )
            data = None
            # TODO can we detect all known nodes to the server and interview them?

        if data is None:
            data = {"next_node_id": 4335, "nodes": {}}

        self.next_node_id = data["next_node_id"]
        # JSON stores dictionary keys as strings, convert to int
        self._nodes = {
            int(node_id): MatterNode(self, node_info) if node_info else None
            for node_id, node_info in data["nodes"].items()
        }

    async def disconnect(self):
        """Disconnect from the server."""
        self._listen_task.cancel()
        await self._listen_task

    async def commission(self, code: str):
        """Commission a new device."""
        if self._commission_lock is None:
            self._commission_lock = asyncio.Lock()

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
            self._schedule_interview_retry({node_id})
            return

        node_info["node_id"] = node_id

        if self._nodes[node_id]:
            self._nodes[node_id].update_data(node_info)
        else:
            self._nodes[node_id] = MatterNode(self, node_info)

        self.adapter.delay_save_data(self._data_to_save)

        try:
            await self.adapter.setup_node(self._nodes[node_id])
        except Exception:  # pylint: disable=broad-except
            self.adapter.logger.exception(
                "Unexptected error setting up node %s", node_id
            )

    def _schedule_interview_retry(self, nodes: set[int], timeout=INTERVIEW_RETRY_TIME):
        """Schedule a retry of failed nodes."""
        if self._reinterview_unsub is None:
            loop = asyncio.get_running_loop()
            self._reinterview_unsub = loop.call_later(
                timeout, lambda: loop.create_task(self._interview_nodes_retry())
            ).cancel

        if self._reinterview_nodes is None:
            self._reinterview_nodes = nodes
        else:
            self._reinterview_nodes |= nodes

    async def _interview_nodes_retry(self) -> None:
        """Retry failed nodes."""
        # Keep track of tried to guard re-interviewing the same node
        tried: set[int] = set()
        assert isinstance(self._reinterview_nodes, set)

        while to_handle := self._reinterview_nodes - tried:
            node_id = to_handle.pop()
            tried.add(node_id)
            await self._interview_node(node_id)
            self._reinterview_nodes.discard(node_id)

        self._reinterview_unsub = None

        if self._reinterview_nodes:
            self._schedule_interview_retry(self._reinterview_nodes)
        else:
            self._reinterview_nodes = None

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
        nodes = self.get_nodes()
        tasks = [self.adapter.setup_node(node) for node in nodes]

        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for node, result in zip(nodes, results):
                if isinstance(result, Exception):
                    self.adapter.logger.error(
                        "Unexpected error setting up node %s",
                        node.node_id,
                        exc_info=result,
                    )

        to_interview = {
            node_id for node_id, info in self._nodes.items() if info is None
        }
        if not to_interview:
            return

        self.adapter.logger.info("Nodes that still need interviewing: %s", to_interview)
        self._schedule_interview_retry(to_interview, 0)

    def _data_to_save(self) -> dict:
        return {
            "compressed_fabric_id": self.client.server_info.compressedFabricId,
            "next_node_id": self.next_node_id,
            "nodes": {
                node_id: node.raw_data if node else None
                for node_id, node in self._nodes.items()
            },
        }
