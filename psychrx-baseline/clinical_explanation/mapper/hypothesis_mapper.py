"""Therapeutic hypothesis explanation mapper."""

from __future__ import annotations

from typing import Any

from clinical_explanation.models import ExplanationNode, ExplanationSource


class TherapeuticHypothesisMapper:
    """Maps optimization output into explanation nodes."""

    def map(self, optimization_result: dict[str, Any]) -> tuple[ExplanationNode, ...]:
        hypotheses = optimization_result.get("hypotheses", ())
        uncertainties = optimization_result.get("uncertainties", ())
        return (
            ExplanationNode(
                node_id="hypothesis-summary",
                title="Therapeutic hypotheses",
                text=(
                    f"TherapeuticOptimizationResult generated {len(hypotheses)} "
                    f"hypotheses for physician review with {len(uncertainties)} uncertainties."
                ),
                source=ExplanationSource("optimization", "therapeutic_optimization_result"),
            ),
        )
