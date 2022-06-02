"""Matter light."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.const import Platform
from homeassistant.components.light import LightEntity, ColorMode, ATTR_BRIGHTNESS
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import percentage

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
    matter.adapter.register_platform_handler(Platform.LIGHT, async_add_entities)


class MatterLight(MatterEntity, LightEntity):
    """Representation of a Matter light."""

    def __init__(
        self, device: matter_devices.MatterDevice, mapping: DeviceMapping
    ) -> None:
        """Initialize the light."""
        super().__init__(device, mapping)
        self._attr_name = device.node.name or f"Matter Light {device.node.node_id}"
        if self.has_cluster(clusters.LevelControl):
            self._attr_supported_color_modes = [ColorMode.BRIGHTNESS]

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn light on."""
        if ATTR_BRIGHTNESS not in kwargs or not self.has_cluster(clusters.LevelControl):
            await self._device.send_command(
                payload=clusters.OnOff.Commands.On(),
            )
            return

        level_control = self._device.data["LevelControl"]
        level = percentage.percentage_to_ranged_value(
            (level_control["minLevel"], level_control["maxLevel"]),
            percentage.ranged_value_to_percentage(
                (0, 255),
                kwargs[ATTR_BRIGHTNESS],
            ),
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
        self._attr_is_on = self._device.data["OnOff"]["onOff"]

        if self.has_cluster(clusters.LevelControl):
            level_control = self._device.data["LevelControl"]
            # Convert brightness to HA = 0..255
            self._attr_brightness = percentage.percentage_to_ranged_value(
                (0, 255),
                percentage.ranged_value_to_percentage(
                    (level_control["minLevel"], level_control["maxLevel"]),
                    level_control["currentLevel"],
                ),
            )
        self.async_write_ha_state()


DEFAULT_MAPPING = DeviceMapping(
    entity_cls=MatterLight,
    subscribe_attributes=(
        clusters.OnOff.Attributes.OnOff,
        clusters.LevelControl.Attributes.CurrentLevel,
    ),
)


DEVICE_ENTITY: dict[
    matter_devices.MatterDevice, DeviceMapping | list[DeviceMapping]
] = {
    matter_devices.OnOffLight: DEFAULT_MAPPING,
    matter_devices.DimmableLight: DEFAULT_MAPPING,
    matter_devices.DimmablePlugInUnit: DEFAULT_MAPPING,
}
