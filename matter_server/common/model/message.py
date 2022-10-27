"""Models for the Websocket messages."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from enum import Enum, IntEnum


@dataclass
class Message:
    pass


@dataclass
class ResultMessage:
    messageId: str


@dataclass
class SuccessResultMessage(ResultMessage):
    result: Any


class ErrorCode(IntEnum):
    """Enum with possible error codes."""

    INVALID_COMMAND = 1
    NOT_FOUND = 2
    UNKNOWN_ERROR = 99


@dataclass
class ErrorResultMessage(ResultMessage):
    errorCode: ErrorCode
    details: str | None = None


@dataclass
class SubscriptionReportMessage(Message):
    subscriptionId: str
    payload: Any


@dataclass
class CommandMessage(Message):
    messageId: str
    command: str
    args: dict[str, Any]


@dataclass
class ServerInformation:
    fabricId: int
    compressedFabricId: int


class EventType(Enum):
    """Enum with possible events sent from server to client."""

    DEVICE_ADDED = "device_added"
    DEVICE_UPDATED = "device_updated"
    DEVICE_DELETED = "device_deleted"


@dataclass
class ServerEvent:
    """Event sent from server to the client."""

    type: EventType
    data: Any
