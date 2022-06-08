"""All mappings of Matter devices to HA platforms."""
from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import Platform

from .binary_sensor import DEVICE_ENTITY as BINARY_SENSOR_DEVICE_ENTITY
from .light import DEVICE_ENTITY as LIGHT_DEVICE_ENTITY
from .sensor import DEVICE_ENTITY as SENSOR_DEVICE_ENTITY
from .switch import DEVICE_ENTITY as SWITCH_DEVICE_ENTITY

if TYPE_CHECKING:
    from matter_server.vendor.device_types import DeviceType

    from .device_platform_helper import DeviceMapping


DEVICE_PLATFORM: dict[
    Platform, dict[type[DeviceType], DeviceMapping | list[DeviceMapping]]
] = {
    Platform.BINARY_SENSOR: BINARY_SENSOR_DEVICE_ENTITY,
    Platform.LIGHT: LIGHT_DEVICE_ENTITY,
    Platform.SENSOR: SENSOR_DEVICE_ENTITY,
    Platform.SWITCH: SWITCH_DEVICE_ENTITY,
}
