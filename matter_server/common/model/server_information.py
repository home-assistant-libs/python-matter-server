"""Represents the version from the server."""

from dataclasses import dataclass


@dataclass
class ServerInfo:
    """Base server information including versions."""
    fabricId: int
    compressedFabricId: int
    schema_version: int


@dataclass
class FullServerState(ServerInfo):
    """Full dump of the server information and data."""
    
