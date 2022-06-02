from dataclasses import dataclass, field


@dataclass
class Event:
    """Represent an event."""

    type: str
    data: dict = field(default_factory=dict)
