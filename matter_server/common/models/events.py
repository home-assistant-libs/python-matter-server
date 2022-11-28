"""Models for events sent by the server and/or client."""

from enum import Enum
from typing import Any, Callable


class EventType(Enum):
    """Enum with possible events sent from server to client."""

    NODE_ADDED = "node_added"
    NODE_UPDATED = "node_updated"
    NODE_DELETED = "node_deleted"
    SERVER_SHUTDOWN = "server_shutdown"


EventCallBackType = Callable[[EventType, Any], None]
