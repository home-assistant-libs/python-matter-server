from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from homeassistant.helpers.entity import EntityDescription

from matter_server.client.model.device import MatterDevice

if TYPE_CHECKING:
    from .entity import MatterEntity


@dataclass
class DeviceMapping:

    entity_cls: type[MatterEntity]
    subscribe_attributes: tuple | None = None
    entity_description: EntityDescription | None = None
    # Return True if you want device to be ignored
    ignore_device: Callable[[MatterDevice], bool] | None = None
