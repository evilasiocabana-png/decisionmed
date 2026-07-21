"""Why included / excluded explanation helpers."""

from __future__ import annotations


class WhyExplanationEngine:
    """Uses existing traces only; performs no clinical inference."""

    def explain_included(self) -> str:
        return "This hypothesis is shown because it exists in the optimization trace and requires clinical judgment."

    def explain_excluded(self) -> str:
        return "This item is not shown as a hypothesis based on available data and structural trace status."

    def explain_limited_confidence(self) -> str:
        return "Confidence is limited when context, safety, evidence, or knowledge traces are incomplete."
