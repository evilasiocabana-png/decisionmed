"""Confidence calculator."""

from __future__ import annotations


class ConfidenceCalculator:
    """Calculates structural confidence from completeness dimensions."""

    def calculate(
        self,
        knowledge_completeness: float = 0.0,
        evidence_quality: float = 0.0,
        constraint_coverage: float = 0.0,
        missing_data: float = 1.0,
    ) -> float:
        raw = (
            knowledge_completeness
            + evidence_quality
            + constraint_coverage
            + max(0.0, 1.0 - missing_data)
        ) / 4.0
        return max(0.0, min(1.0, raw))
