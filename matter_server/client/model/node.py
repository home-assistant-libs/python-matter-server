"""Matter node."""
from __future__ import annotations

from typing import TYPE_CHECKING

from matter_server.vendor import device_types
from matter_server.vendor.chip.clusters import Objects as all_clusters

from .device_type_instance import MatterDeviceTypeInstance

if TYPE_CHECKING:
    from ..matter import Matter


class MatterNode:
    """Matter node."""

    root_device_type_instance: MatterDeviceTypeInstance[device_types.RootNode]

    def __init__(self, matter: Matter, node_info: dict) -> None:
        self.matter = matter
        self.raw_data = node_info

        device_type_instances: list[MatterDeviceTypeInstance] = []

        for endpoint_id, endpoint_info in node_info["attributes"].items():
            descriptor: all_clusters.Descriptor = endpoint_info["Descriptor"]
            for device_info in descriptor.deviceList:
                device_type = device_types.ALL_TYPES.get(device_info.type)

                if device_type is None:
                    matter.adapter.logger.warning(
                        "Found unknown device type %s", device_info.type
                    )
                    continue

                instance = MatterDeviceTypeInstance(
                    self, device_type, int(endpoint_id), device_info.revision
                )
                if device_type is device_types.RootNode:
                    self.root_device_type_instance = instance
                else:
                    device_type_instances.append(instance)

        self.device_type_instances = device_type_instances

        if not hasattr(self, "root_device_type_instance"):
            raise ValueError("No root device found")

    @property
    def node_id(self) -> int:
        return self.raw_data["node_id"]

    @property
    def name(self) -> str:
        return self.root_device_type_instance.get_cluster(all_clusters.Basic).nodeLabel

    @property
    def unique_id(self) -> str:
        return self.root_device_type_instance.get_cluster(all_clusters.Basic).uniqueID

    def update_data(self, node_info):
        self.raw_data = node_info

    def __repr__(self):
        return f"<MatterNode {self.node_id}>"
