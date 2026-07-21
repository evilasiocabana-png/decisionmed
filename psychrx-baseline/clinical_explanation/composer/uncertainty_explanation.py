"""Uncertainty explanation builder."""

from __future__ import annotations

from clinical_explanation.models import ExplanationWarning


class UncertaintyExplanationBuilder:
    """Builds traceable uncertainty explanations."""

    categories = (
        "missing context",
        "missing evidence",
        "conflicting evidence",
        "safety limitation",
        "incomplete knowledge",
        "low confidence",
    )

    def build(self, category: str, origin: str) -> ExplanationWarning:
        return ExplanationWarning(
            category=category,
            message=f"Uncertainty requires clinical judgment. Origin: {origin}.",
        )
