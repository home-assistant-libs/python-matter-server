"""Matter switches."""
from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, TEMP_CELSIUS
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from matter_server.client.model import devices as matter_devices
from matter_server.vendor.chip.clusters import Objects as clusters
from matter_server.vendor.chip.clusters.Types import Nullable

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
    matter.adapter.register_platform_handler(Platform.SENSOR, async_add_entities)


class MatterSensor(MatterEntity, SensorEntity):
    """Representation of a Matter sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self, device: matter_devices.MatterDevice, mapping: DeviceMapping
    ) -> None:
        """Initialize the sensor."""
        super().__init__(device, mapping)
        self._attr_name = device.node.name or f"Matter Sensor {device.node.node_id}"


class MatterTemperatureSesnor(MatterSensor):
    """Representation of a Matter temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = TEMP_CELSIUS

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        measurement = self._device.get_cluster(
            clusters.TemperatureMeasurement
        ).measuredValue

        if measurement is Nullable:
            measurement = None
        else:
            measurement /= 100

        self._attr_native_value = measurement


class MatterPressureSesnor(MatterSensor):
    """Representation of a Matter pressure sensor."""

    _attr_device_class = SensorDeviceClass.PRESSURE
    _attr_native_unit_of_measurement = "kPa"

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        measurement = self._device.get_cluster(
            clusters.PressureMeasurement
        ).measuredValue

        if measurement is Nullable:
            measurement = None
        else:
            measurement /= 10

        self._attr_native_value = measurement


DEVICE_ENTITY: dict[
    matter_devices.MatterDevice, DeviceMapping | list[DeviceMapping]
] = {
    matter_devices.TemperatureSensor: DeviceMapping(
        entity_cls=MatterTemperatureSesnor,
        subscribe_attributes=(
            clusters.TemperatureMeasurement.Attributes.MeasuredValue,
        ),
    ),
    matter_devices.PressureSensor: DeviceMapping(
        entity_cls=MatterPressureSesnor,
        subscribe_attributes=(clusters.PressureMeasurement.Attributes.MeasuredValue,),
    ),
}
