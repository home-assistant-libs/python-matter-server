from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Coroutine, Generic, Optional, TypeVar

from .device_types import DeviceType
from chip.clusters import Objects as all_clusters

if TYPE_CHECKING:
    from .node import MatterNode, MatterAttribute


SubscriberType = Callable[[], None]


_DEVICE_TYPE_T = TypeVar("_DEVICE_TYPE_T", bound=DeviceType)
_CLUSTER_T = TypeVar("_CLUSTER_T", bound=all_clusters.Cluster)


class MatterDeviceTypeInstance(Generic[_DEVICE_TYPE_T]):
    """Base class for Matter device types on endpoints."""

    do_not_serialize = True

    def __init__(
        self,
        node: MatterNode,
        device_type: _DEVICE_TYPE_T,
        endpoint: int,
        device_revision: int,
    ) -> None:
        self.node = node
        self.device_type = device_type
        self.device_revision = device_revision
        self.endpoint = endpoint

    @property
    def attributes(self) -> list[MatterAttribute]:
        """Return all Attributes belonging to this DeviceTypeInstance."""
        return [
            attr
            for attr in self.node.get_endpoint_attributes(self.endpoint)
            if attr.cluster_type in self.device_type.clusters
        ]

    def has_cluster(self, cluster: type[all_clusters.Cluster]) -> bool:
        """Check if device has a specific cluster."""
        # only return True if the cluster belongs to this device type
        # and is actually present in the atributes.
        return cluster in self.device_type.clusters and any(
            x for x in self.attributes if x.cluster_type == cluster
        )

    def get_cluster(self, cluster: type[_CLUSTER_T]) -> Optional[_CLUSTER_T]:
        """Get the cluster object."""
        # only return Cluster if the cluster belongs to this device type
        # and is actually present in the atributes.
        if cluster not in self.device_type.clusters:
            return None
        return self.node.get_cluster(self.endpoint, cluster)

    def __repr__(self):
        return f"<MatterDeviceTypeInstance {self.device_type.__name__} (N:{self.node.node_id}, E:{self.endpoint})>"
