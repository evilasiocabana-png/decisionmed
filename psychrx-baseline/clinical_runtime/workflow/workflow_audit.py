"""In-memory structural workflow audit."""

from __future__ import annotations

from dataclasses import dataclass, field

from clinical_runtime.workflow.workflow_events import WorkflowEvent


@dataclass
class WorkflowAudit:
    """Record workflow events in memory only."""

    entries: list[WorkflowEvent] = field(default_factory=list)

    def record(self, event: WorkflowEvent) -> None:
        """Record a workflow event."""
        self.entries.append(event)

    def snapshot(self) -> tuple[dict[str, str | None], ...]:
        """Return JSON-safe audit snapshot."""
        return tuple(event.to_dict() for event in self.entries)

