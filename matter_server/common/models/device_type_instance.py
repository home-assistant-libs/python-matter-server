from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Coroutine, Generic, TypeVar

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
        endpoint_id: int,
        device_revision: int,
    ) -> None:
        self.node = node
        self.device_type = device_type
        self.device_revision = device_revision
        self.endpoint_id = endpoint_id

    @property
    def attributes(self) -> list[MatterAttribute]:
        return self.node.get_endpoint_attributes(self.endpoint_id)

    def has_cluster(self, cluster: type[all_clusters.Cluster]) -> bool:
        """Check if device has a specific cluster."""
        return any(x for x in self.attributes if x.cluster_type == cluster)

    def get_cluster(self, cluster: type[_CLUSTER_T]) -> _CLUSTER_T | None:
        """Get the cluster object."""
        if not self.has_cluster(cluster):
            return None

        # instantiate a Cluster object from the properties
        return cluster(
            **{
                x.attribute_name: x.value
                for x in self.node.get_cluster_attributes(cluster, self.endpoint_id)
            }
        )

    def __repr__(self):
        return f"<MatterDeviceTypeInstance {self.device_type.__name__} (N:{self.node.node_id}, E:{self.endpoint_id})>"
