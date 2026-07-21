"""In-memory audit for Clinical Explanation Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class ExplanationAuditEntry:
    event: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    explanation_trace_id: str = ""
    runtime_trace_id: str = ""


@dataclass
class ExplanationAudit:
    entries: list[ExplanationAuditEntry] = field(default_factory=list)

    def record(self, entry: ExplanationAuditEntry) -> None:
        self.entries.append(entry)

    def snapshot(self) -> tuple[ExplanationAuditEntry, ...]:
        return tuple(self.entries)
