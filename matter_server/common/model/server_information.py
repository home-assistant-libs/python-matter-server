"""Represents the version from the server."""

from dataclasses import dataclass


@dataclass
class VersionInfo:
    """Version info of the server."""

    sdk_version: str
    server_version: str
    min_schema_version: int
    max_schema_version: int


@dataclass
class ServerInfo:
    """Base server information including versions."""
    fabricId: int
    compressedFabricId: int
    version: VersionInfo


@dataclass
class FullServerState(ServerInfo):
    """Full dump of the server information and data."""
    
