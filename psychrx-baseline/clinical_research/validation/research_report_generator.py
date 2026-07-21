"""Research report generator."""

from __future__ import annotations

from clinical_research.models import ResearchMetrics, ResearchReport


class ResearchReportGenerator:
    def generate(self, metrics: ResearchMetrics) -> ResearchReport:
        return ResearchReport(
            metrics=metrics,
            limitations=("research_environment_only", "no_clinical_execution"),
            known_issues=(),
            promotion_recommendation="governance_review_required",
        )

