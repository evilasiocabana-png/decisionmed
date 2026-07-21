"""Snapshot audit."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class SnapshotAuditEntry:
    event: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    snapshot_id: str = ""
    runtime_id: str = ""
    trace_id: str = ""
    version: str = ""


@dataclass
class SnapshotAudit:
    entries: list[SnapshotAuditEntry] = field(default_factory=list)

    def record(self, entry: SnapshotAuditEntry) -> None:
        self.entries.append(entry)

    def snapshot(self) -> tuple[SnapshotAuditEntry, ...]:
        return tuple(self.entries)
