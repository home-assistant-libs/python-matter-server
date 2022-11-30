"""Matter node."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import inspect
import logging
from typing import TYPE_CHECKING, Any, Dict, TypeVar

from chip.clusters import (
    Attribute,
    Cluster,
    ClusterAttributeDescriptor,
    ClusterEvent,
    ClusterObject,
    ClusterObjects,
    Objects as Clusters,
)
from .device_type_instance import MatterDeviceTypeInstance
from .device_types import ALL_TYPES as DEVICE_TYPES, Aggregator, BridgedDevice, RootNode
from .node_device import (
    AbstractMatterNodeDevice,
    MatterBridgedNodeDevice,
    MatterNodeDevice,
)

LOGGER = logging.getLogger(__name__)

_CLUSTER_T = TypeVar("_CLUSTER_T", bound=Clusters.Cluster)


def create_attribute_path(endpoint: int, cluster_id: int, attribute_id: int) -> str:
    """
    Create path/identifier for an Attribute.

    Returns same output as `Attribute.AttributePath`
    endpoint/cluster_id/attribute_id
    """
    return f"{endpoint}/{cluster_id}/{attribute_id}"


@dataclass
class MatterAttribute:
    """Matter Attribute."""

    node_id: int
    endpoint: int
    cluster_id: int
    cluster_type: type
    cluster_name: str
    attribute_id: int
    attribute_type: type
    attribute_name: str
    value: Any

    @property
    def name(self) -> str:
        """Return full name for this Attribute."""
        return f"{self.cluster_name}.{self.attribute_name}"

    @property
    def path(self) -> str:
        """Return path/key for this attribute."""
        return create_attribute_path(self.endpoint, self.cluster_id, self.attribute_id)

    def __post_init__(self):
        """Initialize optional values after init."""


@dataclass
class MatterNode:
    """Matter node."""

    node_id: int
    date_commissioned: datetime
    last_interview: datetime
    interview_version: int
    # attributes are stored in form of AttributeKey: MatterAttribute
    attributes: Dict[str, MatterAttribute]
    # below attributes are derrived from the attributes in post init.
    endpoints: list[int] = field(default_factory=list, init=False)
    root_device_type_instance: MatterDeviceTypeInstance[RootNode] | None = field(
        default=None, init=False
    )
    aggregator_device_type_instance: MatterDeviceTypeInstance[
        Aggregator
    ] | None = field(default=None, init=False)
    device_type_instances: list[MatterDeviceTypeInstance] = field(
        default_factory=list, init=False
    )
    node_devices: list[AbstractMatterNodeDevice] = field(
        default_factory=list, init=False
    )

    def __post_init__(self):
        """Initialize optional values after init."""
        device_type_instances: list[MatterDeviceTypeInstance] = []
        for attr_path, attr in self.attributes.items():
            if attr.endpoint not in self.endpoints:
                self.endpoints.append(attr.endpoint)
            if attr.attribute_type != Clusters.Descriptor.Attributes.DeviceTypeList:
                continue
            for dev_info in attr.value:
                if not isinstance(
                    dev_info, Clusters.Descriptor.Structs.DeviceTypeStruct
                ):
                    dev_info = Clusters.Descriptor.Structs.DeviceTypeStruct(**dev_info)
                device_type = DEVICE_TYPES.get(dev_info.type)
                if device_type is None:
                    LOGGER("Found unknown device type %s", dev_info)
                    continue

                instance = MatterDeviceTypeInstance(
                    self, device_type, attr.endpoint, dev_info.revision
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

    def get_endpoint_attributes(self, endpoint: int) -> list[MatterAttribute]:
        """Return Matter Attributes for given endpoint."""
        return [x for x in self.attributes.values() if x.endpoint == endpoint]

    def get_cluster_attributes(
        self, endpoint: int, cluster: type[Clusters.Cluster] | int
    ) -> list[MatterAttribute]:
        """Return all Attributes for given cluster."""
        return [
            x
            for x in self.attributes.values()
            if cluster in (x.cluster_type, x.cluster_id) and x.endpoint == endpoint
        ]

    def get_attribute(
        self,
        endpoint: int,
        cluster: type[Clusters.Cluster],
        attribute: str | int | type,
    ) -> MatterAttribute:
        """Return Matter Attribute for given parameters."""
        return next(
            x
            for x in self.attributes.values()
            if x.cluster_type == cluster
            and x.endpoint == endpoint
            and attribute in (x.attribute_id, x.attribute_name, x.attribute_type)
        )

    def has_cluster(self, endpoint: int, cluster: type[Cluster] | int) -> bool:
        """Check if node has a specific cluster."""
        return any(
            x
            for x in self.attributes.values()
            if cluster in (x.cluster_type, x.cluster_id)
            and (endpoint is None or x.endpoint == endpoint)
        )

    def get_cluster(
        self, endpoint: int, cluster: type[_CLUSTER_T]
    ) -> _CLUSTER_T | None:
        """
        Get a full Cluster object containing all attributes.

        Returns None is the Cluster is not present on the node.
        """
        atrributes = self.get_cluster_attributes(endpoint, cluster)
        if len(atrributes) == 0:
            return None

        # instantiate a Cluster object from the properties
        return cluster(**{x.attribute_name: x.value for x in atrributes})

    @property
    def name(self) -> str:
        """Return friendly name for this node."""
        return self.get_attribute(
            self.root_device_type_instance.endpoint, Clusters.Basic, "nodeLabel"
        )

    @property
    def unique_id(self) -> str:
        """Return uniqueID for this node."""
        return self.get_attribute(
            self.root_device_type_instance.endpoint, Clusters.Basic, "uniqueID"
        )

    def __repr__(self):
        return f"<MatterNode {self.node_id}>"
