"""Matter switches."""
from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    Platform,
    TEMP_CELSIUS,
    PERCENTAGE,
    LIGHT_LUX,
    VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR,
    PRESSURE_KPA,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from matter_server.client.model.device import MatterDevice
from matter_server.vendor import device_types
from matter_server.vendor.chip.clusters import Objects as clusters
from matter_server.vendor.chip.clusters.Types import NullValue

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

    def __init__(self, device: MatterDevice, mapping: DeviceMapping) -> None:
        """Initialize the sensor."""
        super().__init__(device, mapping)
        self._attr_name = device.node.name or f"Matter Sensor {device.node.node_id}"


class MatterTemperatureSensor(MatterSensor):
    """Representation of a Matter temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = TEMP_CELSIUS

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        measurement = self._device.get_cluster(
            clusters.TemperatureMeasurement
        ).measuredValue

        if measurement is NullValue:
            measurement = None
        else:
            measurement /= 100

        self._attr_native_value = measurement


class MatterPressureSensor(MatterSensor):
    """Representation of a Matter pressure sensor."""

    _attr_device_class = SensorDeviceClass.PRESSURE
    _attr_native_unit_of_measurement = PRESSURE_KPA

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        measurement = self._device.get_cluster(
            clusters.PressureMeasurement
        ).measuredValue

        if measurement is NullValue:
            measurement = None
        else:
            measurement /= 10

        self._attr_native_value = measurement


class MatterFlowSensor(MatterSensor):
    """Representation of a Matter flow sensor."""

    _attr_native_unit_of_measurement = VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        measurement = self._device.get_cluster(clusters.FlowMeasurement).measuredValue

        if measurement is NullValue:
            measurement = None
        else:
            measurement /= 10

        self._attr_native_value = measurement


class MatterHumiditySensor(MatterSensor):
    """Representation of a Matter humidity sensor."""

    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_native_unit_of_measurement = PERCENTAGE

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        measurement = self._device.get_cluster(
            clusters.RelativeHumidityMeasurement
        ).measuredValue

        if measurement is NullValue:
            measurement = None
        else:
            measurement /= 100

        self._attr_native_value = measurement


class MatterLightSensor(MatterSensor):
    """Representation of a Matter light sensor."""

    _attr_device_class = SensorDeviceClass.ILLUMINANCE
    _attr_native_unit_of_measurement = LIGHT_LUX

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        measurement = self._device.get_cluster(
            clusters.RelativeHumidityMeasurement
        ).measuredValue

        if measurement is NullValue:
            measurement = None
        else:
            measurement = round(pow(10, ((measurement - 1) / 10000)), 1)

        self._attr_native_value = measurement


DEVICE_ENTITY: dict[
    type[device_types.DeviceType], DeviceMapping | list[DeviceMapping]
] = {
    device_types.TemperatureSensor: DeviceMapping(
        entity_cls=MatterTemperatureSensor,
        subscribe_attributes=(
            clusters.TemperatureMeasurement.Attributes.MeasuredValue,
        ),
    ),
    device_types.PressureSensor: DeviceMapping(
        entity_cls=MatterPressureSensor,
        subscribe_attributes=(clusters.PressureMeasurement.Attributes.MeasuredValue,),
    ),
    device_types.FlowSensor: DeviceMapping(
        entity_cls=MatterFlowSensor,
        subscribe_attributes=(clusters.FlowMeasurement.Attributes.MeasuredValue,),
    ),
    device_types.HumiditySensor: DeviceMapping(
        entity_cls=MatterHumiditySensor,
        subscribe_attributes=(
            clusters.RelativeHumidityMeasurement.Attributes.MeasuredValue,
        ),
    ),
    device_types.LightSensor: DeviceMapping(
        entity_cls=MatterLightSensor,
        subscribe_attributes=(
            clusters.IlluminanceMeasurement.Attributes.MeasuredValue,
        ),
    ),
}
