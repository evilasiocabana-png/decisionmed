"""Structural workflow events."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(frozen=True)
class WorkflowEvent:
    """Workflow event with no clinical payload."""

    name: str
    workflow_id: str
    node_id: str | None = None
    event_id: str = field(default_factory=lambda: f"WFE-{uuid4()}")
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, str | None]:
        """Return a JSON-safe representation."""
        return {
            "event_id": self.event_id,
            "name": self.name,
            "workflow_id": self.workflow_id,
            "node_id": self.node_id,
            "timestamp": self.timestamp,
        }


def default_workflow_events() -> tuple[str, ...]:
    """Return official structural workflow events."""
    return (
        "WorkflowStarted",
        "NodeEntered",
        "NodeExited",
        "WorkflowPaused",
        "WorkflowFinished",
    )

