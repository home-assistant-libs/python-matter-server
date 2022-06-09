from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.helpers.entity import EntityDescription

if TYPE_CHECKING:
    from .entity import MatterEntity


@dataclass
class DeviceMapping:
    """Map a matter device to a HA entity."""

    entity_cls: type[MatterEntity]
    subscribe_attributes: tuple | None = None
    entity_description: EntityDescription | None = None
