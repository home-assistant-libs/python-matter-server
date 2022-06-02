"""Matter light."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.const import Platform
from homeassistant.components.light import LightEntity, ColorMode, ATTR_BRIGHTNESS
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import percentage

from matter_server.vendor.chip.clusters import Objects as Clusters
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


class MatterLight(
    MatterEntity,
    LightEntity,
):
    """Representation of a Matter light."""

    _attr_is_on = False

    def __init__(
        self, device: matter_devices.OnOffLight | matter_devices.DimmableLight
    ) -> None:
        """Initialize the light."""
        super().__init__(device)
        node = device.node
        self._attr_unique_id = node.unique_id
        self._attr_name = node.name or f"Matter Light {node.node_id}"
        self._update_from_device()
        self._attr_supported_color_modes = [ColorMode.BRIGHTNESS]

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn light on."""
        if (
            self._device.device_type != matter_devices.DimmableLight.device_type
            or ATTR_BRIGHTNESS not in kwargs
        ):
            await self._device.send_command(
                payload=Clusters.OnOff.Commands.On(),
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
            payload=Clusters.LevelControl.Commands.MoveToLevelWithOnOff(level=level)
        )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn light off."""
        await self._device.send_command(
            payload=Clusters.OnOff.Commands.Off(),
        )

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        self._attr_is_on = self._device.data["OnOff"]["onOff"]

        if self._device.device_type == matter_devices.DimmableLight.device_type:
            level_control = self._device.data["LevelControl"]
            # Convert brightness to HA = 0..255
            self._attr_brightness = percentage.percentage_to_ranged_value(
                (0, 255),
                percentage.ranged_value_to_percentage(
                    (level_control["minLevel"], level_control["maxLevel"]),
                    level_control["currentLevel"],
                ),
            )


DEVICE_ENTITY: dict[
    matter_devices.MatterDevice, DeviceMapping | list[DeviceMapping]
] = {
    matter_devices.OnOffLight: DeviceMapping(entity_cls=MatterLight),
    matter_devices.DimmableLight: DeviceMapping(entity_cls=MatterLight),
}
