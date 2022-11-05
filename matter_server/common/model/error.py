"""Various models for errors."""

class MatterError(Exception):
    """Generic Matter exception."""
    pass

class NodeCommissionFailed(MatterError):
    """Error raised when interview of a device failed."""

class NodeInterviewFailed(MatterError):
    """Error raised when interview of a device failed."""

class NodeNotReady(MatterError):
    """Error raised when performing action on node that has not been fully added."""

class NodeNotExists(MatterError):
    """Error raised when performing action on node that does not exist."""

