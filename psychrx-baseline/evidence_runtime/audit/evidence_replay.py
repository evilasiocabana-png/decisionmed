"""Read-only Evidence Runtime replay."""

from __future__ import annotations

from evidence_runtime.audit.evidence_audit import EvidenceAuditEntry


class EvidenceReplay:
    """Replays audit entries without resolving or recalculating evidence."""

    def __init__(self, entries: tuple[EvidenceAuditEntry, ...]) -> None:
        self._entries = entries

    def replay(self) -> tuple[EvidenceAuditEntry, ...]:
        return self._entries
