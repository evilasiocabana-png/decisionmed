"""In-memory Safety Engine audit trail."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class SafetyAuditEntry:
    event: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    trace_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SafetyAudit:
    """Records structural safety evaluations in memory only."""

    entries: list[SafetyAuditEntry] = field(default_factory=list)

    def record(self, entry: SafetyAuditEntry) -> None:
        self.entries.append(entry)

    def snapshot(self) -> tuple[SafetyAuditEntry, ...]:
        return tuple(self.entries)
