"""Read-only replay support for Safety Engine audit snapshots."""

from __future__ import annotations

from safety_engine.audit.safety_audit import SafetyAuditEntry


class SafetyReplay:
    """Replays recorded audit entries without recalculating safety."""

    def __init__(self, entries: tuple[SafetyAuditEntry, ...]) -> None:
        self._entries = entries

    def replay(self) -> tuple[SafetyAuditEntry, ...]:
        return self._entries
