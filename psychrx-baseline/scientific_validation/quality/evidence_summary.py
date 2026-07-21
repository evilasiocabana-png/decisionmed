"""Evidence summary generator."""

from __future__ import annotations

from scientific_validation.models import QualityAssessment


class EvidenceSummaryGenerator:
    """Generates structured summaries without recommendations."""

    def generate(self, assessment: QualityAssessment, references: tuple[str, ...]) -> tuple[str, ...]:
        return (
            f"strength:{assessment.quality_level}",
            f"quality:{assessment.status}",
            f"references:{len(references)}",
            "recommendations:none",
        )

