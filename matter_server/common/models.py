"""Models that are (serializeable) shared between server and client."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable

# Enums and constants


class EventType(Enum):
    """Enum with possible events sent from server to client."""

    NODE_ADDED = "node_added"
    NODE_UPDATED = "node_updated"
    NODE_DELETED = "node_deleted"
    NODE_EVENT = "node_event"
    ATTRIBUTE_UPDATED = "attribute_updated"
    SERVER_SHUTDOWN = "server_shutdown"


class APICommand(str, Enum):
    """Enum with all known API commands."""

    START_LISTENING = "start_listening"
    SERVER_DIAGNOSTICS = "diagnostics"
    SERVER_INFO = "server_info"
    GET_NODES = "get_nodes"
    GET_NODE = "get_node"
    COMMISSION_WITH_CODE = "commission_with_code"
    COMMISSION_ON_NETWORK = "commission_on_network"
    SET_WIFI_CREDENTIALS = "set_wifi_credentials"
    SET_THREAD_DATASET = "set_thread_dataset"
    OPEN_COMMISSIONING_WINDOW = "open_commissioning_window"
    DISCOVER = "discover"
    INTERVIEW_NODE = "interview_node"
    DEVICE_COMMAND = "device_command"
    REMOVE_NODE = "remove_node"
    GET_VENDOR_NAMES = "get_vendor_names"


EventCallBackType = Callable[[EventType, Any], None]

# Generic model(s)


@dataclass
class VendorInfo:
    """Vendor info as received from the CSA."""

    vendor_id: int
    vendor_name: str
    company_legal_name: str
    company_preferred_name: str
    vendor_landing_page_url: str
    creator: str


@dataclass
class MatterNodeData:
    """Matter node data as received from (and stored on) the server."""

    node_id: int
    date_commissioned: datetime
    last_interview: datetime
    interview_version: int
    available: bool = False
    # attributes are stored in form of AttributePath: ENDPOINT/CLUSTER_ID/ATTRIBUTE_ID
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass
class ServerDiagnostics:
    """Full dump of the server information and data."""

    info: ServerInfoMessage
    nodes: list[MatterNodeData]
    events: list[dict]


# API message models


@dataclass
class CommandMessage:
    """Model for a Message holding a command from server to client or client to server."""

    message_id: str
    command: str
    args: dict[str, Any] | None = None


@dataclass
class ResultMessageBase:
    """Base class for a result/response of a Command Message."""

    message_id: str


@dataclass
class SuccessResultMessage(ResultMessageBase):
    """Message sent when a Command has been successfully executed."""

    result: Any


@dataclass
class ErrorResultMessage(ResultMessageBase):
    """Message sent when a command did not execute successfully."""

    error_code: int
    details: str | None = None


@dataclass
class EventMessage:
    """Message sent when server or client signals a (stateless) event."""

    event: EventType
    data: Any


@dataclass
class ServerInfoMessage:
    """Message sent by the server with it's info when a client connects."""

    fabric_id: int
    compressed_fabric_id: int
    schema_version: int
    min_supported_schema_version: int
    sdk_version: str
    wifi_credentials_set: bool
    thread_credentials_set: bool


MessageType = (
    CommandMessage
    | EventMessage
    | SuccessResultMessage
    | ErrorResultMessage
    | ServerInfoMessage
)
