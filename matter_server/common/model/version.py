"""Represents the version from the server."""

from dataclasses import dataclass


@dataclass
class VersionInfo:
    """Version info of the server."""

    driver_version: str
    server_version: str
    min_schema_version: int
    max_schema_version: int
