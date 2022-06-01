from __future__ import annotations
from typing import TYPE_CHECKING, Any

from matter_server.vendor.chip.clusters import Objects as Clusters

if TYPE_CHECKING:
    from .node import MatterNode

DEVICE_TYPES = {}


class MatterDevice:
    """Base class for Matter devices."""

    device_type: int

    def __init_subclass__(cls, *, device_type: int, **kwargs: Any) -> None:
        """Initialize a subclass, register if possible."""
        super().__init_subclass__(**kwargs)
        cls.device_type = device_type
        DEVICE_TYPES[device_type] = cls

    def __init__(
        self, node: MatterNode, endpoint_id: int, device_revision: int
    ) -> None:
        self.node = node
        self.device_revision = device_revision
        self.endpoint_id = endpoint_id

    @property
    def data(self) -> dict:
        return self.node.raw_data["attributes"][str(self.endpoint_id)]

    async def send_command(
        self,
        payload: Clusters.ClusterCommand,
        responseType=None,
        timedRequestTimeoutMs: int = None,
    ):
        """Send a command to the device."""
        return await self.node.matter.client.driver.device_controller.SendCommand(
            nodeid=self.node.node_id,
            endpoint=self.endpoint_id,
            payload=payload,
            responseType=responseType,
            timedRequestTimeoutMs=timedRequestTimeoutMs,
        )


class RootDevice(MatterDevice, device_type=22):
    """Root device."""

    @property
    def name(self) -> str:
        return self.basic_info["nodeLabel"]

    @property
    def unique_id(self) -> str:
        return self.basic_info["uniqueID"]

    @property
    def basic_info(self) -> dict:
        return self.data["Basic"]


class OnOffLight(MatterDevice, device_type=256):
    """On/Off light."""


class DimmableLight(MatterDevice, device_type=257):
    """Dimmable light."""
