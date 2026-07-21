"""Publication gate for Clinical Quality."""

from __future__ import annotations

from clinical_quality.models import BlockingIssue, PublicationDecision, QualityMetrics, QualityWarning


class PublicationGate:
    """Produces explainable publication decisions."""

    def decide(
        self,
        metrics: QualityMetrics,
        blocking_issues: tuple[BlockingIssue, ...],
        warnings: tuple[QualityWarning, ...],
    ) -> PublicationDecision:
        if blocking_issues:
            return PublicationDecision(
                outcome="block_publication",
                explainable_reason="blocking_quality_issue",
                publish_allowed=False,
            )
        if metrics.average() < 0.75:
            return PublicationDecision(
                outcome="hold_publication",
                explainable_reason="quality_below_minimum",
                publish_allowed=False,
            )
        if warnings:
            return PublicationDecision(
                outcome="publish_with_warnings",
                explainable_reason="quality_valid_with_warnings",
                publish_allowed=True,
            )
        return PublicationDecision(
            outcome="publish",
            explainable_reason="quality_valid",
            publish_allowed=True,
        )

