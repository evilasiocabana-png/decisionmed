"""Coverage analyzer."""

from __future__ import annotations

from collections.abc import Mapping

from clinical_quality.models import QualityDimension


class CoverageAnalyzer:
    """Measures structural coverage without clinical interpretation."""

    AREAS = ("clinical_context", "constraints", "evidence", "hypotheses", "explanations")

    def analyze(self, payload: Mapping[str, object]) -> QualityDimension:
        covered = sum(1 for area in self.AREAS if area in payload)
        score = round(covered / len(self.AREAS), 3)
        return QualityDimension(
            name="coverage",
            status="valid" if score == 1.0 else "partial",
            score=score,
            details=tuple(f"covered:{area}" for area in self.AREAS if area in payload),
        )

