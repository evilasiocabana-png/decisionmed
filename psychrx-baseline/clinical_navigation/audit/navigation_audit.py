"""Navigation audit."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class NavigationAuditEntry:
    event: str
    route: str = ""
    context_switch: str = ""
    selection_change: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    trace_id: str = ""


@dataclass
class NavigationAudit:
    entries: list[NavigationAuditEntry] = field(default_factory=list)

    def record(self, entry: NavigationAuditEntry) -> None:
        self.entries.append(entry)

    def snapshot(self) -> tuple[NavigationAuditEntry, ...]:
        return tuple(self.entries)
