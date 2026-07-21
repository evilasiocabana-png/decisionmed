"""Optimization audit trail."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class OptimizationAuditEntry:
    event: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    candidate_strategies: tuple[str, ...] = field(default_factory=tuple)
    discarded_strategies: tuple[str, ...] = field(default_factory=tuple)
    scores: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    hypotheses: tuple[str, ...] = field(default_factory=tuple)
    trace_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class OptimizationAudit:
    """In-memory audit trail for optimization."""

    entries: list[OptimizationAuditEntry] = field(default_factory=list)

    def record(self, entry: OptimizationAuditEntry) -> None:
        self.entries.append(entry)

    def snapshot(self) -> tuple[OptimizationAuditEntry, ...]:
        return tuple(self.entries)
