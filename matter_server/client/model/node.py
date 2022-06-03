"""Matter node."""
from __future__ import annotations

from typing import TYPE_CHECKING

from matter_server.vendor.chip.clusters.Objects import Descriptor

from .device import DEVICE_TYPES, MatterDevice

if TYPE_CHECKING:
    from ..matter import Matter


class MatterNode:
    """Matter node."""

    root_device: MatterDevice

    def __init__(self, matter: Matter, node_info: dict) -> None:
        self.matter = matter
        self.raw_data = node_info

        devices: list[MatterDevice] = []

        for endpoint_id, endpoint_info in node_info["attributes"].items():
            descriptor: Descriptor = endpoint_info["Descriptor"]
            for device_info in descriptor.deviceList:
                device_cls = DEVICE_TYPES.get(device_info.type)

                if device_cls is None:
                    matter.adapter.logger.warning(
                        "Found unknown device type %s", device_info.type
                    )
                    continue

                device = device_cls(self, int(endpoint_id), device_info.revision)
                if device.device_type == 22:
                    self.root_device = device
                else:
                    devices.append(device)

        self.devices = devices

        if not hasattr(self, "root_device"):
            raise ValueError("No root device found")

    @property
    def node_id(self) -> int:
        return self.raw_data["node_id"]

    @property
    def name(self) -> str:
        return self.root_device.name

    @property
    def unique_id(self) -> str:
        return self.root_device.unique_id

    def update_data(self, node_info):
        self.raw_data = node_info

    def __repr__(self):
        return f"<MatterNode {self.node_id}>"
