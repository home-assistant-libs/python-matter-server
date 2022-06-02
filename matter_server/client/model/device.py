from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable

from matter_server.vendor.chip.clusters import Objects as all_clusters

if TYPE_CHECKING:
    from .node import MatterNode

DEVICE_TYPES = {}

SubscriberType = Callable[[], None]


class MatterDevice:
    """Base class for Matter devices."""

    device_type: int
    clusters: set[type[all_clusters.Cluster]] = set()
    optional_clusters: set[type[all_clusters.Cluster]] = set()

    def __init_subclass__(cls, *, device_type: int, **kwargs: Any) -> None:
        """Initialize a subclass, register if possible."""
        super().__init_subclass__(**kwargs)
        cls.device_type = device_type
        DEVICE_TYPES[device_type] = cls

    def __init__(
        self, node: MatterNode, endpoint_id: int, device_revision: int
    ) -> None:
        self.node = node
        self.device_revision = device_revision
        self.endpoint_id = endpoint_id
        self._on_update_listener: SubscriberType | None = None

    @property
    def data(self) -> dict:
        return self.node.raw_data["attributes"][str(self.endpoint_id)]

    async def send_command(
        self,
        payload: all_clusters.ClusterCommand,
        responseType=None,
        timedRequestTimeoutMs: int = None,
    ):
        """Send a command to the device."""
        return await self.node.matter.client.driver.device_controller.SendCommand(
            nodeid=self.node.node_id,
            endpoint=self.endpoint_id,
            payload=payload,
            responseType=responseType,
            timedRequestTimeoutMs=timedRequestTimeoutMs,
        )

    async def update_attributes(self, attributes: list) -> None:
        """Update attributes."""
        result = await self.node.matter.client.driver.device_controller.Read(
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
                self.data[cluster_name][attribute] = value

    async def subscribe_updates(
        self, subscribe_attributes: list, subscriber: SubscriberType
    ) -> Callable[[], None]:
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
        subscription = await self.node.matter.client.driver.device_controller.Read(
            self.node.node_id,
            attributes=[
                (self.endpoint_id, attribute) for attribute in subscribe_attributes
            ],
            reportInterval=reporting_timing_params,
        )
        subscription.handler = self._receive_event

        async def unsubscribe() -> None:
            self._on_update_listener = None
            subscription.handler = None
            # TODO actually unsubscribe

        return unsubscribe

    def _receive_event(self, event):
        self.node.matter.adapter.logger.debug(
            "node %s, endpoint %s: received subscription event %s",
            self.node.node_id,
            self.endpoint_id,
            event,
        )

        # 2022-06-01 23:19:08 DEBUG (MainThread) [custom_components.matter_experimental.adapter] Received subscription event
        # {
        #     "SubscriptionId": 4032027010,
        #     "FabridId": 1,
        #     "NodeId": 4339,
        #     "Endpoint": 1,
        #     "Attribute": {
        #         "_class": "chip.clusters.Objects.OnOff.Attributes.GlobalSceneControl"
        #     },
        #     "Value": True,
        # }
        # {
        #     "SubscriptionId": 4032027010,
        #     "FabridId": 1,
        #     "NodeId": 4339,
        #     "Endpoint": 1,
        #     "Attribute": {"_class": "chip.clusters.Objects.OnOff.Attributes.OnOff"},
        #     "Value": True,
        # }

        attribute_parts = event["Attribute"]["_class"].rsplit(".")
        cluster_name = attribute_parts[-3]
        attribute = attribute_parts[-1]
        attribute = attribute[0].lower() + attribute[1:]

        self.node.matter.adapter.logger.debug(
            "Updating node %s, endpoint %s, %s: %s=%s",
            self.node.node_id,
            self.endpoint_id,
            cluster_name,
            attribute,
            event["Value"],
        )

        self.data[cluster_name][attribute] = event["Value"]

        if self._on_update_listener:
            self._on_update_listener()


class RootDevice(MatterDevice, device_type=22):
    """Root device."""

    @property
    def name(self) -> str:
        return self.basic_info["nodeLabel"]

    @property
    def unique_id(self) -> str:
        return self.basic_info["uniqueID"]

    @property
    def basic_info(self) -> dict:
        return self.data["Basic"]


class OnOffLight(MatterDevice, device_type=256):
    """On/Off light."""

    clusters = {
        all_clusters.OnOff,
    }
    optional_clusters = {all_clusters.LevelControl}


class DimmableLight(MatterDevice, device_type=257):
    """Dimmable light."""

    clusters = {all_clusters.OnOff, all_clusters.LevelControl}


class OnOffLightSwitch(MatterDevice, device_type=259):
    """On/Off Light Switch."""


class OnOffPlugInUnit(MatterDevice, device_type=266):
    """On/Off Plug-In Unit."""

    clusters = {
        all_clusters.OnOff,
    }
    optional_clusters = {all_clusters.LevelControl}


class DimmablePlugInUnit(MatterDevice, device_type=267):
    """Dimmable Plug-In Unit."""

    clusters = {all_clusters.OnOff, all_clusters.LevelControl}
