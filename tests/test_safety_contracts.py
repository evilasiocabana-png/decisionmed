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
    SafetyCheckProviderBinding,
    SafetyCheckProviderRegistry,
    SafetyCheckRegistry,
    SafetyCheckResult,
    SafetyCheckSpecification,
    SafetyCheckStatus,
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
    evidence_source_ids: tuple[str, ...] | None = None,
    trace_id: str = "trace.run",
) -> SafetyCheckResult:
    return SafetyCheckResult(
        check_id=check_id,
        outcome=outcome,
        trace_id=trace_id,
        explanation="Synthetic structural result for contract tests.",
        evidence_source_ids=(
            evidence_source_ids
            if evidence_source_ids is not None
            else ("source.safety-fixture",)
            if outcome is not SafetyCheckOutcome.NOT_EVALUATED
            else ()
        ),
        findings=findings,
    )


class SafetyCoordinatorTest(unittest.TestCase):
    def configuration(
        self,
    ) -> tuple[SafetyCheckProviderRegistry, EvidenceRegistry]:
        evidence_registry = EvidenceRegistry((evidence(),))
        specifications = SafetyCheckRegistry(
            evidence_registry,
            tuple(
                self.specification(check_id, EvidenceStatus.VALIDATED)
                for check_id in ("check.alpha", "check.beta")
            ),
        )
        providers = SafetyCheckProviderRegistry(
            specifications,
            tuple(
                SafetyCheckProviderBinding(
                    check_id,
                    f"decisionmed.safety.{check_id.removeprefix('check.')}",
                    "0.1.0",
                )
                for check_id in ("check.alpha", "check.beta")
            ),
        )
        return providers, evidence_registry

    def coordinator(self) -> SafetyCoordinator:
        providers, evidence_registry = self.configuration()
        return SafetyCoordinator(providers, evidence_registry)

    @staticmethod
    def specification(
        check_id: str, evidence_status: EvidenceStatus
    ) -> SafetyCheckSpecification:
        validated = evidence_status is EvidenceStatus.VALIDATED
        return SafetyCheckSpecification(
            check_id=check_id,
            specialty_key="cardiology",
            purpose="Synthetic aggregation contract without a clinical rule.",
            limits="Structural test only; does not authorize clinical execution.",
            evidence_source_ids=("source.safety-fixture",),
            version="0.1.0",
            status=SafetyCheckStatus.VALIDATED if validated else SafetyCheckStatus.DRAFT,
            reviewed_on=date.today() if validated else None,
            validated_by="reviewer.synthetic" if validated else None,
            review_due_on=date.today() + timedelta(days=30) if validated else None,
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
        providers, _ = self.configuration()
        evidence_registry = EvidenceRegistry((evidence(EvidenceStatus.DRAFT),))
        assessment = SafetyCoordinator(providers, evidence_registry).assess(
            (result("check.alpha"), result("check.beta")), "trace.run"
        )

        self.assertEqual(SafetyGateStatus.INCOMPLETE, assessment.status)
        self.assertIn("unvalidated_evidence:check.alpha", assessment.blocking_reasons)

    def test_incomplete_provider_coverage_rejects_coordinator(self) -> None:
        _, evidence_registry = self.configuration()
        specifications = SafetyCheckRegistry(
            evidence_registry,
            (self.specification("check.alpha", EvidenceStatus.VALIDATED),),
        )
        with self.assertRaises(SafetyError) as incomplete:
            SafetyCoordinator(
                SafetyCheckProviderRegistry(specifications), evidence_registry
            )

        self.assertEqual("safety.provider_coverage", incomplete.exception.code)

        incompatible = SafetyCheckProviderRegistry(
            specifications,
            (
                SafetyCheckProviderBinding(
                    "check.alpha", "decisionmed.safety.alpha", "0.2.0"
                ),
            ),
        )
        with self.assertRaises(SafetyError) as version_mismatch:
            SafetyCoordinator(incompatible, evidence_registry)
        self.assertEqual(
            "safety.provider_coverage", version_mismatch.exception.code
        )

    def test_undeclared_evidence_keeps_assessment_incomplete(self) -> None:
        registry = EvidenceRegistry(
            (
                evidence(),
                EvidenceSource(
                    source_id="source.other-fixture",
                    title="Other validated synthetic evidence",
                    publication_year=2025,
                    evidence_type=EvidenceType.OTHER,
                    evidence_quality=EvidenceQuality.INSUFFICIENT,
                    recommendation_strength=(
                        RecommendationStrength.INSUFFICIENT_FOR_RECOMMENDATION
                    ),
                    locator="test-only:other-safety-fixture",
                    version="0.1.0",
                    status=EvidenceStatus.VALIDATED,
                    specialties=("cardiology",),
                    reviewed_on=date.today(),
                    known_conflicts="Synthetic fixture.",
                    clinical_applicability="Contract tests only.",
                    review_due_on=date.today() + timedelta(days=30),
                ),
            )
        )
        specifications = SafetyCheckRegistry(
            registry,
            tuple(
                self.specification(check_id, EvidenceStatus.VALIDATED)
                for check_id in ("check.alpha", "check.beta")
            ),
        )
        providers = SafetyCheckProviderRegistry(
            specifications,
            tuple(
                SafetyCheckProviderBinding(
                    check_id,
                    f"decisionmed.safety.{check_id.removeprefix('check.')}",
                    "0.1.0",
                )
                for check_id in ("check.alpha", "check.beta")
            ),
        )

        assessment = SafetyCoordinator(providers, registry).assess(
            (
                result(
                    "check.alpha",
                    evidence_source_ids=("source.other-fixture",),
                ),
                result("check.beta"),
            ),
            "trace.run",
        )

        self.assertEqual(SafetyGateStatus.INCOMPLETE, assessment.status)
        self.assertIn("undeclared_evidence:check.alpha", assessment.blocking_reasons)

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

    def test_result_requires_an_explanation(self) -> None:
        for invalid in ("", "x" * 4001):
            with self.subTest(length=len(invalid)):
                with self.assertRaises(SafetyError) as missing:
                    SafetyCheckResult(
                        check_id="check.alpha",
                        outcome=SafetyCheckOutcome.NOT_EVALUATED,
                        trace_id="trace.run",
                        explanation=invalid,
                    )

                self.assertEqual("safety.explanation", missing.exception.code)

    def test_result_from_another_trace_is_rejected(self) -> None:
        with self.assertRaises(SafetyError) as mismatch:
            self.coordinator().assess(
                (
                    result("check.alpha", trace_id="trace.other-run"),
                    result("check.beta"),
                ),
                "trace.run",
            )

        self.assertEqual("safety.trace_mismatch", mismatch.exception.code)


if __name__ == "__main__":
    unittest.main()
