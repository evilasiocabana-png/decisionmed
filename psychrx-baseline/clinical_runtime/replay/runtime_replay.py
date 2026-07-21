"""Developer read-only runtime replay."""

from __future__ import annotations

from dataclasses import dataclass

from clinical_runtime.audit import RuntimeAuditEntry


@dataclass(frozen=True)
class RuntimeReplay:
    """Replay previous structural execution without modification."""

    entries: tuple[RuntimeAuditEntry, ...]

    def replay(self) -> tuple[RuntimeAuditEntry, ...]:
        return self.entries
