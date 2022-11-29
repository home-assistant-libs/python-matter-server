"""Matter node."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import logging
from typing import TYPE_CHECKING, Dict

from chip.clusters import (
    Attribute,
    Cluster,
    ClusterAttributeDescriptor,
    ClusterEvent,
    ClusterObject,
    ClusterObjects,
    Objects as Clusters,
)

from ..helpers.util import dataclass_to_dict, dataclass_from_dict
from .device_type_instance import MatterDeviceTypeInstance
from .device_types import ALL_TYPES, Aggregator, BridgedDevice, RootNode
from .node_device import (
    AbstractMatterNodeDevice,
    MatterBridgedNodeDevice,
    MatterNodeDevice,
)

LOGGER = logging.getLogger(__name__)


@dataclass
class MatterNode:
    """Matter node."""

    node_id: int
    date_commissioned: datetime
    last_interview: datetime
    interview_version: int
    # attributes are stored in form of endpoint: {ClusterID: Cluster}
    attributes: Dict[int, Dict[int, Cluster]] = field(default_factory=dict)
    # attributes below will be auto derrived from the attributes
    # root_device_type_instance: MatterDeviceTypeInstance[RootNode] | None = None
    # aggregator_device_type_instance: MatterDeviceTypeInstance[Aggregator] | None = None
    # device_type_instances: list[MatterDeviceTypeInstance] = field(default_factory=list)
    # node_devices: list[AbstractMatterNodeDevice] = field(default_factory=list)

    @classmethod
    def from_dict(cls: "MatterNode", obj: dict) -> MatterNode:
        """Instantiate from plain dict."""
        return dataclass_from_dict(MatterNode, obj)

    def parse_attributes(self, attributes: dict) -> None:
        """Try to parse a MatterNode from AttributeCache (retrieved from Read)."""

        device_type_instances: list[MatterDeviceTypeInstance] = []

        for endpoint_id, clusters in attributes.items():
            for cluster_cls, cluster in clusters.items():

                if isinstance(cluster, Attribute.ValueDecodeFailure):
                    # yes, this may happen
                    continue

                # the python wrapped SDK has a funky way to index the Clusters by
                # having the class itself as dict key. We change that here to just the Cluster ID.
                self.attributes[cluster.id] = cluster

                # lookup device type for this cluster
                device_type = ALL_TYPES.get(cluster.id)

                if device_type is None:
                    LOGGER.warning("Found unknown device type for Cluster %s", cluster)
                    continue

                instance = MatterDeviceTypeInstance(
                    self, device_type, int(endpoint_id), cluster.clusterRevision
                )
                

    def parse_attributes_org(self, attributes: dict) -> None:
        """Try to parse a MatterNode from AttributeCache (retrieved from Read)."""

        device_type_instances: list[MatterDeviceTypeInstance] = []

        for endpoint_id, clusters in attributes.items():
            for cluster_cls, cluster in clusters.items():

                if isinstance(cluster, Attribute.ValueDecodeFailure):
                    # yes, this may happen
                    continue

                # the python wrapped SDK has a funky way to index the Clusters by
                # having the class itself as dict key. We change that here to just the Cluster ID.
                self.attributes[cluster.id] = cluster

                # lookup device type for this cluster
                device_type = ALL_TYPES.get(cluster.id)

                if device_type is None:
                    LOGGER.warning("Found unknown device type for Cluster %s", cluster)
                    continue

                instance = MatterDeviceTypeInstance(
                    self, device_type, int(endpoint_id), cluster.clusterRevision
                )
                if device_type is RootNode:
                    self.root_device_type_instance = instance
                elif device_type is Aggregator:
                    self.aggregator_device_type_instance = instance
                else:
                    device_type_instances.append(instance)

            self.device_type_instances = device_type_instances

            if not hasattr(self, "root_device_type_instance"):
                raise ValueError("No root device found")

            self.node_devices = []

            if self.aggregator_device_type_instance:
                for instance in device_type_instances:
                    if instance.device_type == BridgedDevice:
                        self.node_devices.append(MatterBridgedNodeDevice(instance))

            else:
                self.node_devices.append(MatterNodeDevice(self))

    @property
    def name(self) -> str:
        return self.root_device_type_instance.get_cluster(Clusters.Basic).nodeLabel

    @property
    def unique_id(self) -> str:
        return self.root_device_type_instance.get_cluster(Clusters.Basic).uniqueID

    def __repr__(self):
        return f"<MatterNode {self.node_id}>"
