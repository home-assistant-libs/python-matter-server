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
