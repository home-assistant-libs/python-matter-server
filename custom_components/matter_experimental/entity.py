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
        basic_info = self._device.node.root_device.basic_info

        info = {
            "identifiers": {(DOMAIN, basic_info["uniqueID"])},
            "hw_version": basic_info["hardwareVersionString"],
            "sw_version": basic_info["softwareVersionString"],
            "manufacturer": basic_info["vendorName"],
            "model": basic_info["productName"],
        }
        if basic_info["nodeLabel"]:
            info["name"] = basic_info["nodeLabel"]
        if basic_info["location"]:
            info["suggested_area"] = basic_info["location"]

        return info

    async def async_added_to_hass(self) -> None:
        """Handle being added to Home Assistant."""
        await super().async_added_to_hass()
        # TODO subscribe to updates.

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
