"""Read-only optimization replay."""

from __future__ import annotations

from therapeutic_optimization.audit.optimization_audit import OptimizationAuditEntry


class OptimizationReplay:
    """Replays audit entries without recalculating hypotheses."""

    def __init__(self, entries: tuple[OptimizationAuditEntry, ...]) -> None:
        self._entries = entries

    def replay(self) -> tuple[OptimizationAuditEntry, ...]:
        return self._entries
