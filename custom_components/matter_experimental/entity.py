"""Matter entity base class."""
from __future__ import annotations

import asyncio
from typing import Any, Callable, Coroutine

import async_timeout
from homeassistant.core import callback
from homeassistant.helpers import device_registry, entity

from matter_server.client.model.device import MatterDevice

from .const import DOMAIN
from .device_platform_helper import DeviceMapping


class MatterEntity(entity.Entity):

    _attr_should_poll = False
    _unsubscribe: Callable[..., Coroutine[Any, Any, None]] | None = None

    def __init__(self, device: MatterDevice, mapping: DeviceMapping) -> None:
        self._device = device
        self._device_mapping = mapping
        self._attr_unique_id = f"{device.node.matter.client.server_info.compressedFabricId}-{device.node.unique_id}-{device.endpoint_id}-{device.device_type.device_type}"

    @property
    def device_info(self) -> entity.DeviceInfo | None:
        """Return device info for device registry."""
        return {"identifiers": {(DOMAIN, self._device.node.unique_id)}}

    async def async_added_to_hass(self) -> None:
        """Handle being added to Home Assistant."""
        await super().async_added_to_hass()

        device_name = (
            device_registry.async_get(self.hass)
            .async_get(self.registry_entry.device_id)
            .name
        )

        device_type_name = self._device.device_type.__doc__[:-1]
        name = f"{device_name} {device_type_name}"

        # If this device has multiple of this device type, add their endpoint.
        if (
            sum(
                dev.device_type is self._device.device_type
                for dev in self._device.node.devices
            )
            > 1
        ):
            name += f" ({self._device.endpoint_id})"

        self._attr_name = name

        if not self._device_mapping.subscribe_attributes:
            self._update_from_device()
            return

        try:
            # Subscribe to updates.
            async with async_timeout.timeout(5):
                self._unsubscribe = await self._device.subscribe_updates(
                    self._device_mapping.subscribe_attributes, self._subscription_update
                )

            # Fetch latest info from the device.
            async with async_timeout.timeout(5):
                await self._device.update_attributes(
                    self._device_mapping.subscribe_attributes
                )
        except asyncio.TimeoutError:
            self._device.node.matter.adapter.logger.warning(
                "Timeout interacting with %s, marking device as unavailable. Recovery is not implemented yet. Reload config entry when device is available again.",
                self.entity_id,
            )
            self._attr_available = False

        self._update_from_device()

    async def async_will_remove_from_hass(self) -> None:
        """Run when entity will be removed from hass."""
        if self._unsubscribe is not None:
            await self._unsubscribe()

    @callback
    def _subscription_update(self) -> None:
        """Called when subscription updated."""
        self._update_from_device()
        self.async_write_ha_state()

    @callback
    def _update_from_device(self) -> None:
        """Update data from Matter device."""
        self.async_write_ha_state()
