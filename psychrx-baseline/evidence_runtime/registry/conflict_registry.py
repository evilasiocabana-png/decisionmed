"""Conflict registry for scientific evidence disagreements."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class EvidenceConflict:
    conflict_id: str
    evidence_ids: tuple[str, ...]
    explanation: str = "Conflict registered for future scientific review."


@dataclass
class ConflictRegistry:
    """Records conflicts without arbitrating them."""

    _conflicts: list[EvidenceConflict] = field(default_factory=list)

    def register(self, conflict: EvidenceConflict) -> None:
        self._conflicts.append(conflict)

    def all(self) -> tuple[EvidenceConflict, ...]:
        return tuple(self._conflicts)
