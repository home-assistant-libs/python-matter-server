"""Node Device represent the actual devices available on a node.


"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from matter_server.vendor import device_types
from matter_server.vendor.chip.clusters import Objects as all_clusters

if TYPE_CHECKING:
    from .device_type_instance import MatterDeviceTypeInstance
    from .node import MatterNode


class AbstractMatterNodeDevice(ABC):
    """Device that can be mapped."""

    @abstractmethod
    def node(self) -> MatterNode:
        """Return the node of this device."""

    @abstractmethod
    def device_info(self) -> all_clusters.Basic | all_clusters.BridgedDeviceBasic:
        """Return device info."""

    @abstractmethod
    def device_type_instances(self) -> list[MatterDeviceTypeInstance]:
        """Return Matter device type instances."""


class MatterNodeDevice(AbstractMatterNodeDevice):
    """Device that is the whole node."""

    def __init__(self, node: MatterNode) -> None:
        self._node = node

    def node(self) -> MatterNode:
        return self._node

    def device_info(self) -> all_clusters.Basic:
        return self._node.root_device_type_instance.get_cluster(all_clusters.Basic)

    def device_type_instances(self) -> list[MatterDeviceTypeInstance]:
        return self._node.device_type_instances

    def __repr__(self) -> str:
        return f"<MatterNodeDevice (N:{self._node.node_id})>"


class MatterBridgedNodeDevice(AbstractMatterNodeDevice):
    """Device that is based on a bridged device on a node."""

    def __init__(
        self,
        bridged_device_type_instance: MatterDeviceTypeInstance[
            device_types.BridgedDevice
        ],
    ) -> None:
        self.bridged_device_type_instance = bridged_device_type_instance

    def node(self) -> MatterNode:
        return self.bridged_device_type_instance.node

    def device_info(self) -> all_clusters.BridgedDeviceBasic:
        return self.bridged_device_type_instance.get_cluster(
            all_clusters.BridgedDeviceBasic
        )

    def device_type_instances(self) -> list[MatterDeviceTypeInstance]:
        endpoint_id = self.bridged_device_type_instance.endpoint_id
        return [
            inst
            for inst in self.bridged_device_type_instance.node.device_type_instances
            if inst.endpoint_id == endpoint_id
            and inst != self.bridged_device_type_instance
        ]

    def __repr__(self) -> str:
        bridged = self.bridged_device_type_instance
        return f"<MatterBridgedNodeDevice (N:{bridged.node.node_id}, E:{bridged.endpoint_id})>"
