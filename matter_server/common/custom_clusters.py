"""Definitions for custom (vendor specific) Matter clusters."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from chip import ChipUtility
from chip.clusters.ClusterObjects import (
    Cluster,
    ClusterAttributeDescriptor,
    ClusterObjectDescriptor,
    ClusterObjectFieldDescriptor,
)
from chip.tlv import float32

from matter_server.common.helpers.util import parse_attribute_path

if TYPE_CHECKING:
    from matter_server.common.models import MatterNodeData


# pylint: disable=invalid-name,arguments-renamed,no-self-argument
# mypy: ignore_errors=true


ALL_CUSTOM_CLUSTERS: dict[int, Cluster] = {}
ALL_CUSTOM_ATTRIBUTES: dict[int, dict[int, ClusterAttributeDescriptor]] = {}


@dataclass
class CustomClusterMixin:
    """Base model for a vendor specific custom cluster."""

    id: ClassVar[int]  # cluster id
    should_poll: bool = False  # should the entire cluster be polled for state changes?

    def __init_subclass__(cls: Cluster, *args, **kwargs) -> None:
        """Register a subclass."""
        super().__init_subclass__(*args, **kwargs)
        ALL_CUSTOM_CLUSTERS[cls.id] = cls


@dataclass
class CustomClusterAttributeMixin:
    """Base model for a vendor specific custom cluster attribute."""

    should_poll: bool = False  # should this attribute be polled ?

    def __init_subclass__(cls: ClusterAttributeDescriptor, *args, **kwargs) -> None:
        """Register a subclass."""
        super().__init_subclass__(*args, **kwargs)
        if cls.cluster_id not in ALL_CUSTOM_ATTRIBUTES:
            ALL_CUSTOM_ATTRIBUTES[cls.cluster_id] = {}
        ALL_CUSTOM_ATTRIBUTES[cls.cluster_id][cls.attribute_id] = cls


@dataclass
class EveCluster(Cluster, CustomClusterMixin):
    """Custom (vendor-specific) cluster for Eve - Vendor ID 4874 (0x130a)."""

    id: ClassVar[int] = 0x130AFC01

    @ChipUtility.classproperty
    def descriptor(cls) -> ClusterObjectDescriptor:
        """Return descriptor for this cluster."""
        return ClusterObjectDescriptor(
            Fields=[
                ClusterObjectFieldDescriptor(
                    Label="timesOpened", Tag=0x130A0006, Type=int
                ),
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

    timesOpened: int | None = None
    watt: float32 | None = None
    wattAccumulated: float32 | None = None
    wattAccumulatedControlPoint: float32 | None = None
    voltage: float32 | None = None
    current: float32 | None = None

    class Attributes:
        """Attributes for the Eve Cluster."""

        @dataclass
        class TimesOpened(ClusterAttributeDescriptor, CustomClusterAttributeMixin):
            """TimesOpened Attribute within the Eve Cluster."""

            should_poll = True

            @ChipUtility.classproperty
            def cluster_id(cls) -> int:
                """Return cluster id."""
                return 0x130AFC01

            @ChipUtility.classproperty
            def attribute_id(cls) -> int:
                """Return attribute id."""
                return 0x130A0006

            @ChipUtility.classproperty
            def attribute_type(cls) -> ClusterObjectFieldDescriptor:
                """Return attribute type."""
                return ClusterObjectFieldDescriptor(Type=int)

            value: int = 0

        @dataclass
        class Watt(ClusterAttributeDescriptor, CustomClusterAttributeMixin):
            """Watt Attribute within the Eve Cluster."""

            should_poll = True

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
        class WattAccumulated(ClusterAttributeDescriptor, CustomClusterAttributeMixin):
            """WattAccumulated Attribute within the Eve Cluster."""

            should_poll = True

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
        class WattAccumulatedControlPoint(
            ClusterAttributeDescriptor, CustomClusterAttributeMixin
        ):
            """wattAccumulatedControlPoint Attribute within the Eve Cluster."""

            should_poll = True

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
        class Voltage(ClusterAttributeDescriptor, CustomClusterAttributeMixin):
            """Voltage Attribute within the Eve Cluster."""

            should_poll = True

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
        class Current(ClusterAttributeDescriptor, CustomClusterAttributeMixin):
            """Current Attribute within the Eve Cluster."""

            should_poll = True

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


@dataclass
class NeoCluster(Cluster, CustomClusterMixin):
    """Custom (vendor-specific) cluster for Neo - Vendor ID 4991 (0x137F)."""

    id: ClassVar[int] = 0x00125DFC11

    @ChipUtility.classproperty
    def descriptor(cls) -> ClusterObjectDescriptor:
        """Return descriptor for this cluster."""
        return ClusterObjectDescriptor(
            Fields=[
                ClusterObjectFieldDescriptor(
                    Label="wattAccumulated", Tag=0x00125D0021, Type=float32
                ),
                ClusterObjectFieldDescriptor(
                    Label="watt", Tag=0x00125D0023, Type=float32
                ),
                ClusterObjectFieldDescriptor(
                    Label="current", Tag=0x00125D0022, Type=float32
                ),
                ClusterObjectFieldDescriptor(
                    Label="voltage", Tag=0x00125D0024, Type=float32
                ),
            ]
        )

    watt: float32 | None = None
    wattAccumulated: float32 | None = None
    voltage: float32 | None = None
    current: float32 | None = None

    class Attributes:
        """Attributes for the Neo Cluster."""

        @dataclass
        class Watt(ClusterAttributeDescriptor, CustomClusterAttributeMixin):
            """Watt Attribute within the Neo Cluster."""

            @ChipUtility.classproperty
            def cluster_id(cls) -> int:
                """Return cluster id."""
                return 0x00125DFC11

            @ChipUtility.classproperty
            def attribute_id(cls) -> int:
                """Return attribute id."""
                return 0x00125D0023

            @ChipUtility.classproperty
            def attribute_type(cls) -> ClusterObjectFieldDescriptor:
                """Return attribute type."""
                return ClusterObjectFieldDescriptor(Type=float32)

            value: float32 = 0

        @dataclass
        class WattAccumulated(ClusterAttributeDescriptor, CustomClusterAttributeMixin):
            """WattAccumulated Attribute within the Neo Cluster."""

            @ChipUtility.classproperty
            def cluster_id(cls) -> int:
                """Return cluster id."""
                return 0x00125DFC11

            @ChipUtility.classproperty
            def attribute_id(cls) -> int:
                """Return attribute id."""
                return 0x00125D0021

            @ChipUtility.classproperty
            def attribute_type(cls) -> ClusterObjectFieldDescriptor:
                """Return attribute type."""
                return ClusterObjectFieldDescriptor(Type=float32)

            value: float32 = 0

        @dataclass
        class Voltage(ClusterAttributeDescriptor, CustomClusterAttributeMixin):
            """Voltage Attribute within the Neo Cluster."""

            @ChipUtility.classproperty
            def cluster_id(cls) -> int:
                """Return cluster id."""
                return 0x00125DFC11

            @ChipUtility.classproperty
            def attribute_id(cls) -> int:
                """Return attribute id."""
                return 0x00125D0024

            @ChipUtility.classproperty
            def attribute_type(cls) -> ClusterObjectFieldDescriptor:
                """Return attribute type."""
                return ClusterObjectFieldDescriptor(Type=float32)

            value: float32 = 0

        @dataclass
        class Current(ClusterAttributeDescriptor, CustomClusterAttributeMixin):
            """Current Attribute within the Neo Cluster."""

            @ChipUtility.classproperty
            def cluster_id(cls) -> int:
                """Return cluster id."""
                return 0x00125DFC11

            @ChipUtility.classproperty
            def attribute_id(cls) -> int:
                """Return attribute id."""
                return 0x00125D0022

            @ChipUtility.classproperty
            def attribute_type(cls) -> ClusterObjectFieldDescriptor:
                """Return attribute type."""
                return ClusterObjectFieldDescriptor(Type=float32)

            value: float32 = 0


def check_polled_attributes(node_data: MatterNodeData) -> set[str]:
    """Check if custom attributes are present in the node data that need to be polled."""
    attributes_to_poll: set[str] = set()
    for attr_path in node_data.attributes:
        endpoint_id, cluster_id, attribute_id = parse_attribute_path(attr_path)
        if not (custom_cluster := ALL_CUSTOM_CLUSTERS.get(cluster_id)):
            continue
        if custom_cluster.should_poll:
            # the entire cluster needs to be polled
            attributes_to_poll.add(f"{endpoint_id}/{cluster_id}/*")
            continue
        custom_attribute = ALL_CUSTOM_ATTRIBUTES[cluster_id].get(attribute_id)
        if custom_attribute and custom_attribute.should_poll:
            # this attribute needs to be polled
            attributes_to_poll.add(attr_path)
    return attributes_to_poll
