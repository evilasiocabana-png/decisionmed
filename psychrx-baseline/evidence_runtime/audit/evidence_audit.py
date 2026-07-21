"""In-memory audit trail for Evidence Runtime."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class EvidenceAuditEntry:
    event: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    query: dict[str, Any] = field(default_factory=dict)
    selected_evidence: tuple[str, ...] = field(default_factory=tuple)
    discarded_evidence: tuple[str, ...] = field(default_factory=tuple)
    versions: tuple[str, ...] = field(default_factory=tuple)
    trace_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EvidenceAudit:
    """Records runtime evidence use in memory only."""

    entries: list[EvidenceAuditEntry] = field(default_factory=list)

    def record(self, entry: EvidenceAuditEntry) -> None:
        self.entries.append(entry)

    def snapshot(self) -> tuple[EvidenceAuditEntry, ...]:
        return tuple(self.entries)
