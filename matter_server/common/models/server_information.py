"""Represents the version from the server."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from chip.clusters import Attribute

from .device import MatterNode


@dataclass
class ServerInfo:
    """Base server information including versions."""

    fabricId: int
    compressedFabricId: int
    schema_version: int
    sdk_version: str


@dataclass
class ServerDiagnostics:
    """Full dump of the server information and data."""

    info: ServerInfo
    nodes: list[MatterNode]
    events: list[Attribute.EventReadResult]
