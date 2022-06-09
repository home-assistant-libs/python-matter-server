"""Matter switches."""
from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from typing import TYPE_CHECKING, Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    LIGHT_LUX,
    PERCENTAGE,
    PRESSURE_KPA,
    TEMP_CELSIUS,
    VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR,
    Platform,
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
    _device_mapping: SensorDeviceMapping

    def __init__(self, device: MatterDevice, mapping: SensorDeviceMapping) -> None:
        """Initialize the sensor."""
        super().__init__(device, mapping)
        self._attr_name = device.node.name or f"Matter Sensor {device.node.node_id}"

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        measurement = self._device.get_cluster(
            clusters.TemperatureMeasurement
        ).measuredValue

        if measurement is NullValue:
            measurement = None
        else:
            measurement = self._device_mapping.measurement_to_ha(measurement)

        self._attr_native_value = measurement


@dataclass
class SensorDeviceMappingMixin:
    """Required fields for sensor device mapping."""

    measurement_to_ha: Callable[[float], float]


@dataclass
class SensorDeviceMapping(DeviceMapping, SensorDeviceMappingMixin):
    """Matter Sensor device mapping."""


# You can't set default values on inherited data classes
SensorDeviceMappingCls = partial(SensorDeviceMapping, entity_cls=SensorEntity)
SensorEntityDescriptionKey = partial(SensorEntityDescription, key=None)


DEVICE_ENTITY: dict[
    type[device_types.DeviceType], DeviceMapping | list[DeviceMapping]
] = {
    device_types.TemperatureSensor: SensorDeviceMappingCls(
        measurement_to_ha=lambda x: x / 100,
        subscribe_attributes=(
            clusters.TemperatureMeasurement.Attributes.MeasuredValue,
        ),
        entity_description=SensorEntityDescriptionKey(
            native_unit_of_measurement=TEMP_CELSIUS,
            device_class=SensorDeviceClass.TEMPERATURE,
        ),
    ),
    device_types.PressureSensor: SensorDeviceMappingCls(
        measurement_to_ha=lambda x: x / 10,
        subscribe_attributes=(clusters.PressureMeasurement.Attributes.MeasuredValue,),
        entity_description=SensorEntityDescriptionKey(
            native_unit_of_measurement=PRESSURE_KPA,
            device_class=SensorDeviceClass.PRESSURE,
        ),
    ),
    device_types.FlowSensor: SensorDeviceMappingCls(
        measurement_to_ha=lambda x: x / 10,
        subscribe_attributes=(clusters.FlowMeasurement.Attributes.MeasuredValue,),
        entity_description=SensorEntityDescriptionKey(
            native_unit_of_measurement=VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR,
        ),
    ),
    device_types.HumiditySensor: SensorDeviceMappingCls(
        measurement_to_ha=lambda x: x / 100,
        subscribe_attributes=(
            clusters.RelativeHumidityMeasurement.Attributes.MeasuredValue,
        ),
        entity_description=SensorEntityDescriptionKey(
            native_unit_of_measurement=PERCENTAGE,
            device_class=SensorDeviceClass.HUMIDITY,
        ),
    ),
    device_types.LightSensor: SensorDeviceMappingCls(
        measurement_to_ha=lambda x: round(pow(10, ((x - 1) / 10000)), 1),
        subscribe_attributes=(
            clusters.IlluminanceMeasurement.Attributes.MeasuredValue,
        ),
        entity_description=SensorEntityDescriptionKey(
            native_unit_of_measurement=LIGHT_LUX,
            device_class=SensorDeviceClass.ILLUMINANCE,
        ),
    ),
}
