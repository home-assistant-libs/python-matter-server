"""Models for a DeviceType instance (per endpoint)."""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Generic, TypeVar

from chip.clusters import Objects as all_clusters

from .device_types import DeviceType

if TYPE_CHECKING:
    from .node import MatterNode


SubscriberType = Callable[[], None]

# pylint: disable=invalid-name
_DEVICE_TYPE_T = TypeVar("_DEVICE_TYPE_T", bound=DeviceType)
_CLUSTER_T = TypeVar("_CLUSTER_T", bound=all_clusters.Cluster)
# pylint: enable=invalid-name


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
        """Initialize the device type instance."""
        self.node = node
        self.device_type = device_type
        self.device_revision = device_revision
        self.endpoint = endpoint

    def has_cluster(self, cluster: type[_CLUSTER_T] | int) -> bool:
        """Check if device has a specific cluster."""
        return self.node.has_cluster(cluster, self.endpoint)

    def get_cluster(self, cluster: type[_CLUSTER_T] | int) -> _CLUSTER_T | None:
        """Get the cluster object."""
        return self.node.get_cluster(self.endpoint, cluster)

    def __repr__(self) -> str:
        """Return the representation."""
        return (
            "<MatterDeviceTypeInstance "
            f"{self.device_type.__name__} "  # type: ignore[attr-defined]
            f"(N:{self.node.node_id}, E:{self.endpoint})>"
        )
