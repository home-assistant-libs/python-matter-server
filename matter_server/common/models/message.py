"""Models for the Websocket messages."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Any, Type, Union

from ..helpers.util import dataclass_from_dict
from .events import EventType


@dataclass
class CommandMessage:
    """Model for a Message holding a command from server to client or client to server."""

    messageId: str
    command: str
    args: dict[str, Any] | None = None


@dataclass
class ResultMessageBase:
    """Base class for a result/response of a Command Message."""

    messageId: str


@dataclass
class SuccessResultMessage(ResultMessageBase):
    """Message sent when a Command has been succesfully executed."""

    result: Any


class ErrorCode(IntEnum):
    """Enum with possible error codes."""

    INVALID_COMMAND = 1
    NOT_FOUND = 2
    STACK_ERROR = 3
    UNKNOWN_ERROR = 99


@dataclass
class ErrorResultMessage(ResultMessageBase):
    """Message sent when a command did not execute succesfully"""

    errorCode: ErrorCode
    details: str | None = None


@dataclass
class EventMessage:
    """Message sent when server or client signals a (stateless) event."""

    event: EventType
    data: Any


MessageType = Union[
    CommandMessage, EventMessage, SuccessResultMessage, ErrorResultMessage
]


def parse_message(self, raw: dict) -> MessageType:
    """Parse Message from raw dict object."""
    if "event" in raw:
        return dataclass_from_dict(EventMessage, raw)
    if "errorCode" in raw:
        return dataclass_from_dict(ErrorResultMessage, raw)
    if "result" in raw:
        return dataclass_from_dict(SuccessResultMessage, raw)
    return dataclass_from_dict(CommandMessage, raw)
