from __future__ import annotations
from dataclasses import dataclass

from .entity import MatterEntity


@dataclass
class DeviceMapping:

    entity_cls: type[MatterEntity]
