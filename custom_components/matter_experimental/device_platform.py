from __future__ import annotations

from homeassistant.const import Platform


from .light import DEVICE_ENTITY as LIGHT_DEVICE_ENTITY


DEVICE_PLATFORM = {Platform.LIGHT: LIGHT_DEVICE_ENTITY}
