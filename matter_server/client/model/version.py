"""Represents the version from the server."""

from dataclasses import dataclass

from ..const import TYPING_EXTENSION_FOR_TYPEDDICT_REQUIRED

if TYPING_EXTENSION_FOR_TYPEDDICT_REQUIRED:
    from typing_extensions import TypedDict
else:
    from typing import TypedDict


class VersionInfoDataType(TypedDict):
    """Version info data dict type."""

    driverVersion: str
    serverVersion: str
    minSchemaVersion: int
    maxSchemaVersion: int


@dataclass
class VersionInfo:
    """Version info of the server."""

    driver_version: str
    server_version: str
    min_schema_version: int
    max_schema_version: int

    @classmethod
    def from_message(cls, msg: VersionInfoDataType) -> "VersionInfo":
        """Create a version info from a version message."""
        return cls(
            driver_version=msg["driverVersion"],
            server_version=msg["serverVersion"],
            min_schema_version=msg["minSchemaVersion"],
            max_schema_version=msg["maxSchemaVersion"],
        )
