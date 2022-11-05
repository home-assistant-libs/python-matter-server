"""Models for events sent by the server."""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class EventType(Enum):
    """Enum with possible events sent from server to client."""

    NODE_ADDED = "node_added"
    NODE_UPDATED = "node_updated"
    NODE_DELETED = "node_deleted"
    SERVER_SHUTDOWN = "server_shutdown"


@dataclass
class ServerEvent:
    """Event sent from server to the client."""

    type: EventType
    data: Any
