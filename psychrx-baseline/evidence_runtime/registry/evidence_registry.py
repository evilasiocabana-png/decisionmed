"""In-memory evidence registry with no persistence."""

from __future__ import annotations

from dataclasses import dataclass, field

from evidence_runtime.models import Evidence


@dataclass
class EvidenceRegistry:
    """Registers evidence records made available by the knowledge layer."""

    version: str = "0.1-structural"
    _evidence: list[Evidence] = field(default_factory=list)

    def register(self, evidence: Evidence) -> None:
        self._evidence.append(evidence)

    def all(self) -> tuple[Evidence, ...]:
        return tuple(self._evidence)

    def lookup(self, evidence_id: str) -> Evidence | None:
        return next(
            (evidence for evidence in self._evidence if evidence.evidence_id == evidence_id),
            None,
        )

    def by_category(self, category: str) -> tuple[Evidence, ...]:
        return tuple(
            evidence
            for evidence in self._evidence
            if evidence.metadata.category == category
        )
