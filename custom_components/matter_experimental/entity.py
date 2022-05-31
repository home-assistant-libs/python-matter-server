"""Matter entity base class."""
from __future__ import annotations

from homeassistant.helpers import entity

from matter_server.client.node import MatterNode

from .const import DOMAIN


class MatterEntity(entity.Entity):
    def __init__(self, node: MatterNode):
        self._node = node

    @property
    def device_info(self) -> entity.DeviceInfo | None:
        """Return device info for device registry."""
        basic_info = self._node.basic_info

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
