"""Runtime audit trail."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class RuntimeAuditEntry:
    event: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RuntimeAudit:
    """In-memory audit trail. No database."""

    entries: list[RuntimeAuditEntry] = field(default_factory=list)

    def record(self, entry: RuntimeAuditEntry) -> None:
        self.entries.append(entry)

    def snapshot(self) -> tuple[RuntimeAuditEntry, ...]:
        return tuple(self.entries)
