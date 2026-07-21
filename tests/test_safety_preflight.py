from datetime import date, datetime, timedelta, timezone
import unittest

from decisionmed.domain import (
    ClinicalDataProvenance,
    ClinicalObservation,
    ClinicalSnapshot,
    ClinicalSnapshotSection,
    EntityId,
    SubjectReference,
)
from decisionmed.evidence import (
    EvidenceQuality,
    EvidenceRegistry,
    EvidenceSource,
    EvidenceStatus,
    EvidenceType,
    RecommendationStrength,
)
from decisionmed.safety import (
    SafetyCheckEvaluatorRegistry,
    SafetyCheckOutcome,
    SafetyCheckProviderBinding,
    SafetyCheckProviderRegistry,
    SafetyCheckRegistry,
    SafetyCheckResult,
    SafetyCheckSpecification,
    SafetyCheckStatus,
    SafetyError,
    SafetyGateStatus,
    SafetyPreflight,
)


class SyntheticEvaluator:
    check_id = "check.synthetic-preflight"
    provider = "decisionmed.safety.synthetic-preflight"
    specification_version = "0.1.0"

    def __init__(self, mode: str = "pass") -> None:
        self.mode = mode
        self.call_count = 0

    def evaluate(
        self, snapshot: ClinicalSnapshot, *, trace_id: str
    ) -> SafetyCheckResult:
        self.call_count += 1
        if self.mode == "raise":
            raise RuntimeError("synthetic evaluator failure")
        if self.mode == "wrong_type":
            return object()  # type: ignore[return-value]
        if self.mode == "wrong_trace":
            trace_id = "trace.other"
        return SafetyCheckResult(
            check_id="check.other" if self.mode == "wrong_check" else self.check_id,
            outcome=SafetyCheckOutcome.PASSED,
            trace_id=trace_id,
            evidence_source_ids=("source.synthetic-preflight",),
        )


class SafetyPreflightTest(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime.now(timezone.utc) - timedelta(seconds=1)
        self.evidence = EvidenceRegistry((self._evidence(),))
        self.providers = self._providers(self.evidence)

    def test_complete_snapshot_reaches_human_review_only(self) -> None:
        evaluator = SyntheticEvaluator()
        preflight = self._preflight(evaluator)

        assessment = preflight.run(self._snapshot(complete=True))

        self.assertEqual(SafetyGateStatus.READY_FOR_HUMAN_REVIEW, assessment.status)
        self.assertEqual(1, evaluator.call_count)
        self.assertFalse(assessment.clinical_execution_allowed)
        self.assertFalse(preflight.clinical_execution_allowed)

    def test_incomplete_or_wrong_specialty_snapshot_is_not_evaluated(self) -> None:
        for snapshot in (
            self._snapshot(complete=False),
            self._snapshot(complete=True, specialty_key="psychiatry"),
        ):
            evaluator = SyntheticEvaluator()
            assessment = self._preflight(evaluator).run(snapshot)

            self.assertEqual(SafetyGateStatus.INCOMPLETE, assessment.status)
            self.assertIn(
                "not_evaluated:check.synthetic-preflight",
                assessment.blocking_reasons,
            )
            self.assertEqual(0, evaluator.call_count)

    def test_evaluator_failure_or_invalid_result_fails_closed(self) -> None:
        for mode in ("raise", "wrong_type", "wrong_check", "wrong_trace"):
            evaluator = SyntheticEvaluator(mode)
            assessment = self._preflight(evaluator).run(
                self._snapshot(complete=True)
            )

            self.assertEqual(SafetyGateStatus.INCOMPLETE, assessment.status)
            self.assertIn(
                "not_evaluated:check.synthetic-preflight",
                assessment.blocking_reasons,
            )
            self.assertEqual(1, evaluator.call_count)

    def test_incomplete_evaluator_registry_cannot_start_preflight(self) -> None:
        incomplete = SafetyCheckEvaluatorRegistry(self.providers)

        with self.assertRaises(SafetyError) as coverage:
            SafetyPreflight(incomplete, self.evidence)

        self.assertEqual(
            "safety_preflight.evaluator_coverage", coverage.exception.code
        )

    def _preflight(self, evaluator: SyntheticEvaluator) -> SafetyPreflight:
        return SafetyPreflight(
            SafetyCheckEvaluatorRegistry(self.providers, (evaluator,)),
            self.evidence,
        )

    def _snapshot(
        self, *, complete: bool, specialty_key: str = "cardiology"
    ) -> ClinicalSnapshot:
        sections = tuple(ClinicalSnapshotSection) if complete else ()
        observations = tuple(
            ClinicalObservation(
                observation_id=EntityId(f"observation-{section.value}"),
                section=section,
                field_key=f"{section.value}.synthetic",
                value=False,
                provenance=ClinicalDataProvenance.CLINICIAN_ENTERED,
                observed_at=self.now,
            )
            for section in sections
        )
        return ClinicalSnapshot(
            snapshot_id=EntityId(f"snapshot-{specialty_key}-{len(sections)}"),
            lineage_id=EntityId("lineage-synthetic-preflight"),
            subject_reference=SubjectReference(
                "sub-0123456789abcdef0123456789abcdef"
            ),
            session_id=EntityId("session-synthetic-preflight"),
            specialty_key=specialty_key,
            captured_at=self.now,
            observations=observations,
            trace_id=f"trace.{specialty_key}.{len(sections)}",
        )

    @staticmethod
    def _evidence() -> EvidenceSource:
        return EvidenceSource(
            source_id="source.synthetic-preflight",
            title="Synthetic preflight evidence metadata",
            publication_year=2025,
            evidence_type=EvidenceType.OTHER,
            evidence_quality=EvidenceQuality.INSUFFICIENT,
            recommendation_strength=(
                RecommendationStrength.INSUFFICIENT_FOR_RECOMMENDATION
            ),
            locator="test-only:synthetic-preflight",
            version="0.1.0",
            status=EvidenceStatus.VALIDATED,
            specialties=("cardiology",),
            reviewed_on=date.today(),
            known_conflicts="Synthetic fixture.",
            clinical_applicability="Structural tests only.",
            review_due_on=date.today() + timedelta(days=30),
        )

    @staticmethod
    def _providers(evidence: EvidenceRegistry) -> SafetyCheckProviderRegistry:
        specifications = SafetyCheckRegistry(
            evidence,
            (
                SafetyCheckSpecification(
                    check_id="check.synthetic-preflight",
                    specialty_key="cardiology",
                    purpose="Synthetic preflight contract without a clinical rule.",
                    limits="Structural tests only; human review remains required.",
                    evidence_source_ids=("source.synthetic-preflight",),
                    version="0.1.0",
                    status=SafetyCheckStatus.VALIDATED,
                    reviewed_on=date.today(),
                    validated_by="reviewer.synthetic",
                    review_due_on=date.today() + timedelta(days=30),
                ),
            ),
        )
        return SafetyCheckProviderRegistry(
            specifications,
            (
                SafetyCheckProviderBinding(
                    "check.synthetic-preflight",
                    "decisionmed.safety.synthetic-preflight",
                    "0.1.0",
                ),
            ),
        )


if __name__ == "__main__":
    unittest.main()
