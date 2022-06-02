"""Matter switches."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.const import Platform
from homeassistant.components.switch import (
    SwitchEntity,
    SwitchEntityDescription,
    SwitchDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from matter_server.vendor.chip.clusters import Objects as clusters
from matter_server.client.model import device as matter_devices

from .const import DOMAIN
from .entity import MatterEntity
from .device_platform_helper import DeviceMapping

if TYPE_CHECKING:
    from matter_server.client.matter import Matter


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Matter Light from Config Entry."""
    matter: Matter = hass.data[DOMAIN][config_entry.entry_id]
    matter.adapter.register_platform_handler(Platform.SWITCH, async_add_entities)


class MatterSwitch(MatterEntity, SwitchEntity):
    """Representation of a Matter switch."""

    def __init__(
        self, device: matter_devices.MatterDevice, mapping: DeviceMapping
    ) -> None:
        """Initialize the switch."""
        super().__init__(device, mapping)
        self._attr_name = device.node.name or f"Matter Switch {device.node.node_id}"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn switch on."""
        await self._device.send_command(
            payload=clusters.OnOff.Commands.On(),
        )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn switch off."""
        await self._device.send_command(
            payload=clusters.OnOff.Commands.Off(),
        )

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        self._attr_is_on = self._device.data["OnOff"]["onOff"]


DEVICE_ENTITY: dict[
    matter_devices.MatterDevice, DeviceMapping | list[DeviceMapping]
] = {
    matter_devices.OnOffPlugInUnit: DeviceMapping(
        entity_cls=MatterSwitch,
        subscribe_attributes=(clusters.OnOff.Attributes.OnOff,),
        entity_description=SwitchEntityDescription(
            key=None,
            device_class=SwitchDeviceClass.OUTLET,
        ),
    ),
}
