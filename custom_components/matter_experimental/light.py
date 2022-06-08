"""Matter light."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.light import ATTR_BRIGHTNESS, ColorMode, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from matter_server.client.model.device import MatterDevice
from matter_server.vendor import device_types
from matter_server.vendor.chip.clusters import Objects as clusters

from .const import DOMAIN
from .device_platform_helper import DeviceMapping
from .entity import MatterEntity
from .util import renormalize

if TYPE_CHECKING:
    from matter_server.client.matter import Matter


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Matter Light from Config Entry."""
    matter: Matter = hass.data[DOMAIN][config_entry.entry_id]
    matter.adapter.register_platform_handler(Platform.LIGHT, async_add_entities)


class MatterLight(MatterEntity, LightEntity):
    """Representation of a Matter light."""

    def __init__(self, device: MatterDevice, mapping: DeviceMapping) -> None:
        """Initialize the light."""
        super().__init__(device, mapping)
        self._attr_name = device.node.name or f"Matter Light {device.node.node_id}"
        if self._supports_brightness():
            self._attr_supported_color_modes = [ColorMode.BRIGHTNESS]

    def _supports_brightness(self):
        """Return if device supports brightness."""
        return (
            clusters.LevelControl.Attributes.CurrentLevel
            in self._device_mapping.subscribe_attributes
        )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn light on."""
        if ATTR_BRIGHTNESS not in kwargs or not self._supports_brightness():
            await self._device.send_command(
                payload=clusters.OnOff.Commands.On(),
            )
            return

        level_control = self._device.get_cluster(clusters.LevelControl)
        level = round(
            renormalize(
                kwargs[ATTR_BRIGHTNESS],
                (0, 255),
                (level_control.minLevel, level_control.maxLevel),
            )
        )

        await self._device.send_command(
            payload=clusters.LevelControl.Commands.MoveToLevelWithOnOff(level=level)
        )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn light off."""
        await self._device.send_command(
            payload=clusters.OnOff.Commands.Off(),
        )

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        self._attr_is_on = self._device.get_cluster(clusters.OnOff).onOff

        if (
            clusters.LevelControl.Attributes.CurrentLevel
            in self._device_mapping.subscribe_attributes
        ):
            level_control = self._device.get_cluster(clusters.LevelControl)

            # Convert brightness to HA = 0..255
            self._attr_brightness = round(
                renormalize(
                    level_control.currentLevel,
                    (level_control.minLevel, level_control.maxLevel),
                    (0, 255),
                )
            )


DEVICE_ENTITY: dict[
    type[device_types.DeviceType], DeviceMapping | list[DeviceMapping]
] = {
    device_types.OnOffLight: DeviceMapping(
        entity_cls=MatterLight,
        subscribe_attributes=(clusters.OnOff.Attributes.OnOff,),
    ),
    device_types.DimmableLight: DeviceMapping(
        entity_cls=MatterLight,
        subscribe_attributes=(
            clusters.OnOff.Attributes.OnOff,
            clusters.LevelControl.Attributes.CurrentLevel,
        ),
    ),
    device_types.DimmablePlugInUnit: DeviceMapping(
        entity_cls=MatterLight,
        subscribe_attributes=(
            clusters.OnOff.Attributes.OnOff,
            clusters.LevelControl.Attributes.CurrentLevel,
        ),
    ),
}
