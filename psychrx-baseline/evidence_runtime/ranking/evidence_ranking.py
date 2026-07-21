"""Evidence hierarchy ranking without clinical interpretation."""

from __future__ import annotations

from evidence_runtime.models import EVIDENCE_HIERARCHY, Evidence


class EvidenceRanking:
    """Orders evidence by documented hierarchy only."""

    def rank(self, evidence: tuple[Evidence, ...]) -> tuple[Evidence, ...]:
        order = {kind: index for index, kind in enumerate(EVIDENCE_HIERARCHY)}
        return tuple(sorted(evidence, key=lambda item: order.get(item.evidence_type, 999)))

    def explanation(self) -> tuple[str, ...]:
        return EVIDENCE_HIERARCHY
