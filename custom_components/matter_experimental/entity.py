"""Matter entity base class."""
from __future__ import annotations

from typing import Any, Callable, Coroutine

from homeassistant.core import callback
from homeassistant.helpers import entity

from matter_server.client.model.device import MatterDevice
from matter_server.vendor.chip.clusters import Objects as clusters

from .const import DOMAIN
from .device_platform_helper import DeviceMapping


class MatterEntity(entity.Entity):

    _unsubscribe: Callable[..., Coroutine[Any, Any, None]] | None = None

    def __init__(self, device: MatterDevice, mapping: DeviceMapping) -> None:
        self._device = device
        self._device_mapping = mapping
        self._attr_unique_id = (
            f"{device.node.unique_id}-{device.endpoint_id}-{device.device_type}"
        )

    @property
    def device_info(self) -> entity.DeviceInfo | None:
        """Return device info for device registry."""
        return {"identifiers": {(DOMAIN, self._device.node.unique_id)}}

    async def async_added_to_hass(self) -> None:
        """Handle being added to Home Assistant."""
        await super().async_added_to_hass()

        if not self._device_mapping.subscribe_attributes:
            self._update_from_device()
            return

        # Detect the clusters that this device has
        present_clusters = set(cluster.id for cluster in self._device.clusters)

        for cluster in self._device.optional_clusters:
            if cluster.__name__ in self._device.data:
                present_clusters.add(cluster.id)

        # Filter out subscribe attributes belonging to optional clusters not present
        subscribe_attributes = []

        for attribute in self._device_mapping.subscribe_attributes:
            if attribute.cluster_id in present_clusters:
                subscribe_attributes.append(attribute)

        # Fetch latest info from the device.
        await self._device.update_attributes(subscribe_attributes)
        self._update_from_device()

        # Subscribe to updates.
        self._unsubscribe = await self._device.subscribe_updates(
            subscribe_attributes, self._update_from_device
        )

    async def async_will_remove_from_hass(self) -> None:
        """Run when entity will be removed from hass."""
        if self._unsubscribe is not None:
            await self._unsubscribe()

    def has_cluster(self, cluster: type[clusters.Cluster]) -> bool:
        """Check if device has a specific cluster."""
        if cluster in self._device.clusters:
            return True

        if cluster not in self._device.optional_clusters:
            return False

        return cluster.__name__ in self._device.data

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
