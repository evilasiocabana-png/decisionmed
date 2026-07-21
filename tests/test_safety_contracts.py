from datetime import date, timedelta
import unittest

from decisionmed.evidence import (
    EvidenceRegistry,
    EvidenceQuality,
    EvidenceSource,
    EvidenceStatus,
    EvidenceType,
    RecommendationStrength,
)
from decisionmed.safety import (
    SafetyCheckOutcome,
    SafetyCheckResult,
    SafetyCoordinator,
    SafetyError,
    SafetyFinding,
    SafetyGateStatus,
    SafetySeverity,
)


def evidence(status: EvidenceStatus = EvidenceStatus.VALIDATED) -> EvidenceSource:
    return EvidenceSource(
        source_id="source.safety-fixture",
        title="Synthetic metadata for structural safety tests",
        publication_year=2025,
        evidence_type=EvidenceType.OTHER,
        evidence_quality=EvidenceQuality.INSUFFICIENT,
        recommendation_strength=RecommendationStrength.INSUFFICIENT_FOR_RECOMMENDATION,
        locator="test-only:safety-fixture",
        version="0.1.0",
        status=status,
        specialties=("cardiology",),
        reviewed_on=date(2026, 7, 21),
        known_conflicts="No conflicts assessed; synthetic fixture.",
        clinical_applicability="Contract tests only.",
        review_due_on=(
            date.today() + timedelta(days=30)
            if status is EvidenceStatus.VALIDATED
            else None
        ),
    )


def result(
    check_id: str,
    outcome: SafetyCheckOutcome = SafetyCheckOutcome.PASSED,
    findings: tuple[SafetyFinding, ...] = (),
) -> SafetyCheckResult:
    return SafetyCheckResult(
        check_id=check_id,
        outcome=outcome,
        trace_id=f"trace.{check_id}",
        evidence_source_ids=("source.safety-fixture",)
        if outcome is not SafetyCheckOutcome.NOT_EVALUATED
        else (),
        findings=findings,
    )


class SafetyCoordinatorTest(unittest.TestCase):
    def coordinator(
        self, status: EvidenceStatus = EvidenceStatus.VALIDATED
    ) -> SafetyCoordinator:
        return SafetyCoordinator(
            ("check.alpha", "check.beta"), EvidenceRegistry((evidence(status),))
        )

    def test_missing_or_not_evaluated_checks_fail_closed(self) -> None:
        missing = self.coordinator().assess((result("check.alpha"),), "trace.run")
        not_evaluated = self.coordinator().assess(
            (
                result("check.alpha"),
                result("check.beta", SafetyCheckOutcome.NOT_EVALUATED),
            ),
            "trace.run",
        )

        self.assertEqual(SafetyGateStatus.INCOMPLETE, missing.status)
        self.assertEqual(("check.beta",), missing.missing_check_ids)
        self.assertEqual(SafetyGateStatus.INCOMPLETE, not_evaluated.status)
        self.assertFalse(missing.clinical_execution_allowed)

    def test_unvalidated_evidence_keeps_assessment_incomplete(self) -> None:
        assessment = self.coordinator(EvidenceStatus.DRAFT).assess(
            (result("check.alpha"), result("check.beta")), "trace.run"
        )

        self.assertEqual(SafetyGateStatus.INCOMPLETE, assessment.status)
        self.assertIn("unvalidated_evidence:check.alpha", assessment.blocking_reasons)

    def test_critical_finding_blocks_but_does_not_decide_clinically(self) -> None:
        finding = SafetyFinding(
            "finding.synthetic-critical",
            SafetySeverity.CRITICAL,
            "Synthetic critical finding used only to test gate precedence.",
            ("source.safety-fixture",),
        )
        assessment = self.coordinator().assess(
            (
                result("check.alpha", SafetyCheckOutcome.FINDING, (finding,)),
                result("check.beta"),
            ),
            "trace.run",
        )

        self.assertEqual(SafetyGateStatus.BLOCKED, assessment.status)
        self.assertIn(
            "critical_finding:finding.synthetic-critical", assessment.blocking_reasons
        )
        self.assertFalse(assessment.clinical_execution_allowed)

    def test_noncritical_finding_requires_human_review(self) -> None:
        finding = SafetyFinding(
            "finding.synthetic-caution",
            SafetySeverity.CAUTION,
            "Synthetic caution used only to test structural aggregation.",
            ("source.safety-fixture",),
        )
        assessment = self.coordinator().assess(
            (
                result("check.alpha", SafetyCheckOutcome.FINDING, (finding,)),
                result("check.beta"),
            ),
            "trace.run",
        )

        self.assertEqual(SafetyGateStatus.HUMAN_REVIEW_REQUIRED, assessment.status)
        self.assertIn(
            "finding:finding.synthetic-caution", assessment.blocking_reasons
        )
        self.assertFalse(assessment.clinical_execution_allowed)

    def test_all_structural_checks_only_reach_human_review(self) -> None:
        assessment = self.coordinator().assess(
            (result("check.alpha"), result("check.beta")), "trace.run"
        )

        self.assertEqual(SafetyGateStatus.READY_FOR_HUMAN_REVIEW, assessment.status)
        self.assertFalse(assessment.clinical_execution_allowed)

    def test_duplicate_or_unknown_results_are_rejected(self) -> None:
        with self.assertRaises(SafetyError):
            self.coordinator().assess(
                (result("check.alpha"), result("check.alpha")), "trace.run"
            )
        with self.assertRaises(SafetyError):
            self.coordinator().assess((result("check.unknown"),), "trace.run")


if __name__ == "__main__":
    unittest.main()
