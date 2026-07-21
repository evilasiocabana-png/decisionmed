"""Completeness analyzer."""

from __future__ import annotations

from collections.abc import Mapping

from clinical_quality.models import QualityDimension


class CompletenessAnalyzer:
    """Validates that required structural engine outputs exist."""

    REQUIRED = (
        "safety_result",
        "evidence_result",
        "optimization_result",
        "explanation_result",
        "clinical_snapshot",
        "clinical_timeline",
        "clinical_navigation",
        "clinical_operating_mind",
    )

    def analyze(self, runtime_output: Mapping[str, object]) -> QualityDimension:
        missing = tuple(key for key in self.REQUIRED if key not in runtime_output)
        score = 1.0 if not missing else round((len(self.REQUIRED) - len(missing)) / len(self.REQUIRED), 3)
        return QualityDimension(
            name="completeness",
            status="valid" if not missing else "incomplete",
            score=score,
            details=tuple(f"missing:{key}" for key in missing),
        )

