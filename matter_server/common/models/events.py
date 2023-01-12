"""Models for events sent by the server and/or client."""

from enum import Enum
from typing import Any, Callable


class EventType(Enum):
    """Enum with possible events emitted by the Matter Server (or client)."""

    # server to client events
    NODE_ADDED = "node_added"
    NODE_DELETED = "node_deleted"
    NODE_EVENT = "node_event"
    ATTRIBUTE_UPDATED = "attribute_updated"
    SERVER_SHUTDOWN = "server_shutdown"
    # client-only events
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    INITIALIZED = "initialized"
    CONNECTION_LOST = "connection_lost"


EventCallBackType = Callable[[EventType, Any], None]
