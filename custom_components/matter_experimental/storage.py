"""Storage for Matter."""
from __future__ import annotations

from homeassistant.core import callback
from homeassistant.helpers.storage import Store

from .const import DOMAIN
from .node import MatterNode

STORAGE_MAJOR_VERSION = 1
STORAGE_MINOR_VERSION = 0


class MatterStorage:
    """Storage for Matter devices."""

    data: dict

    def __init__(self, hass):
        self._store = Store(
            hass,
            STORAGE_MAJOR_VERSION,
            DOMAIN,
            minor_version=STORAGE_MINOR_VERSION,
        )

    async def async_initialize(self):
        """Initialize the store."""
        self.data = await self._store.async_load()

        if self.data is None:
            self.data = {
                "next_node_id": 4335,
                "nodes": {},
            }
        else:
            # JSON stores dictionary keys as strings, convert to int
            self.data["nodes"] = {
                int(node_id): MatterNode(node_info) if node_info else None
                for node_id, node_info in self.data["nodes"].items()
            }

    @property
    def nodes(self):
        return self.data["nodes"]

    @property
    def next_node_id(self):
        return self.data["next_node_id"]

    async def register_node(self) -> None:
        """Register a node. Assumes it was registerd under next_node_id."""
        self.data["nodes"][self.next_node_id] = None
        self.data["next_node_id"] += 1
        # Save right away because we don't want to lose node IDs
        await self._store.async_save(self._data_to_save())

    @callback
    def update_node(self, node_id: int, data: dict):
        """Update a node."""
        data["node_id"] = node_id
        if self.data["nodes"][node_id]:
            self.data["nodes"][node_id].update_data(data)
        else:
            self.data["nodes"][node_id] = MatterNode(data)

        self._delay_save_data()

        return self.data["nodes"][node_id]

    @callback
    def delete_node(self, node_id: int) -> None:
        """Delete a node."""
        self.data["nodes"].pop(node_id)
        self._delay_save_data()

    @callback
    def _delay_save_data(self) -> None:
        self._store.async_delay_save(self._data_to_save, 60)

    def _data_to_save(self) -> dict:
        data = dict(self.data)
        data["nodes"] = {
            node_id: node.raw_data if node else None
            for node_id, node in data["nodes"].items()
        }
        return data
