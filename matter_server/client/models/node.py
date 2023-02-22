"""Matter node."""
from __future__ import annotations

import logging
from typing import Any, TypeVar, cast

from chip.clusters import Objects as Clusters
from chip.clusters.ClusterObjects import ALL_ATTRIBUTES, ALL_CLUSTERS

from matter_server.common.helpers.util import parse_attribute_path, parse_value
from matter_server.common.models import MatterNodeData

from .device_type_instance import MatterDeviceTypeInstance
from .device_types import ALL_TYPES as DEVICE_TYPES, Aggregator, BridgedDevice, RootNode
from .node_device import (
    AbstractMatterNodeDevice,
    MatterBridgedNodeDevice,
    MatterNodeDevice,
)

LOGGER = logging.getLogger(__name__)

# pylint: disable=invalid-name
_CLUSTER_T = TypeVar("_CLUSTER_T", bound=Clusters.Cluster)
_ATTRIBUTE_T = TypeVar("_ATTRIBUTE_T", bound=Clusters.ClusterAttributeDescriptor)
# pylint: enable=invalid-name


def get_object_params(
    descriptor: Clusters.ClusterObjectDescriptor, object_id: int
) -> tuple[str, type]:
    """Parse label/key and type for an object from the descriptors, given the raw object id."""
    for desc in descriptor.Fields:
        if desc.Tag == object_id:
            return (desc.Label, desc.Type)
    return KeyError(f"No descriptor found for object {object_id}")


class MatterEndpoint:
    """Representation of a Matter Endpoint."""

    def __init__(
        self,
        endpoint_id: int,
        attributes_data: dict[str, Any],
        node: MatterNode,
    ) -> None:
        """Initialize MatterEndpoint."""
        self.node = node
        self.endpoint_id = endpoint_id
        self.clusters: dict[int, Clusters.Cluster] = {}
        # unwrap cluster and clusterattributes from raw node data attributes
        for attribute_path, attribute_value in attributes_data.items():
            self.set_attribute_value(attribute_path, attribute_value)

    def has_cluster(self, cluster: type[_CLUSTER_T] | int) -> bool:
        """Check if endpoint has a specific cluster."""
        if isinstance(cluster, type):
            return cluster.id in self.clusters
        return cluster in self.clusters

    def get_cluster(self, cluster: type[_CLUSTER_T] | int) -> _CLUSTER_T | None:
        """
        Get a full Cluster object containing all attributes.

        Return None if the Cluster is not present on the node.
        """
        if isinstance(cluster, type):
            return self.clusters[cluster.id]
        return self.clusters[cluster]

    def get_attribute_value(
        self,
        cluster: type[_CLUSTER_T] | int | None,
        attribute: int | type[_ATTRIBUTE_T],
    ) -> type[_ATTRIBUTE_T] | Clusters.ClusterAttributeDescriptor | None:
        """
        Return Matter Cluster Attribute object for given parameters.

        Send cluster as None to derive it from the Attribute.
        """
        if cluster is None:
            # allow sending None for Cluster to auto resolve it from the Attribute
            if isinstance(attribute, int):
                # get cluster from attribute
                cluster = ALL_ATTRIBUTES[attribute].cluster_id
            else:
                cluster = attribute.cluster_id
        # get cluster first, grab value from cluster instance next
        if cluster_obj := self.get_cluster(cluster):
            if isinstance(attribute, type):
                attribute_name, _ = get_object_params(
                    cluster_obj.descriptor, attribute.attribute_id
                )
                return getattr(cluster_obj, attribute_name)
            # actual value is just a class attribute on the cluster instance
            # NOTE: do not use the value on the ClusterAttribute
            # instance itself as that is not used!
            attribute_name, _ = get_object_params(cluster_obj.descriptor, attribute)
            return getattr(
                cluster_obj,
                attribute_name,
            )
        return None

    def set_attribute_value(self, attribute_path: str, attribute_value: Any) -> None:
        """
        Set the value of a Cluster Attribute.

        May only be called by logic that received data from the server.
        Do not modify the data directly from a consumer.
        """
        _, cluster_id, attribute_id = parse_attribute_path(attribute_path)
        cluster_class: Clusters.Cluster = ALL_CLUSTERS[cluster_id]
        if cluster_id in self.clusters:
            cluster_instance = self.clusters[cluster_id]
        else:
            cluster_instance = cluster_class()
            self.clusters[cluster_id] = cluster_instance

        # unpack cluster attribute, using the descriptor
        attribute_class: Clusters.ClusterAttributeDescriptor = ALL_ATTRIBUTES[
            cluster_id
        ][attribute_id]
        attribute_name, attribute_type = get_object_params(
            cluster_class.descriptor, attribute_id
        )

        # we only set the value at cluster instance level and we leave
        # the underlying Attributes classproperty alone
        attribute_value = parse_value(
            attribute_name, attribute_value, attribute_type, attribute_class().value
        )
        setattr(cluster_instance, attribute_name, attribute_value)


class MatterNode:
    """Representation of a Matter Node."""

    def __init__(self, node_data: MatterNodeData) -> None:
        """Initialize MatterNode from MatterNodeData."""
        self.endpoints: dict[int, MatterEndpoint] = {}
        self.root_device_type_instance: MatterDeviceTypeInstance[RootNode] | None = None
        self.aggregator_device_type_instance: MatterDeviceTypeInstance[
            Aggregator
        ] | None = None
        self.node_devices: list[AbstractMatterNodeDevice] = []
        self.device_type_instances: list[MatterDeviceTypeInstance] = []
        self.update(node_data)

    def update(self, node_data: MatterNodeData) -> None:
        """Update MatterNode from MatterNodeData."""
        # pylint: disable=too-many-branches
        self.node_data = node_data
        # collect per endpoint data
        endpoint_data: dict[int, dict[str, Any]] = {}
        for attribute_path, attribute_data in node_data.attributes.items():
            endpoint_id = int(attribute_path.split("/")[0])
            endpoint_data.setdefault(endpoint_id, {})
            endpoint_data[endpoint_id][attribute_path] = attribute_data
        # TODO: Should we update existing endpoints instead of overwriting them?
        for endpoint_id, attributes_data in endpoint_data.items():
            self.endpoints[endpoint_id] = MatterEndpoint(
                endpoint_id=endpoint_id, attributes_data=attributes_data, node=self
            )
        # lookup device types from node data
        for endpoint in self.endpoints.values():
            # get DeviceTypeList Attribute on the Descriptor cluster
            cluster = endpoint.get_cluster(Clusters.Descriptor)
            for dev_info in cluster.deviceTypeList:
                device_type = DEVICE_TYPES.get(dev_info.type)
                if device_type is None:
                    LOGGER.debug("Found unknown device type %s", dev_info)
                    continue

                instance: MatterDeviceTypeInstance[Any] = MatterDeviceTypeInstance(
                    self, device_type, endpoint, dev_info.revision
                )
                if device_type is RootNode:
                    self.root_device_type_instance = instance
                elif device_type is Aggregator:
                    self.aggregator_device_type_instance = instance
                else:
                    self.device_type_instances.append(instance)

        if self.root_device_type_instance is None:
            raise ValueError("No root device found")

        # parse node devices
        self.node_devices = []
        if self.aggregator_device_type_instance:
            for instance in self.device_type_instances:
                if instance.device_type == BridgedDevice:
                    self.node_devices.append(MatterBridgedNodeDevice(instance))
        else:
            self.node_devices.append(MatterNodeDevice(self))

    def update_attribute(self, attribute_path: str, new_value: Any) -> None:
        """Handle Attribute value update."""
        endpoint_id = int(attribute_path.split("/")[0])
        self.endpoints[endpoint_id].set_attribute_value(attribute_path, new_value)

    @property
    def node_id(self) -> int:
        """Return Node ID."""
        return self.node_data.node_id

    @property
    def available(self) -> bool:
        """Return availability of the node."""
        return self.node_data.available

    def get_attribute_value(
        self,
        endpoint: int,
        cluster: type[_CLUSTER_T] | int | None,
        attribute: int | type[_ATTRIBUTE_T],
    ) -> Any:
        """Return Matter Cluster Attribute value for given parameters."""
        return self.endpoints[endpoint].get_attribute_value(cluster, attribute)

    def has_cluster(
        self, cluster: type[_CLUSTER_T] | int, endpoint: int | None = None
    ) -> bool:
        """Check if node has a specific cluster on any of the endpoints."""
        return any(
            x
            for x in self.endpoints.values()
            if x.has_cluster(cluster)
            and (endpoint is None or x.endpoint_id == endpoint)
        )

    def get_cluster(
        self, endpoint: int, cluster: type[_CLUSTER_T] | int
    ) -> _CLUSTER_T | None:
        """
        Get a Cluster object containing all attributes.

        Returns None is the Cluster is not present on the node.
        """
        return self.endpoints[endpoint].get_cluster(cluster)

    @property
    def name(self) -> str:
        """Return friendly name for this node."""
        return cast(
            str,
            self.root_device_type_instance.endpoint.get_attribute_value(
                None,
                Clusters.BasicInformation.Attributes.NodeLabel,
            ),
        )

    @property
    def unique_id(self) -> str:
        """Return uniqueID for this node."""
        return cast(
            str,
            self.root_device_type_instance.endpoint.get_attribute_value(
                None,
                Clusters.BasicInformation.Attributes.UniqueID,
            ),
        )

    def __repr__(self) -> str:
        """Return the representation."""
        return f"<MatterNode {self.node_id}>"
