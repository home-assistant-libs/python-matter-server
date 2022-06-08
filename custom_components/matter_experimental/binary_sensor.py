"""Matter switches."""
from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
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

if TYPE_CHECKING:
    from matter_server.client.matter import Matter


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Matter Light from Config Entry."""
    matter: Matter = hass.data[DOMAIN][config_entry.entry_id]
    matter.adapter.register_platform_handler(Platform.BINARY_SENSOR, async_add_entities)


class MatterBinarySensor(MatterEntity, BinarySensorEntity):
    """Representation of a Matter binary sensor."""

    def __init__(self, device: MatterDevice, mapping: DeviceMapping) -> None:
        """Initialize the sensor."""
        super().__init__(device, mapping)
        self._attr_name = device.node.name or f"Matter Sensor {device.node.node_id}"

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        self._attr_is_on = self._device.get_cluster(clusters.BooleanState).stateValue


class MatterOccupancySensor(MatterEntity, BinarySensorEntity):
    """Representation of a Matter occupancy sensor."""

    _attr_device_class = BinarySensorDeviceClass.OCCUPANCY

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        occupancy = self._device.get_cluster(clusters.OccupancySensing).occupancy
        # The first bit = if occupied
        self._attr_is_on = occupancy & 1 == 1


DEVICE_ENTITY: dict[
    type[device_types.DeviceType], DeviceMapping | list[DeviceMapping]
] = {
    device_types.ContactSensor: DeviceMapping(
        entity_cls=MatterBinarySensor,
        subscribe_attributes=(clusters.BooleanState.Attributes.StateValue,),
        entity_description=BinarySensorEntityDescription(
            key=None,
            device_class=BinarySensorDeviceClass.DOOR,
        ),
    ),
    device_types.OccupancySensor: DeviceMapping(
        entity_cls=MatterOccupancySensor,
        subscribe_attributes=(clusters.OccupancySensing.Attributes.Occupancy,),
    ),
}
