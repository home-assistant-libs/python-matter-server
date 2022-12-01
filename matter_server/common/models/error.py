"""Various models for errors."""


class MatterError(Exception):
    """Generic Matter exception."""


class NodeCommissionFailed(MatterError):
    """Error raised when interview of a device failed."""


class NodeInterviewFailed(MatterError):
    """Error raised when interview of a device failed."""


class NodeNotReady(MatterError):
    """Error raised when performing action on node that has not been fully added."""


class NodeNotResolving(MatterError):
    """Error raised when resolving the node fails."""


class NodeNotExists(MatterError):
    """Error raised when performing action on node that does not exist."""


class VersionMismatch(MatterError):
    """Issue raised when SDK version mismatches."""


class SDKCommandFailed(MatterError):
    """Raised when command on the CHIP SDK Failed."""
