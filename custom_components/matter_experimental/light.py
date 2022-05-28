"""Matter light."""
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.light import (
    LightEntity,
)

from matter_server.client.client import Client
from matter_server.vendor.chip.clusters import Objects as Clusters

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Hue Light from Config Entry."""
    client: Client = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([MatterLight(client, 4335)])


class MatterLight(LightEntity):
    """Representation of a Matter light."""

    _attr_is_on = False
    _attr_assumed_state = True

    def __init__(self, client: Client, node_id: int) -> None:
        """Initialize the light."""
        self.client = client
        self.node_id = node_id
        self._attr_name = f"Matter Light {node_id}"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn light on."""
        await self.client.driver.device_controller.SendCommand(
            nodeid=self.node_id, endpoint=1, payload=Clusters.OnOff.Commands.On()
        )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn light off."""
        await self.client.driver.device_controller.SendCommand(
            nodeid=self.node_id, endpoint=1, payload=Clusters.OnOff.Commands.Off()
        )
