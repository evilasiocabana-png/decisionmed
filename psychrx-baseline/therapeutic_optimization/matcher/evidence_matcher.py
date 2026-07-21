"""Evidence matcher."""

from __future__ import annotations

from typing import Any

from therapeutic_optimization.models import CandidateStrategy


class EvidenceMatcher:
    """Associates EvidenceResult metadata with candidates without ranking."""

    def match(
        self,
        candidates: tuple[CandidateStrategy, ...],
        evidence_result: dict[str, Any],
    ) -> dict[str, tuple[str, ...]]:
        citations = tuple(
            citation.get("citation_id", "")
            for citation in evidence_result.get("citations", ())
            if isinstance(citation, dict)
        )
        return {candidate.strategy_id: citations for candidate in candidates}
