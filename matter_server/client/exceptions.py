"""Client-specific Exceptions for matter-server library."""

from __future__ import annotations


class MatterClientException(Exception):
    """Generic Matter exception."""


class TransportError(MatterClientException):
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


class NotConnected(MatterClientException):
    """Exception raised when not connected to client."""


class InvalidState(MatterClientException):
    """Exception raised when data gets in invalid state."""


class InvalidMessage(MatterClientException):
    """Exception raised when an invalid message is received."""


class InvalidServerVersion(MatterClientException):
    """Exception raised when connected to server with incompatible version."""

    def __init__(
        self,
        msg: str,
        client_schema_version: int,
        server_schema_version: int,
        min_supported_schema_version: int,
    ):
        """Initialize an invalid server version error."""
        super().__init__(msg)
        self.client_schema_version = client_schema_version
        self.server_schema_version = server_schema_version
        self.min_supported_schema_version = min_supported_schema_version
