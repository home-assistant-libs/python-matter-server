"""Represents the version from the server."""

from dataclasses import dataclass

from .node import MatterNode


@dataclass
class ServerInfo:
    """Base server information including versions."""

    fabric_id: int
    compressed_fabric_id: int
    schema_version: int
    sdk_version: str
    wifi_credentials_set: bool
    thread_credentials_set: bool


@dataclass
class ServerDiagnostics:
    """Full dump of the server information and data."""

    info: ServerInfo
    nodes: list[MatterNode]
    events: list[dict]  # TODO !
