"""Definitions for custom (vendor specific) Matter clusters."""

from dataclasses import dataclass
from typing import ClassVar

from chip import ChipUtility
from chip.clusters.ClusterObjects import (
    Cluster,
    ClusterAttributeDescriptor,
    ClusterObjectDescriptor,
    ClusterObjectFieldDescriptor,
)
from chip.tlv import float32

# pylint: disable=invalid-name,arguments-renamed,no-self-argument
# mypy: ignore_errors=true


@dataclass
class CustomCluster:
    """Base model for a vendor specific custom cluster."""

    should_poll: bool = False  # should the entire cluster be polled for state changes?


@dataclass
class CustomClusterAttribute:
    """Base model for a vendor specific custom cluster attribute."""

    should_poll: bool = False  # should this attribute be polled ?


@dataclass
class EveEnergyCluster(Cluster, CustomCluster):
    """Custom (vendor-specific) cluster for Eve Energy plug."""

    id: ClassVar[int] = 0x130AFC01

    @ChipUtility.classproperty
    def descriptor(cls) -> ClusterObjectDescriptor:
        """Return descriptor for this cluster."""
        return ClusterObjectDescriptor(
            Fields=[
                ClusterObjectFieldDescriptor(
                    Label="watt", Tag=0x130A000A, Type=float32
                ),
                ClusterObjectFieldDescriptor(
                    Label="wattAccumulated", Tag=0x130A000B, Type=float32
                ),
                ClusterObjectFieldDescriptor(
                    Label="wattAccumulatedControlPoint", Tag=0x130A000E, Type=float32
                ),
                ClusterObjectFieldDescriptor(
                    Label="voltage", Tag=0x130A0008, Type=float32
                ),
                ClusterObjectFieldDescriptor(
                    Label="current", Tag=0x130A0009, Type=float32
                ),
            ]
        )

    watt: float32 | None = None
    wattAccumulated: float32 | None = None
    wattAccumulatedControlPoint: float32 | None = None
    voltage: float32 | None = None
    current: float32 | None = None

    class Attributes:
        """Attributes for the EveEnergy Cluster."""

        @dataclass
        class Watt(ClusterAttributeDescriptor, CustomClusterAttribute):
            """Watt Attribute within the EveEnergy Cluster."""

            @ChipUtility.classproperty
            def cluster_id(cls) -> int:
                """Return cluster id."""
                return 0x130AFC01

            @ChipUtility.classproperty
            def attribute_id(cls) -> int:
                """Return attribute id."""
                return 0x130A000A

            @ChipUtility.classproperty
            def attribute_type(cls) -> ClusterObjectFieldDescriptor:
                """Return attribute type."""
                return ClusterObjectFieldDescriptor(Type=float32)

            value: float32 = 0

        @dataclass
        class WattAccumulated(ClusterAttributeDescriptor, CustomClusterAttribute):
            """WattAccumulated Attribute within the EveEnergy Cluster."""

            @ChipUtility.classproperty
            def cluster_id(cls) -> int:
                """Return cluster id."""
                return 0x130AFC01

            @ChipUtility.classproperty
            def attribute_id(cls) -> int:
                """Return attribute id."""
                return 0x130A000B

            @ChipUtility.classproperty
            def attribute_type(cls) -> ClusterObjectFieldDescriptor:
                """Return attribute type."""
                return ClusterObjectFieldDescriptor(Type=float32)

            value: float32 = 0

        @dataclass
        class wattAccumulatedControlPoint(
            ClusterAttributeDescriptor, CustomClusterAttribute
        ):
            """wattAccumulatedControlPoint Attribute within the EveEnergy Cluster."""

            @ChipUtility.classproperty
            def cluster_id(cls) -> int:
                """Return cluster id."""
                return 0x130AFC01

            @ChipUtility.classproperty
            def attribute_id(cls) -> int:
                """Return attribute id."""
                return 0x130A000E

            @ChipUtility.classproperty
            def attribute_type(cls) -> ClusterObjectFieldDescriptor:
                """Return attribute type."""
                return ClusterObjectFieldDescriptor(Type=float32)

            value: float32 = 0

        @dataclass
        class Voltage(ClusterAttributeDescriptor, CustomClusterAttribute):
            """Voltage Attribute within the EveEnergy Cluster."""

            @ChipUtility.classproperty
            def cluster_id(cls) -> int:
                """Return cluster id."""
                return 0x130AFC01

            @ChipUtility.classproperty
            def attribute_id(cls) -> int:
                """Return attribute id."""
                return 0x130A0008

            @ChipUtility.classproperty
            def attribute_type(cls) -> ClusterObjectFieldDescriptor:
                """Return attribute type."""
                return ClusterObjectFieldDescriptor(Type=float32)

            value: float32 = 0

        @dataclass
        class Current(ClusterAttributeDescriptor, CustomClusterAttribute):
            """Current Attribute within the EveEnergy Cluster."""

            @ChipUtility.classproperty
            def cluster_id(cls) -> int:
                """Return cluster id."""
                return 0x130AFC01

            @ChipUtility.classproperty
            def attribute_id(cls) -> int:
                """Return attribute id."""
                return 0x130A0009

            @ChipUtility.classproperty
            def attribute_type(cls) -> ClusterObjectFieldDescriptor:
                """Return attribute type."""
                return ClusterObjectFieldDescriptor(Type=float32)

            value: float32 = 0
