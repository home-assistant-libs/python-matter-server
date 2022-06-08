from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Coroutine, Generic, TypeVar

from matter_server.vendor import device_types
from matter_server.vendor.chip.clusters import Objects as all_clusters

if TYPE_CHECKING:
    from .node import MatterNode

SubscriberType = Callable[[], None]


_DEVICE_TYPE_T = TypeVar("_DEVICE_TYPE_T", bound=device_types.DeviceType)
_CLUSTER_T = TypeVar("_CLUSTER_T", bound=all_clusters.Cluster)


class MatterDevice(Generic[_DEVICE_TYPE_T]):
    """Base class for Matter devices."""

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
        self._on_update_listener: SubscriberType | None = None

    @property
    def data(self) -> dict:
        return self.node.raw_data["attributes"][str(self.endpoint_id)]

    def has_cluster(self, cluster: type[all_clusters.Cluster]) -> bool:
        """Check if device has a specific cluster."""
        return cluster in self.device_type.clusters and cluster.__name__ in self.data

    def get_cluster(self, cluster: type[_CLUSTER_T]) -> _CLUSTER_T | None:
        """Get the cluster object."""
        if not self.has_cluster(cluster):
            return None

        return self.data[cluster.__name__]

    async def send_command(
        self,
        payload: all_clusters.ClusterCommand,
        responseType=None,
        timedRequestTimeoutMs: int = None,
    ):
        """Send a command to the device."""
        return await self.node.matter.client.driver.device_controller.send_command(
            nodeid=self.node.node_id,
            endpoint=self.endpoint_id,
            payload=payload,
            responseType=responseType,
            timedRequestTimeoutMs=timedRequestTimeoutMs,
        )

    async def update_attributes(self, attributes: list) -> None:
        """Update attributes."""
        result = await self.node.matter.client.driver.device_controller.read(
            self.node.node_id,
            attributes=[(self.endpoint_id, attribute) for attribute in attributes],
        )

        # {
        #     "attributes": {
        #         "1": {
        #             "LevelControl": {"DataVersion": 2821513409, "CurrentLevel": 1},
        #             "OnOff": {"DataVersion": 781696941, "OnOff": True},
        #         }
        #     },
        #     "events": [],
        #     "_type": "chip.clusters.Attribute.AsyncReadTransaction.ReadResponse",
        # }

        self.node.matter.adapter.logger.debug("Read result: %s", result)

        updated_data = result["attributes"].get(str(self.endpoint_id))

        for cluster_name, info in updated_data.items():
            info.pop("DataVersion")
            # Convert to dictionary where all the keys start with lowercase
            info = {key[0].lower() + key[1:]: value for key, value in info.items()}
            for attribute, value in info.items():
                self.node.matter.adapter.logger.debug(
                    "node %s, endpoint %s: updating %s, set %s=%s",
                    self.node.node_id,
                    self.endpoint_id,
                    cluster_name,
                    attribute,
                    value,
                )
                setattr(self.data[cluster_name], attribute, value)

    async def subscribe_updates(
        self, subscribe_attributes: list, subscriber: SubscriberType
    ) -> Callable[[], Coroutine[None]]:
        """Subscribe to updates."""
        if self._on_update_listener is not None:
            raise RuntimeError("Cannot subscribe twice!")

        self.node.matter.adapter.logger.debug(
            "node %s, endpoint %s: subscribing to %s",
            self.node.node_id,
            self.endpoint_id,
            subscribe_attributes,
        )

        self._on_update_listener = subscriber

        reporting_timing_params = (0, 10)

        unsub_subscription = (
            await self.node.matter.client.driver.read_subscriptions.subscribe_node(
                nodeid=self.node.node_id,
                subscription_callback=self._receive_event,
                attributes=[
                    (self.endpoint_id, attribute) for attribute in subscribe_attributes
                ],
                reportInterval=reporting_timing_params,
            )
        )

        async def unsubscribe() -> None:
            self.node.matter.adapter.logger.debug(
                "node %s, endpoint %s: unsubscribing from %s",
                self.node.node_id,
                self.endpoint_id,
                subscribe_attributes,
            )
            self._on_update_listener = None
            await unsub_subscription()

        return unsubscribe

    def _receive_event(self, event):
        self.node.matter.adapter.logger.debug(
            "node %s, endpoint %s: received subscription event %s",
            self.node.node_id,
            self.endpoint_id,
            event,
        )

        # 2022-06-03 11:30:52 DEBUG (MainThread) [custom_components.matter_experimental.adapter] node 4335, endpoint 1: received subscription event
        # {'SubscriptionId': 2632459106, 'FabridId': 1, 'NodeId': 4335, 'Endpoint': 1, 'Attribute': <class 'matter_server.vendor.chip.clusters.Objects.OnOff.Attributes.OnOff'>, 'Value': False}

        self.node.matter.adapter.logger.debug(
            "Updating node %s, endpoint %s, %s: %s=%s",
            self.node.node_id,
            self.endpoint_id,
            event["cluster"].__name__,
            event["attribute"],
            event["value"],
        )

        setattr(
            self.data[event["cluster"].__name__], event["attribute"], event["value"]
        )

        if self._on_update_listener:
            self._on_update_listener()
