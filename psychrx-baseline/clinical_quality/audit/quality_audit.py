"""In-memory audit log for quality evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(frozen=True)
class QualityAuditEntry:
    event: str
    decision: str = ""
    trace_id: str = field(default_factory=lambda: f"CQ-AUD-{uuid4()}")
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class QualityAuditLog:
    def __init__(self) -> None:
        self._entries: list[QualityAuditEntry] = []

    def record(self, entry: QualityAuditEntry) -> None:
        self._entries.append(entry)

    def snapshot(self) -> tuple[QualityAuditEntry, ...]:
        return tuple(self._entries)

