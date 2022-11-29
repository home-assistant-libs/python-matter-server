"""Exceptions for matter-server."""
from __future__ import annotations

from ..common.models.error import MatterError

# TODO: merge these exceptions with the common ones


class TransportError(MatterError):
    """Exception raised to represent transport errors."""

    def __init__(self, message: str, error: Exception | None = None) -> None:
        """Initialize a transport error."""
        super().__init__(message)
        self.error = error


class ConnectionClosed(TransportError):
    """Exception raised when the connection is closed."""


class CannotConnect(TransportError):
    """Exception raised when failed to connect the client."""

    def __init__(self, error: Exception) -> None:
        """Initialize a cannot connect error."""
        super().__init__(f"{error}", error)


class ConnectionFailed(TransportError):
    """Exception raised when an established connection fails."""

    def __init__(self, error: Exception | None = None) -> None:
        """Initialize a connection failed error."""
        if error is None:
            super().__init__("Connection failed.")
            return
        super().__init__(f"{error}", error)


class NotConnected(MatterError):
    """Exception raised when not connected to client."""


class InvalidState(MatterError):
    """Exception raised when data gets in invalid state."""


class InvalidMessage(MatterError):
    """Exception raised when an invalid message is received."""


class InvalidServerVersion(MatterError):
    """Exception raised when connected to server with incompatible version."""


class FailedCommand(MatterError):
    """When a command has failed."""

    def __init__(self, message_id: str, error_code: str, msg: str | None = None):
        """Initialize a failed command error."""
        super().__init__(msg or f"Command failed: {error_code}")
        self.message_id = message_id
        self.error_code = error_code
