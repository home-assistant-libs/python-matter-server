"""Matter switches."""
from __future__ import annotations

from dataclasses import dataclass
from functools import partial
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

from matter_server.vendor import device_types
from matter_server.vendor.chip.clusters import Objects as clusters

from .const import DOMAIN
from .entity import MatterEntity
from .entity_description import MatterEntityDescription

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

    entity_description: MatterBinarySensorEntityDescription

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        self._attr_is_on = self._device_type_instance.get_cluster(
            clusters.BooleanState
        ).stateValue


class MatterOccupancySensor(MatterBinarySensor):
    """Representation of a Matter occupancy sensor."""

    _attr_device_class = BinarySensorDeviceClass.OCCUPANCY

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        occupancy = self._device_type_instance.get_cluster(
            clusters.OccupancySensing
        ).occupancy
        # The first bit = if occupied
        self._attr_is_on = occupancy & 1 == 1


@dataclass
class MatterBinarySensorEntityDescription(
    BinarySensorEntityDescription,
    MatterEntityDescription,
):
    """Matter Binary Sensor entity description."""


# You can't set default values on inherited data classes
MatterSensorEntityDescriptionFactory = partial(
    MatterBinarySensorEntityDescription, entity_cls=MatterBinarySensor
)

DEVICE_ENTITY: dict[
    type[device_types.DeviceType],
    MatterEntityDescription | list[MatterEntityDescription],
] = {
    device_types.ContactSensor: MatterSensorEntityDescriptionFactory(
        key=device_types.ContactSensor,
        name="Contact",
        subscribe_attributes=(clusters.BooleanState.Attributes.StateValue,),
        device_class=BinarySensorDeviceClass.DOOR,
    ),
    device_types.OccupancySensor: MatterSensorEntityDescriptionFactory(
        key=device_types.OccupancySensor,
        name="Occupancy",
        entity_cls=MatterOccupancySensor,
        subscribe_attributes=(clusters.OccupancySensing.Attributes.Occupancy,),
    ),
}
