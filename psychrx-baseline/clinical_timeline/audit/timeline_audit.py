"""Timeline audit."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class TimelineAuditEntry:
    event: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    timeline_id: str = ""
    trace_id: str = ""


@dataclass
class TimelineAudit:
    entries: list[TimelineAuditEntry] = field(default_factory=list)

    def record(self, entry: TimelineAuditEntry) -> None:
        self.entries.append(entry)

    def snapshot(self) -> tuple[TimelineAuditEntry, ...]:
        return tuple(self.entries)
