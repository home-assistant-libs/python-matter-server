"""Matter light."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.light import LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from matter_server.vendor.chip.clusters import Objects as Clusters

from .const import DOMAIN
from .entity import MatterEntity

if TYPE_CHECKING:
    from matter_server.client.matter import Matter
    from matter_server.client.node import MatterNode


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Hue Light from Config Entry."""
    matter: Matter = hass.data[DOMAIN][config_entry.entry_id]

    # Temp. Should be done in adapter.setup_entity instead.
    async_add_entities([MatterLight(matter, node) for node in matter.get_nodes()])


class MatterLight(MatterEntity, LightEntity):
    """Representation of a Matter light."""

    _attr_is_on = False
    _attr_assumed_state = True

    def __init__(self, matter: Matter, node: MatterNode) -> None:
        """Initialize the light."""
        super().__init__(node)
        self.matter = matter
        self._attr_unique_id = node.unique_id
        self._attr_name = node.name or f"Matter Light {node.node_id}"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn light on."""
        await self.matter.client.driver.device_controller.SendCommand(
            nodeid=self._node.node_id, endpoint=1, payload=Clusters.OnOff.Commands.On()
        )
        self._attr_is_on = True

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn light off."""
        await self.matter.client.driver.device_controller.SendCommand(
            nodeid=self._node.node_id,
            endpoint=1,
            payload=Clusters.OnOff.Commands.Off(),
        )
        self._attr_is_on = False
