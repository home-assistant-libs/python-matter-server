"""Exceptions for matter-server."""
from __future__ import annotations


class BaseMatterServerError(Exception):
    """Base Zwave JS Server exception."""


class TransportError(BaseMatterServerError):
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


class NotConnected(BaseMatterServerError):
    """Exception raised when not connected to client."""


class InvalidState(BaseMatterServerError):
    """Exception raised when data gets in invalid state."""


class InvalidMessage(BaseMatterServerError):
    """Exception raised when an invalid message is received."""


class InvalidServerVersion(BaseMatterServerError):
    """Exception raised when connected to server with incompatible version."""


class FailedCommand(BaseMatterServerError):
    """When a command has failed."""

    def __init__(self, message_id: str, error_code: str, msg: str | None = None):
        """Initialize a failed command error."""
        super().__init__(msg or f"Command failed: {error_code}")
        self.message_id = message_id
        self.error_code = error_code
