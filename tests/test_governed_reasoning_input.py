from dataclasses import FrozenInstanceError, replace
from datetime import date, datetime, timedelta, timezone
import unittest
from unittest.mock import patch

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
    EvidenceSource,
    EvidenceStatus,
    EvidenceType,
    RecommendationStrength,
)
from decisionmed.knowledge import (
    ClinicalFieldDefinition,
    ClinicalFieldValueType,
    EvidenceAnchor,
    KnowledgeObject,
    KnowledgeObjectType,
    KnowledgeStatus,
    SpecialtyFormSchema,
)
from decisionmed.reasoning import (
    GovernedReasoningInput,
    ReasoningError,
    ReasoningInputEnvelope,
    ReasoningKnowledgeBinding,
)
from decisionmed.safety import (
    SafetyAssessment,
    SafetyCheckOutcome,
    SafetyCheckResult,
    SafetyGateStatus,
    SafetyReviewDisposition,
    SafetyReviewRecord,
)


class GovernedReasoningInputTest(unittest.TestCase):
    def setUp(self) -> None:
        self.snapshot_time = datetime.now(timezone.utc) - timedelta(seconds=4)
        self.review_time = datetime.now(timezone.utc) - timedelta(seconds=3)
        self.prepared_at = datetime.now(timezone.utc) - timedelta(seconds=2)
        self.bound_at = datetime.now(timezone.utc) - timedelta(seconds=2)
        self.assembled_at = datetime.now(timezone.utc) - timedelta(seconds=1)
        self.envelope = self._envelope()
        self.binding = self._binding()

    def test_exact_composition_is_immutable_and_still_non_executable(self) -> None:
        governed = self._governed()

        self.assertEqual(self.envelope.trace_id, governed.trace_id)
        self.assertEqual("cardiology", governed.specialty_key)
        self.assertEqual(
            self.envelope.snapshot_fingerprint,
            governed.snapshot_fingerprint,
        )
        self.assertEqual(
            self.binding.content_fingerprint,
            governed.knowledge_binding_fingerprint,
        )
        self.assertRegex(governed.content_fingerprint, r"^[0-9a-f]{64}$")
        self.assertTrue(governed.knowledge_binding_complete)
        self.assertFalse(governed.engine_contract_present)
        self.assertFalse(governed.engine_invocation_allowed)
        self.assertFalse(governed.reasoning_execution_allowed)
        self.assertFalse(governed.clinical_execution_allowed)
        self.assertNotIn("Sensitive synthetic observation.", repr(governed))
        self.assertNotIn("Synthetic knowledge description.", repr(governed))
        with self.assertRaises(FrozenInstanceError):
            governed.input_id = "changed"  # type: ignore[misc]

    def test_specialty_mismatch_is_rejected(self) -> None:
        source = replace(self.binding.evidence_sources[0], specialties=("psychiatry",))
        schema = replace(
            self.binding.form_schemas[0],
            specialty_key="psychiatry",
        )
        mismatched_binding = replace(
            self.binding,
            specialty_key="psychiatry",
            evidence_sources=(source,),
            form_schemas=(schema,),
        )

        with self.assertRaises(ReasoningError) as mismatch:
            self._governed(knowledge_binding=mismatched_binding)

        self.assertEqual(
            "governed_reasoning_input.specialty_mismatch",
            mismatch.exception.code,
        )

    def test_expired_binding_is_rechecked_and_rejected(self) -> None:
        future = date.today() + timedelta(days=60)
        with patch(
            "decisionmed.reasoning.knowledge_binding._today",
            return_value=future,
        ):
            with self.assertRaises(ReasoningError) as expired:
                self._governed()

        self.assertEqual(
            "governed_reasoning_input.knowledge_expired",
            expired.exception.code,
        )

    def test_knowledge_change_changes_combined_fingerprint(self) -> None:
        original = self._governed()
        changed_object = replace(
            self.binding.knowledge_objects[0],
            description="Changed synthetic knowledge description.",
        )
        changed_binding = replace(
            self.binding,
            knowledge_objects=(changed_object,),
        )
        changed = self._governed(knowledge_binding=changed_binding)

        self.assertNotEqual(
            original.content_fingerprint,
            changed.content_fingerprint,
        )

    def test_identity_and_assembly_time_are_validated(self) -> None:
        governed = self._governed()
        for values in (
            {"input_id": "Invalid Input"},
            {"contract_version": "v1"},
            {"assembled_at": self.prepared_at - timedelta(seconds=1)},
            {"assembled_at": self.bound_at - timedelta(seconds=1)},
            {"assembled_at": datetime.now(timezone.utc) + timedelta(minutes=1)},
        ):
            with self.subTest(values=values):
                with self.assertRaises((ReasoningError, TypeError)):
                    replace(governed, **values)

    def _governed(self, **changes: object) -> GovernedReasoningInput:
        values = {
            "input_id": "governed-reasoning-input.synthetic",
            "contract_version": "0.1.0",
            "assembled_at": self.assembled_at,
            "envelope": self.envelope,
            "knowledge_binding": self.binding,
            **changes,
        }
        return GovernedReasoningInput(**values)

    def _envelope(self) -> ReasoningInputEnvelope:
        snapshot = self._snapshot()
        result = SafetyCheckResult(
            check_id="check.synthetic-governed-input",
            outcome=SafetyCheckOutcome.PASSED,
            trace_id=snapshot.trace_id,
            snapshot_fingerprint=snapshot.content_fingerprint,
            explanation="Synthetic safety explanation.",
            evidence_source_ids=("source.synthetic-governed-input",),
        )
        safety = SafetyAssessment(
            status=SafetyGateStatus.READY_FOR_HUMAN_REVIEW,
            expected_check_ids=(result.check_id,),
            results=(result,),
            missing_check_ids=(),
            blocking_reasons=(),
            trace_id=snapshot.trace_id,
            snapshot_fingerprint=snapshot.content_fingerprint,
        )
        review = SafetyReviewRecord.create(
            safety,
            reviewer_id="reviewer.synthetic",
            authority_reference="authority.synthetic-workflow",
            reviewed_at=self.review_time,
            disposition=SafetyReviewDisposition.VALIDATED_FOR_REASONING_REVIEW,
            rationale="Synthetic review rationale.",
        )
        return ReasoningInputEnvelope.prepare(
            snapshot,
            safety,
            review,
            envelope_id="reasoning-input.synthetic-governed",
            producer="application.synthetic",
            prepared_at=self.prepared_at,
        )

    def _snapshot(self) -> ClinicalSnapshot:
        return ClinicalSnapshot(
            snapshot_id=EntityId("snapshot-governed-reasoning-input"),
            lineage_id=EntityId("lineage-governed-reasoning-input"),
            subject_reference=SubjectReference(
                "sub-0123456789abcdef0123456789abcdef"
            ),
            session_id=EntityId("session-governed-reasoning-input"),
            specialty_key="cardiology",
            captured_at=self.snapshot_time,
            observations=tuple(
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
            ),
            trace_id="trace.governed-reasoning-input",
        )

    def _binding(self) -> ReasoningKnowledgeBinding:
        source = EvidenceSource(
            source_id="source.synthetic-governed-input",
            title="Synthetic governed input source",
            publication_year=2025,
            evidence_type=EvidenceType.OTHER,
            evidence_quality=EvidenceQuality.INSUFFICIENT,
            recommendation_strength=(
                RecommendationStrength.INSUFFICIENT_FOR_RECOMMENDATION
            ),
            locator="test-only:governed-input",
            version="1.0.0",
            status=EvidenceStatus.VALIDATED,
            specialties=("cardiology",),
            reviewed_on=date.today(),
            known_conflicts="Synthetic conflicts metadata.",
            clinical_applicability="Structural tests only.",
            review_due_on=date.today() + timedelta(days=30),
        )
        knowledge = KnowledgeObject(
            object_id="knowledge.synthetic-governed-input",
            official_name="Synthetic governed input knowledge",
            object_type=KnowledgeObjectType.OTHER,
            description="Synthetic knowledge description.",
            evidence_anchors=(
                EvidenceAnchor(
                    source.source_id,
                    "Synthetic section",
                    "Synthetic locator",
                ),
            ),
            applicability="Structural tests only.",
            limits="No clinical use.",
            version="1.0.0",
            status=KnowledgeStatus.VALIDATED,
            reviewed_on=date.today(),
            validated_by="reviewer.synthetic",
            review_due_on=date.today() + timedelta(days=30),
        )
        schema = SpecialtyFormSchema(
            schema_id="schema.cardiology.synthetic-governed-input",
            specialty_key="cardiology",
            workflow_id="decisionmed.cardiology.workflow.v1",
            step_key="context",
            version="1.0.0",
            fields=(
                ClinicalFieldDefinition(
                    field_key="symptoms.synthetic",
                    label="Synthetic governed input field",
                    section=ClinicalSnapshotSection.SYMPTOMS,
                    value_type=ClinicalFieldValueType.TEXT,
                    knowledge_object_id=knowledge.object_id,
                    required=True,
                ),
            ),
            status=KnowledgeStatus.VALIDATED,
            reviewed_on=date.today(),
            validated_by="reviewer.synthetic",
            review_due_on=date.today() + timedelta(days=30),
        )
        return ReasoningKnowledgeBinding(
            catalog_id="decisionmed.knowledge",
            catalog_version="1.0.0",
            catalog_status=KnowledgeStatus.VALIDATED,
            catalog_released_on=date.today(),
            catalog_validated_by="reviewer.synthetic",
            specialty_key="cardiology",
            bound_at=self.bound_at,
            knowledge_objects=(knowledge,),
            evidence_sources=(source,),
            form_schemas=(schema,),
        )


if __name__ == "__main__":
    unittest.main()
