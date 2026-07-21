from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timedelta, timezone
import unittest

from decisionmed.domain import (
    ClinicalDataProvenance,
    ClinicalObservation,
    ClinicalSnapshot,
    ClinicalSnapshotSection,
    EntityId,
    SubjectReference,
)
from decisionmed.reasoning import (
    ReasoningError,
    ReasoningGate,
    ReasoningInputEnvelope,
)
from decisionmed.safety import (
    SafetyAssessment,
    SafetyCheckOutcome,
    SafetyCheckResult,
    SafetyGateStatus,
    SafetyReviewDisposition,
    SafetyReviewRecord,
    safety_assessment_fingerprint,
)


class ReasoningInputEnvelopeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.snapshot_time = datetime.now(timezone.utc) - timedelta(seconds=2)
        self.review_time = datetime.now(timezone.utc) - timedelta(seconds=1)
        self.prepared_at = datetime.now(timezone.utc) - timedelta(milliseconds=100)
        self.snapshot = self._snapshot()
        self.safety = self._safety(self.snapshot)
        self.review = self._review(self.safety)

    def test_prepare_builds_immutable_exact_non_executable_envelope(self) -> None:
        envelope = self._prepare()

        self.assertEqual(self.snapshot.trace_id, envelope.trace_id)
        self.assertEqual(
            self.snapshot.content_fingerprint,
            envelope.snapshot_fingerprint,
        )
        self.assertEqual(
            safety_assessment_fingerprint(self.safety),
            envelope.safety_assessment_fingerprint,
        )
        self.assertFalse(envelope.knowledge_binding_complete)
        self.assertFalse(envelope.engine_invocation_allowed)
        self.assertFalse(envelope.reasoning_execution_allowed)
        self.assertFalse(envelope.clinical_execution_allowed)
        self.assertNotIn("Sensitive synthetic observation.", repr(envelope))
        self.assertNotIn("Synthetic safety explanation.", repr(envelope))
        self.assertNotIn("Synthetic review rationale.", repr(envelope))
        with self.assertRaises(FrozenInstanceError):
            envelope.producer = "changed"  # type: ignore[misc]

    def test_changed_snapshot_with_same_trace_cannot_prepare(self) -> None:
        changed_observation = replace(
            self.snapshot.observations[0],
            value="Changed synthetic observation.",
        )
        changed_snapshot = replace(
            self.snapshot,
            observations=(changed_observation, *self.snapshot.observations[1:]),
        )

        with self.assertRaises(ReasoningError) as mismatch:
            ReasoningInputEnvelope.prepare(
                changed_snapshot,
                self.safety,
                self.review,
                envelope_id="reasoning-input.synthetic",
                producer="application.synthetic",
                prepared_at=self.prepared_at,
            )

        self.assertEqual("reasoning.snapshot_mismatch", mismatch.exception.code)

    def test_reassessment_review_cannot_prepare_engine_input(self) -> None:
        review = self._review(
            self.safety,
            disposition=SafetyReviewDisposition.REASSESSMENT_REQUIRED,
        )

        with self.assertRaises(ReasoningError) as blocked:
            ReasoningInputEnvelope.prepare(
                self.snapshot,
                self.safety,
                review,
                envelope_id="reasoning-input.synthetic",
                producer="application.synthetic",
                prepared_at=self.prepared_at,
            )

        self.assertEqual("reasoning_input.gate_status", blocked.exception.code)

    def test_tampered_gate_result_is_rejected(self) -> None:
        envelope = self._prepare()
        tampered_gate = replace(
            envelope.gate_result,
            reasons=("tampered_reason",),
        )

        with self.assertRaises(ReasoningError) as tampered:
            replace(envelope, gate_result=tampered_gate)

        self.assertEqual("reasoning_input.gate_result", tampered.exception.code)

    def test_identity_version_and_preparation_time_are_validated(self) -> None:
        envelope = self._prepare()
        for values in (
            {"envelope_id": "Invalid Envelope"},
            {"producer": "Invalid Producer"},
            {"contract_version": "v1"},
            {"prepared_at": self.snapshot_time - timedelta(seconds=1)},
            {"prepared_at": self.review_time - timedelta(milliseconds=1)},
            {"prepared_at": datetime.now(timezone.utc) + timedelta(minutes=1)},
        ):
            with self.subTest(values=values):
                with self.assertRaises((ReasoningError, TypeError)):
                    replace(envelope, **values)

    def _prepare(self) -> ReasoningInputEnvelope:
        return ReasoningInputEnvelope.prepare(
            self.snapshot,
            self.safety,
            self.review,
            envelope_id="reasoning-input.synthetic",
            producer="application.synthetic",
            prepared_at=self.prepared_at,
        )

    def _snapshot(self) -> ClinicalSnapshot:
        observations = tuple(
            ClinicalObservation(
                observation_id=EntityId(f"observation-{section.value}"),
                section=section,
                field_key=f"{section.value}.synthetic",
                value=(
                    "Sensitive synthetic observation."
                    if section is ClinicalSnapshotSection.SYMPTOMS
                    else False
                ),
                provenance=ClinicalDataProvenance.CLINICIAN_ENTERED,
                observed_at=self.snapshot_time,
            )
            for section in ClinicalSnapshotSection
        )
        return ClinicalSnapshot(
            snapshot_id=EntityId("snapshot-reasoning-input"),
            lineage_id=EntityId("lineage-reasoning-input"),
            subject_reference=SubjectReference(
                "sub-0123456789abcdef0123456789abcdef"
            ),
            session_id=EntityId("session-reasoning-input"),
            specialty_key="cardiology",
            captured_at=self.snapshot_time,
            observations=observations,
            trace_id="trace.reasoning-input",
        )

    @staticmethod
    def _safety(snapshot: ClinicalSnapshot) -> SafetyAssessment:
        result = SafetyCheckResult(
            check_id="check.synthetic-reasoning-input",
            outcome=SafetyCheckOutcome.PASSED,
            trace_id=snapshot.trace_id,
            snapshot_fingerprint=snapshot.content_fingerprint,
            explanation="Synthetic safety explanation.",
            evidence_source_ids=("source.synthetic-reasoning-input",),
        )
        return SafetyAssessment(
            status=SafetyGateStatus.READY_FOR_HUMAN_REVIEW,
            expected_check_ids=(result.check_id,),
            results=(result,),
            missing_check_ids=(),
            blocking_reasons=(),
            trace_id=snapshot.trace_id,
            snapshot_fingerprint=snapshot.content_fingerprint,
        )

    def _review(
        self,
        safety: SafetyAssessment,
        *,
        disposition: SafetyReviewDisposition = (
            SafetyReviewDisposition.VALIDATED_FOR_REASONING_REVIEW
        ),
    ) -> SafetyReviewRecord:
        return SafetyReviewRecord.create(
            safety,
            reviewer_id="reviewer.synthetic",
            authority_reference="authority.synthetic-workflow",
            reviewed_at=self.review_time,
            disposition=disposition,
            rationale="Synthetic review rationale.",
        )


if __name__ == "__main__":
    unittest.main()
