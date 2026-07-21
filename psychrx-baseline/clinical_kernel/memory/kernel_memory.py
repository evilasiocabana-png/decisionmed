"""In-memory structural kernel memory."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class KernelMemory:
    """Session-local structural memory. It stores no real patient record."""

    events: list[str] = field(default_factory=list)

    def record(self, event: str) -> None:
        """Record a structural event label."""
        self.events.append(event)

    def snapshot(self) -> tuple[str, ...]:
        """Return immutable event labels."""
        return tuple(self.events)
