"""Model(s) for working with Matter nodes/devices."""


from datetime import datetime
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Dict

from chip.clusters import (
        Attribute,
        Cluster,
        ClusterAttributeDescriptor,
        ClusterEvent,
    )

@dataclass
class MatterAttribute(Attribute.AttributeCache):
    """Representation of a Matter Attribute."""



@dataclass
class MatterNode:
    """Representation of a Matter Node."""

    nodeid: int
    date_commissioned: datetime
    last_interview: datetime
    interview_version: int
    attributes: Dict[int, Dict[type, Cluster]]


class CommissionOption(IntEnum):
    """Enum with available comissioning methodes/options."""

    BASIC = 0
    ENHANCED = 1
