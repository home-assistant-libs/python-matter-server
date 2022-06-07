"""All mappings of Matter devices to HA platforms."""
from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import Platform

from .device_platform_helper import DeviceMapping
from .light import DEVICE_ENTITY as LIGHT_DEVICE_ENTITY
from .sensor import DEVICE_ENTITY as SENSOR_DEVICE_ENTITY
from .switch import DEVICE_ENTITY as SWITCH_DEVICE_ENTITY

if TYPE_CHECKING:
    from matter_server.client.model import device as matter_devices


DEVICE_PLATFORM: dict[
    Platform, dict[matter_devices.MatterDevice, DeviceMapping | list[DeviceMapping]]
] = {
    Platform.LIGHT: LIGHT_DEVICE_ENTITY,
    Platform.SENSOR: SENSOR_DEVICE_ENTITY,
    Platform.SWITCH: SWITCH_DEVICE_ENTITY,
}
