from dataclasses import FrozenInstanceError, replace
from datetime import date, datetime, timedelta, timezone
import unittest
from unittest.mock import patch

from decisionmed.application import (
    QUESTION_ENGINE_INVOCATION_ACTION,
    QuestionEngineExecutionApplicationService,
    QuestionEngineExecutionError,
    QuestionEngineInvocationAuthorityDecision,
    QuestionEngineInvocationAuthorityStatus,
    QuestionEnginePreparationApplicationService,
)
from decisionmed.audit import AuditError, AuditLedger

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
    QuestionEngineItem,
    QuestionEngineBinding,
    QuestionEngineOutputValidator,
    QuestionEngineReadiness,
    QuestionEngineReadinessStatus,
    QuestionEngineRegistry,
    QuestionEngineResult,
    QuestionEngineState,
    QuestionRequirement,
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


class SyntheticQuestionEngine:
    engine_id = "question-engine.synthetic"
    provider = "decisionmed.reasoning.question-engine.synthetic"
    contract_version = "0.1.0"

    def __init__(self) -> None:
        self.call_count = 0
        self.output: QuestionEngineResult | None = None

    def generate(self, input_value: GovernedReasoningInput) -> QuestionEngineResult:
        self.call_count += 1
        if self.output is None:
            raise AssertionError("test must configure synthetic engine output")
        return self.output


class SyntheticInvocationAuthority:
    provider = "authority.synthetic-question-engine"

    def __init__(self, decision: object) -> None:
        self.decision = decision
        self.call_count = 0

    def verify(self, **kwargs: object) -> object:
        self.call_count += 1
        return self.decision


class FailingAuditLedger(AuditLedger):
    def append(self, event, trace_id):  # type: ignore[no-untyped-def]
        raise AuditError("audit.synthetic_failure", "synthetic audit failure")


class QuestionEngineOutputValidatorTest(unittest.TestCase):
    def setUp(self) -> None:
        now = datetime.now(timezone.utc)
        self.snapshot_time = now - timedelta(seconds=5)
        self.review_time = now - timedelta(seconds=4)
        self.prepared_at = now - timedelta(seconds=3)
        self.bound_at = now - timedelta(seconds=2)
        self.assembled_at = now - timedelta(seconds=1)
        self.input_value = self._input()
        self.engine = SyntheticQuestionEngine()
        self.validator = QuestionEngineOutputValidator()

    def test_valid_result_produces_immutable_non_executable_receipt(self) -> None:
        result = self._result()

        receipt = self.validator.validate(
            self.input_value,
            result,
            self.engine,
            validated_at=self.assembled_at,
        )

        self.assertEqual(self.input_value.content_fingerprint, receipt.governed_input_fingerprint)
        self.assertEqual(result.engine_id, receipt.engine_id)
        self.assertRegex(receipt.result_fingerprint, r"^[0-9a-f]{64}$")
        self.assertRegex(receipt.content_fingerprint, r"^[0-9a-f]{64}$")
        self.assertFalse(receipt.engine_invocation_allowed)
        self.assertFalse(receipt.reasoning_execution_allowed)
        self.assertFalse(receipt.clinical_execution_allowed)
        with self.assertRaises(FrozenInstanceError):
            receipt.engine_id = "changed"  # type: ignore[misc]

    def test_exact_input_trace_and_engine_identity_are_required(self) -> None:
        for result in (
            self._result(input_fingerprint="a" * 64),
            self._result(trace_id="trace.other"),
            replace(self._result(), engine_id="question-engine.other"),
            replace(self._result(), provider="provider.other"),
            replace(self._result(), engine_version="0.2.0"),
        ):
            with self.subTest(result=result):
                with self.assertRaises(ReasoningError):
                    self.validator.validate(self.input_value, result, self.engine)

    def test_fields_and_open_gaps_must_exist_in_governed_schemas(self) -> None:
        for result in (
            self._result(field_key="symptoms.unknown"),
            self._result(extra_gap="symptoms.unknown"),
        ):
            with self.subTest(result=result):
                with self.assertRaises(ReasoningError) as rejected:
                    self.validator.validate(self.input_value, result, self.engine)

                self.assertIn(
                    rejected.exception.code,
                    {"question_validation.open_gaps", "question_validation.question_field"},
                )

    def test_question_references_must_be_bound_and_support_the_field(self) -> None:
        invalid_references = (
            (("knowledge.unbound",), ("source.synthetic-one",)),
            (("knowledge.synthetic-one",), ("source.unbound",)),
            (("knowledge.synthetic-two",), ("source.synthetic-two",)),
            (("knowledge.synthetic-one",), ("source.synthetic-two",)),
        )
        for object_ids, source_ids in invalid_references:
            with self.subTest(object_ids=object_ids, source_ids=source_ids):
                result = self._result(
                    knowledge_object_ids=object_ids,
                    evidence_source_ids=source_ids,
                )
                with self.assertRaises(ReasoningError):
                    self.validator.validate(self.input_value, result, self.engine)

    def test_result_fingerprint_covers_output_content(self) -> None:
        first = self.validator.validate(self.input_value, self._result(), self.engine)
        changed = self.validator.validate(
            self.input_value,
            self._result(prompt="Changed synthetic prompt?"),
            self.engine,
        )

        self.assertNotEqual(first.result_fingerprint, changed.result_fingerprint)

    def test_validation_cannot_predate_input_assembly(self) -> None:
        with self.assertRaises(ReasoningError) as rejected:
            self.validator.validate(
                self.input_value,
                self._result(),
                self.engine,
                validated_at=self.assembled_at - timedelta(seconds=1),
            )

        self.assertEqual("question_validation.validated_at", rejected.exception.code)

    def test_readiness_reports_structure_without_authorizing_invocation(self) -> None:
        registry = self._engine_registry(include_engine=True)

        report = QuestionEngineReadiness().assess(
            self.input_value,
            registry,
            self.engine.engine_id,
        )

        self.assertEqual(
            QuestionEngineReadinessStatus.STRUCTURAL_PREREQUISITES_PRESENT,
            report.status,
        )
        self.assertTrue(report.structural_prerequisites_present)
        self.assertIn("audited_invocation_orchestration_required", report.reasons)
        self.assertEqual(0, self.engine.call_count)
        self.assertFalse(report.engine_invocation_allowed)
        self.assertFalse(report.reasoning_execution_allowed)
        self.assertFalse(report.clinical_execution_allowed)
        with self.assertRaises(ReasoningError):
            replace(report, status=QuestionEngineReadinessStatus.BLOCKED)

    def test_readiness_fails_closed_for_missing_engine_or_expired_knowledge(self) -> None:
        report = QuestionEngineReadiness().assess(
            self.input_value,
            self._engine_registry(include_engine=False),
            self.engine.engine_id,
        )
        self.assertEqual(QuestionEngineReadinessStatus.BLOCKED, report.status)
        self.assertEqual(("engine_implementation_missing",), report.reasons)

        with patch(
            "decisionmed.reasoning.knowledge_binding._today",
            return_value=date.today() + timedelta(days=60),
        ):
            expired = QuestionEngineReadiness().assess(
                self.input_value,
                self._engine_registry(include_engine=True),
                self.engine.engine_id,
            )
        self.assertEqual(QuestionEngineReadinessStatus.BLOCKED, expired.status)
        self.assertIn("governed_knowledge_not_current", expired.reasons)
        self.assertEqual(0, self.engine.call_count)

    def test_question_preparation_is_audited_without_engine_invocation(self) -> None:
        ledger = AuditLedger()
        service = QuestionEnginePreparationApplicationService(
            QuestionEngineReadiness(),
            self._engine_registry(include_engine=True),
            ledger,
        )

        report = service.prepare(self.input_value, engine_id=self.engine.engine_id)
        record = ledger.records()[0]
        payload = dict(record.payload)

        self.assertTrue(report.structural_prerequisites_present)
        self.assertEqual(
            "reasoning.question_engine_preparation_completed",
            record.event_name,
        )
        self.assertEqual(report.status.value, payload["status"])
        self.assertEqual(self.input_value.content_fingerprint, payload["governed_input_fingerprint"])
        self.assertEqual("false", payload["engine_invocation_allowed"])
        self.assertEqual(0, self.engine.call_count)
        self.assertTrue(ledger.verify())
        self.assertFalse(service.engine_invocation_allowed)
        self.assertFalse(service.reasoning_execution_allowed)
        self.assertFalse(service.clinical_execution_allowed)
        self.assertNotIn("Synthetic value", str(record))

    def test_blocked_preparation_is_audited_and_audit_failure_prevents_return(self) -> None:
        ledger = AuditLedger()
        blocked_service = QuestionEnginePreparationApplicationService(
            QuestionEngineReadiness(),
            self._engine_registry(include_engine=False),
            ledger,
        )

        report = blocked_service.prepare(
            self.input_value,
            engine_id=self.engine.engine_id,
        )

        self.assertEqual(QuestionEngineReadinessStatus.BLOCKED, report.status)
        self.assertEqual("blocked", dict(ledger.records()[0].payload)["status"])
        self.assertEqual(0, self.engine.call_count)

        failing_service = QuestionEnginePreparationApplicationService(
            QuestionEngineReadiness(),
            self._engine_registry(include_engine=True),
            FailingAuditLedger(),
        )
        with self.assertRaises(AuditError):
            failing_service.prepare(
                self.input_value,
                engine_id=self.engine.engine_id,
            )

    def test_preparation_failure_records_only_safe_metadata(self) -> None:
        ledger = AuditLedger()
        service = QuestionEnginePreparationApplicationService(
            QuestionEngineReadiness(),
            self._engine_registry(include_engine=True),
            ledger,
        )

        with self.assertRaises(ReasoningError):
            service.prepare(self.input_value, engine_id="Invalid Engine")

        record = ledger.records()[0]
        self.assertEqual(
            "reasoning.question_engine_preparation_failed",
            record.event_name,
        )
        self.assertEqual("ReasoningError", dict(record.payload)["error_type"])
        self.assertNotIn("Synthetic value", str(record))
        self.assertEqual(0, self.engine.call_count)

    def test_authorized_execution_is_validated_and_audited(self) -> None:
        self.engine.output = self._result()
        authority = SyntheticInvocationAuthority(self._decision())
        ledger = AuditLedger()
        service = self._execution_service(authority, ledger)

        invocation = service.generate(
            self.input_value,
            engine_id=self.engine.engine_id,
            reviewer_id="reviewer.synthetic",
            authority_reference="authority.synthetic-workflow",
        )
        record = ledger.records()[-1]
        payload = dict(record.payload)

        self.assertIs(self.engine.output, invocation.result)
        self.assertEqual("decision.synthetic-question-engine", invocation.decision_reference)
        self.assertEqual("reasoning.question-engine-generated", record.event_name)
        self.assertEqual(invocation.receipt.result_fingerprint, payload["result_fingerprint"])
        self.assertEqual(1, self.engine.call_count)
        self.assertEqual(1, authority.call_count)
        self.assertEqual(
            "reasoning.question-engine-invocation-authorized",
            ledger.records()[0].event_name,
        )
        self.assertTrue(ledger.verify())
        self.assertFalse(invocation.engine_invocation_allowed)
        self.assertFalse(invocation.reasoning_execution_allowed)
        self.assertFalse(invocation.clinical_execution_allowed)
        self.assertNotIn("Synthetic governed question?", str(record))

    def test_execution_is_blocked_or_denied_before_engine_call(self) -> None:
        self.engine.output = self._result()
        denied_authority = SyntheticInvocationAuthority(
            self._decision(QuestionEngineInvocationAuthorityStatus.DENIED)
        )
        denied_ledger = AuditLedger()
        denied_service = self._execution_service(denied_authority, denied_ledger)

        with self.assertRaises(QuestionEngineExecutionError) as denied:
            denied_service.generate(
                self.input_value,
                engine_id=self.engine.engine_id,
                reviewer_id="reviewer.synthetic",
                authority_reference="authority.synthetic-workflow",
            )
        self.assertEqual("question_engine_execution.authority_denied", denied.exception.code)
        self.assertEqual("reasoning.question-engine-authority-denied", denied_ledger.records()[0].event_name)
        self.assertEqual(0, self.engine.call_count)

        blocked_authority = SyntheticInvocationAuthority(self._decision())
        blocked_ledger = AuditLedger()
        blocked_service = self._execution_service(
            blocked_authority,
            blocked_ledger,
            include_engine=False,
        )
        with self.assertRaises(QuestionEngineExecutionError) as blocked:
            blocked_service.generate(
                self.input_value,
                engine_id=self.engine.engine_id,
                reviewer_id="reviewer.synthetic",
                authority_reference="authority.synthetic-workflow",
            )
        self.assertEqual("question_engine_execution.not_ready", blocked.exception.code)
        self.assertEqual("reasoning.question-engine-invocation-blocked", blocked_ledger.records()[0].event_name)
        self.assertEqual(0, blocked_authority.call_count)
        self.assertEqual(0, self.engine.call_count)

    def test_invalid_engine_output_is_audited_and_not_returned(self) -> None:
        self.engine.output = self._result(field_key="symptoms.unknown")
        authority = SyntheticInvocationAuthority(self._decision())
        ledger = AuditLedger()
        service = self._execution_service(authority, ledger)

        with self.assertRaises(ReasoningError):
            service.generate(
                self.input_value,
                engine_id=self.engine.engine_id,
                reviewer_id="reviewer.synthetic",
                authority_reference="authority.synthetic-workflow",
            )

        record = ledger.records()[-1]
        self.assertEqual("reasoning.question-engine-output-rejected", record.event_name)
        self.assertEqual(1, self.engine.call_count)
        self.assertNotIn("Synthetic governed question?", str(record))

    def test_audit_failure_prevents_engine_invocation(self) -> None:
        self.engine.output = self._result()
        service = self._execution_service(
            SyntheticInvocationAuthority(self._decision()),
            FailingAuditLedger(),
        )

        with self.assertRaises(AuditError):
            service.generate(
                self.input_value,
                engine_id=self.engine.engine_id,
                reviewer_id="reviewer.synthetic",
                authority_reference="authority.synthetic-workflow",
            )

        self.assertEqual(0, self.engine.call_count)

    def _execution_service(
        self,
        authority: SyntheticInvocationAuthority,
        ledger: AuditLedger,
        *,
        include_engine: bool = True,
    ) -> QuestionEngineExecutionApplicationService:
        return QuestionEngineExecutionApplicationService(
            QuestionEngineReadiness(),
            self._engine_registry(include_engine=include_engine),
            authority,
            self.validator,
            ledger,
        )

    def _decision(
        self,
        status: QuestionEngineInvocationAuthorityStatus = (
            QuestionEngineInvocationAuthorityStatus.AUTHORIZED
        ),
    ) -> QuestionEngineInvocationAuthorityDecision:
        return QuestionEngineInvocationAuthorityDecision(
            reviewer_id="reviewer.synthetic",
            authority_reference="authority.synthetic-workflow",
            authority_provider="authority.synthetic-question-engine",
            action=QUESTION_ENGINE_INVOCATION_ACTION,
            trace_id=self.input_value.trace_id,
            governed_input_fingerprint=self.input_value.content_fingerprint,
            engine_id=self.engine.engine_id,
            engine_contract_version=self.engine.contract_version,
            status=status,
            decision_reference="decision.synthetic-question-engine",
            verified_at=self.assembled_at,
        )

    def _engine_registry(self, *, include_engine: bool) -> QuestionEngineRegistry:
        binding = QuestionEngineBinding(
            engine_id=self.engine.engine_id,
            provider=self.engine.provider,
            contract_version=self.engine.contract_version,
        )
        engines = (self.engine,) if include_engine else ()
        return QuestionEngineRegistry((binding,), engines)

    def _result(
        self,
        *,
        input_fingerprint: str | None = None,
        trace_id: str | None = None,
        field_key: str = "symptoms.synthetic",
        extra_gap: str | None = None,
        knowledge_object_ids: tuple[str, ...] = ("knowledge.synthetic-one",),
        evidence_source_ids: tuple[str, ...] = ("source.synthetic-one",),
        prompt: str = "Synthetic governed question?",
    ) -> QuestionEngineResult:
        fingerprint = input_fingerprint or self.input_value.content_fingerprint
        trace = trace_id or self.input_value.trace_id
        question = QuestionEngineItem(
            question_id="question.synthetic",
            field_key=field_key,
            prompt=prompt,
            requirement=QuestionRequirement.REQUIRED,
            priority_rank=1,
            rationale="Synthetic rationale.",
            knowledge_object_ids=knowledge_object_ids,
            evidence_source_ids=evidence_source_ids,
            trace_id=trace,
            governed_input_fingerprint=fingerprint,
        )
        gaps = (field_key,) + ((extra_gap,) if extra_gap else ())
        return QuestionEngineResult(
            engine_id=self.engine.engine_id,
            engine_version=self.engine.contract_version,
            provider=self.engine.provider,
            governed_input_fingerprint=fingerprint,
            trace_id=trace,
            state=QuestionEngineState.COLLECTION_PENDING,
            questions=(question,),
            open_gap_field_keys=gaps,
            explanation="Synthetic result explanation.",
        )

    def _input(self) -> GovernedReasoningInput:
        snapshot = ClinicalSnapshot(
            snapshot_id=EntityId("snapshot-question-output-validation"),
            lineage_id=EntityId("lineage-question-output-validation"),
            subject_reference=SubjectReference("sub-0123456789abcdef0123456789abcdef"),
            session_id=EntityId("session-question-output-validation"),
            specialty_key="cardiology",
            captured_at=self.snapshot_time,
            observations=tuple(
                ClinicalObservation(
                    observation_id=EntityId(f"observation-{section.value}"),
                    section=section,
                    field_key=f"{section.value}.synthetic",
                    value="Synthetic value" if section is ClinicalSnapshotSection.SYMPTOMS else False,
                    provenance=ClinicalDataProvenance.CLINICIAN_ENTERED,
                    observed_at=self.snapshot_time,
                )
                for section in ClinicalSnapshotSection
            ),
            trace_id="trace.question-output-validation",
        )
        check = SafetyCheckResult(
            check_id="check.question-output-validation",
            outcome=SafetyCheckOutcome.PASSED,
            trace_id=snapshot.trace_id,
            snapshot_fingerprint=snapshot.content_fingerprint,
            explanation="Synthetic safety explanation.",
            evidence_source_ids=("source.synthetic-one",),
        )
        assessment = SafetyAssessment(
            status=SafetyGateStatus.READY_FOR_HUMAN_REVIEW,
            expected_check_ids=(check.check_id,),
            results=(check,),
            missing_check_ids=(),
            blocking_reasons=(),
            trace_id=snapshot.trace_id,
            snapshot_fingerprint=snapshot.content_fingerprint,
        )
        review = SafetyReviewRecord.create(
            assessment,
            reviewer_id="reviewer.synthetic",
            authority_reference="authority.synthetic-workflow",
            reviewed_at=self.review_time,
            disposition=SafetyReviewDisposition.VALIDATED_FOR_REASONING_REVIEW,
            rationale="Synthetic review rationale.",
        )
        envelope = ReasoningInputEnvelope.prepare(
            snapshot,
            assessment,
            review,
            envelope_id="reasoning-input.question-output-validation",
            producer="application.synthetic",
            prepared_at=self.prepared_at,
        )
        sources = tuple(self._source(index) for index in ("one", "two"))
        objects = tuple(
            self._knowledge(index, source.source_id)
            for index, source in zip(("one", "two"), sources)
        )
        schema = SpecialtyFormSchema(
            schema_id="schema.cardiology.question-output-validation",
            specialty_key="cardiology",
            workflow_id="decisionmed.cardiology.workflow.v1",
            step_key="context",
            version="1.0.0",
            fields=(
                ClinicalFieldDefinition(
                    field_key="symptoms.synthetic",
                    label="Synthetic field",
                    section=ClinicalSnapshotSection.SYMPTOMS,
                    value_type=ClinicalFieldValueType.TEXT,
                    knowledge_object_id=objects[0].object_id,
                    required=True,
                ),
            ),
            status=KnowledgeStatus.VALIDATED,
            reviewed_on=date.today(),
            validated_by="reviewer.synthetic",
            review_due_on=date.today() + timedelta(days=30),
        )
        binding = ReasoningKnowledgeBinding(
            catalog_id="decisionmed.knowledge",
            catalog_version="1.0.0",
            catalog_status=KnowledgeStatus.VALIDATED,
            catalog_released_on=date.today(),
            catalog_validated_by="reviewer.synthetic",
            specialty_key="cardiology",
            bound_at=self.bound_at,
            knowledge_objects=objects,
            evidence_sources=sources,
            form_schemas=(schema,),
        )
        return GovernedReasoningInput(
            input_id="governed-reasoning-input.question-output-validation",
            contract_version="0.1.0",
            assembled_at=self.assembled_at,
            envelope=envelope,
            knowledge_binding=binding,
        )

    @staticmethod
    def _source(index: str) -> EvidenceSource:
        return EvidenceSource(
            source_id=f"source.synthetic-{index}",
            title=f"Synthetic source {index}",
            publication_year=2025,
            evidence_type=EvidenceType.OTHER,
            evidence_quality=EvidenceQuality.INSUFFICIENT,
            recommendation_strength=RecommendationStrength.INSUFFICIENT_FOR_RECOMMENDATION,
            locator=f"test-only:{index}",
            version="1.0.0",
            status=EvidenceStatus.VALIDATED,
            specialties=("cardiology",),
            reviewed_on=date.today(),
            known_conflicts="Synthetic conflicts.",
            clinical_applicability="Structural tests only.",
            review_due_on=date.today() + timedelta(days=30),
        )

    @staticmethod
    def _knowledge(index: str, source_id: str) -> KnowledgeObject:
        return KnowledgeObject(
            object_id=f"knowledge.synthetic-{index}",
            official_name=f"Synthetic knowledge {index}",
            object_type=KnowledgeObjectType.OTHER,
            description="Synthetic description.",
            evidence_anchors=(EvidenceAnchor(source_id, "Synthetic section", "Synthetic locator"),),
            applicability="Structural tests only.",
            limits="No clinical use.",
            version="1.0.0",
            status=KnowledgeStatus.VALIDATED,
            reviewed_on=date.today(),
            validated_by="reviewer.synthetic",
            review_due_on=date.today() + timedelta(days=30),
        )


if __name__ == "__main__":
    unittest.main()
