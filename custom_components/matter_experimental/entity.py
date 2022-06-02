"""Matter entity base class."""
from __future__ import annotations

from homeassistant.core import callback
from homeassistant.helpers import entity

from matter_server.client.device import MatterDevice

from .const import DOMAIN


class MatterEntity(entity.Entity):
    def __init__(self, device: MatterDevice):
        self._device = device

    @property
    def device_info(self) -> entity.DeviceInfo | None:
        """Return device info for device registry."""
        return {"identifiers": {(DOMAIN, self._device.node.unique_id)}}

    async def async_added_to_hass(self) -> None:
        """Handle being added to Home Assistant."""
        await super().async_added_to_hass()

        if not self._device.cluster_subscribes:
            return

        self.async_on_remove(
            await self._device.subscribe_updates(self._update_from_device)
        )

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
