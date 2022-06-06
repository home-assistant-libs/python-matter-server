from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    pass


@dataclass
class ResultMessage:
    messageId: str
    pass


@dataclass
class SuccessResultMessage(ResultMessage):
    result: Any


@dataclass
class ErrorResultMessage(ResultMessage):
    errorCode: Any


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
