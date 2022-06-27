"""Matter switches."""
from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from typing import TYPE_CHECKING, Any, Callable

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

from matter_server.client.model.device_type_instance import MatterDeviceTypeInstance
from matter_server.vendor import device_types
from matter_server.vendor.chip.clusters import Objects as clusters
from matter_server.vendor.chip.clusters.Types import Nullable, NullValue

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
    matter.adapter.register_platform_handler(Platform.SENSOR, async_add_entities)


class MatterSensor(MatterEntity, SensorEntity):
    """Representation of a Matter sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    entity_description: MatterSensorEntityDescription

    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        measurement: Nullable | float = _get_attribute_value(
            self._device_type_instance,
            # We always subscribe to a single value
            self.entity_description.subscribe_attributes[0],
        )

        if measurement is NullValue:
            measurement = None
        else:
            measurement = self.entity_description.measurement_to_ha(measurement)

        self._attr_native_value = measurement


def _get_attribute_value(
    device_type_instance: MatterDeviceTypeInstance,
    attribute: clusters.ClusterAttributeDescriptor,
) -> Any:
    """Return the value of an attribute."""
    # Find the cluster for this attribute. We don't have a lookup table yet.
    cluster_cls: clusters.Cluster = next(
        cluster
        for cluster in device_type_instance.device_type.clusters
        if cluster.id == attribute.cluster_id
    )

    # Find the attribute descriptor so we know the instance variable to fetch
    attribute_descriptor: clusters.ClusterObjectFieldDescriptor = next(
        descriptor
        for descriptor in cluster_cls.descriptor.Fields
        if descriptor.Tag == attribute.attribute_id
    )

    cluster_data = device_type_instance.get_cluster(cluster_cls)
    return getattr(cluster_data, attribute_descriptor.Label)


@dataclass
class MatterSensorEntityDescriptionMixin:
    """Required fields for sensor device mapping."""

    measurement_to_ha: Callable[[float], float]


@dataclass
class MatterSensorEntityDescription(
    SensorEntityDescription,
    MatterSensorEntityDescriptionMixin,
    MatterEntityDescription,
):
    """Matter Sensor entity description."""


# You can't set default values on inherited data classes
MatterSensorEntityDescriptionFactory = partial(
    MatterSensorEntityDescription, entity_cls=MatterSensor
)


DEVICE_ENTITY: dict[
    type[device_types.DeviceType],
    MatterEntityDescription | list[MatterEntityDescription],
] = {
    device_types.TemperatureSensor: MatterSensorEntityDescriptionFactory(
        key=device_types.TemperatureSensor,
        measurement_to_ha=lambda x: x / 100,
        subscribe_attributes=(
            clusters.TemperatureMeasurement.Attributes.MeasuredValue,
        ),
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    device_types.PressureSensor: MatterSensorEntityDescriptionFactory(
        key=device_types.PressureSensor,
        measurement_to_ha=lambda x: x / 10,
        subscribe_attributes=(clusters.PressureMeasurement.Attributes.MeasuredValue,),
        native_unit_of_measurement=PRESSURE_KPA,
        device_class=SensorDeviceClass.PRESSURE,
    ),
    device_types.FlowSensor: MatterSensorEntityDescriptionFactory(
        key=device_types.FlowSensor,
        measurement_to_ha=lambda x: x / 10,
        subscribe_attributes=(clusters.FlowMeasurement.Attributes.MeasuredValue,),
        native_unit_of_measurement=VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR,
    ),
    device_types.HumiditySensor: MatterSensorEntityDescriptionFactory(
        key=device_types.HumiditySensor,
        measurement_to_ha=lambda x: x / 100,
        subscribe_attributes=(
            clusters.RelativeHumidityMeasurement.Attributes.MeasuredValue,
        ),
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
    ),
    device_types.LightSensor: MatterSensorEntityDescriptionFactory(
        key=device_types.LightSensor,
        measurement_to_ha=lambda x: round(pow(10, ((x - 1) / 10000)), 1),
        subscribe_attributes=(
            clusters.IlluminanceMeasurement.Attributes.MeasuredValue,
        ),
        native_unit_of_measurement=LIGHT_LUX,
        device_class=SensorDeviceClass.ILLUMINANCE,
    ),
}
