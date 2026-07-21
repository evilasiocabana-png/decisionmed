"""Explainability validator."""

from __future__ import annotations

from collections.abc import Mapping

from clinical_quality.models import QualityDimension


class ExplainabilityValidator:
    """Checks structural explanation requirements."""

    def validate(self, runtime_output: Mapping[str, object]) -> QualityDimension:
        explanation = runtime_output.get("explanation_result", {})
        details: list[str] = []
        if not isinstance(explanation, Mapping):
            details.append("missing_explanation")
        else:
            if not explanation.get("sections"):
                details.append("missing_sections")
            if not explanation.get("trace"):
                details.append("missing_explanation_trace")
        return QualityDimension(
            name="explainability",
            status="valid" if not details else "incomplete",
            score=1.0 if not details else 0.5,
            details=tuple(details),
        )

