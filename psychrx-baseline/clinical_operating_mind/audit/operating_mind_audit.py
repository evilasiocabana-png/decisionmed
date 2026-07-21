"""In-memory audit log for Clinical Operating Mind."""

from __future__ import annotations

from clinical_operating_mind.models import OperatingMindAudit


class OperatingMindAuditLog:
    """Records structural lifecycle and validation events."""

    def __init__(self) -> None:
        self._entries: list[OperatingMindAudit] = []

    def record(self, entry: OperatingMindAudit) -> None:
        self._entries.append(entry)

    def snapshot(self) -> tuple[OperatingMindAudit, ...]:
        return tuple(self._entries)

