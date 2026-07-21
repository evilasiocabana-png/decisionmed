from dataclasses import FrozenInstanceError, replace
from datetime import date
import unittest

from decisionmed.domain import ClinicalSnapshotSection
from decisionmed.evidence import (
    EvidenceRegistry,
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
    KnowledgeError,
    KnowledgeObject,
    KnowledgeObjectType,
    KnowledgeRegistry,
    KnowledgeStatus,
    SpecialtyFormSchema,
    SpecialtyFormSchemaRegistry,
)


class SpecialtyFormSchemaTest(unittest.TestCase):
    def test_field_is_immutable_and_never_runtime_eligible(self) -> None:
        field = self._field()

        self.assertFalse(field.runtime_eligible)
        with self.assertRaises(FrozenInstanceError):
            field.label = "changed"  # type: ignore[misc]

    def test_choice_values_are_explicit_unique_and_type_limited(self) -> None:
        valid = self._field(
            value_type=ClinicalFieldValueType.CODED_CHOICE,
            allowed_values=("present", "absent", "unknown"),
        )
        self.assertEqual(("present", "absent", "unknown"), valid.allowed_values)

        for value_type, choices in (
            (ClinicalFieldValueType.CODED_CHOICE, ()),
            (ClinicalFieldValueType.BOOLEAN, ("yes", "no")),
            (ClinicalFieldValueType.CODED_CHOICE, ("same", "same")),
        ):
            with self.subTest(value_type=value_type, choices=choices):
                with self.assertRaises(KnowledgeError):
                    self._field(value_type=value_type, allowed_values=choices)

    def test_schema_requires_unique_fields_and_human_review_metadata(self) -> None:
        field = self._field()
        with self.assertRaises(KnowledgeError):
            self._schema((field, field))
        with self.assertRaises(KnowledgeError):
            self._schema((field,), status=KnowledgeStatus.VALIDATED)

    def test_registry_requires_every_linked_knowledge_object(self) -> None:
        registry = SpecialtyFormSchemaRegistry(KnowledgeRegistry(EvidenceRegistry()))

        with self.assertRaises(KnowledgeError) as context:
            registry.register(self._schema((self._field(),)))

        self.assertEqual("knowledge_registry.unknown", context.exception.code)

    def test_validated_schema_requires_validated_linked_knowledge(self) -> None:
        evidence = EvidenceRegistry((self._evidence(EvidenceStatus.DRAFT),))
        knowledge = KnowledgeRegistry(
            evidence,
            (self._knowledge(KnowledgeStatus.DRAFT),),
        )
        registry = SpecialtyFormSchemaRegistry(knowledge)

        with self.assertRaises(KnowledgeError) as context:
            registry.register(
                self._schema(
                    (self._field(),),
                    status=KnowledgeStatus.VALIDATED,
                    reviewed_on=date(2026, 7, 21),
                    validated_by="reviewer-1",
                )
            )

        self.assertEqual(
            "specialty_form_schema_registry.unvalidated_knowledge",
            context.exception.code,
        )

    def test_registered_schema_is_deterministic_but_never_clinically_active(self) -> None:
        evidence = EvidenceRegistry((self._evidence(EvidenceStatus.VALIDATED),))
        knowledge = KnowledgeRegistry(
            evidence,
            (self._knowledge(KnowledgeStatus.VALIDATED),),
        )
        schema = self._schema(
            (self._field(),),
            status=KnowledgeStatus.VALIDATED,
            reviewed_on=date(2026, 7, 21),
            validated_by="reviewer-1",
        )
        registry = SpecialtyFormSchemaRegistry(knowledge, (schema,))

        self.assertIs(
            schema,
            registry.require(
                "cardiology", "decisionmed.cardiology.workflow.v1", "context"
            ),
        )
        self.assertEqual((schema,), registry.all())
        self.assertFalse(schema.runtime_eligible)
        self.assertFalse(schema.clinical_execution_allowed)
        with self.assertRaises(KnowledgeError):
            registry.register(schema)

    def test_registry_allows_distinct_steps_but_rejects_duplicate_binding(self) -> None:
        evidence = EvidenceRegistry((self._evidence(EvidenceStatus.DRAFT),))
        knowledge = KnowledgeRegistry(
            evidence,
            (self._knowledge(KnowledgeStatus.DRAFT),),
        )
        context_schema = self._schema((self._field(),))
        risk_schema = replace(
            context_schema,
            schema_id="schema.cardiology.risk",
            step_key="risk",
        )
        registry = SpecialtyFormSchemaRegistry(
            knowledge, (context_schema, risk_schema)
        )

        self.assertEqual(
            (context_schema, risk_schema),
            registry.for_workflow(
                "cardiology", "decisionmed.cardiology.workflow.v1"
            ),
        )
        self.assertIs(
            risk_schema,
            registry.require(
                "cardiology", "decisionmed.cardiology.workflow.v1", "risk"
            ),
        )
        with self.assertRaises(KnowledgeError) as context:
            registry.register(
                replace(
                    context_schema,
                    schema_id="schema.cardiology.duplicate-context",
                )
            )
        self.assertEqual(
            "specialty_form_schema_registry.duplicate_binding",
            context.exception.code,
        )

    @staticmethod
    def _field(
        *,
        value_type: ClinicalFieldValueType = ClinicalFieldValueType.BOOLEAN,
        allowed_values: tuple[str, ...] = (),
    ) -> ClinicalFieldDefinition:
        return ClinicalFieldDefinition(
            field_key="symptoms.present",
            label="Structural sample field",
            section=ClinicalSnapshotSection.SYMPTOMS,
            value_type=value_type,
            knowledge_object_id="knowledge.sample-field",
            required=True,
            allowed_values=allowed_values,
        )

    @staticmethod
    def _schema(
        fields: tuple[ClinicalFieldDefinition, ...],
        *,
        status: KnowledgeStatus = KnowledgeStatus.DRAFT,
        reviewed_on: date | None = None,
        validated_by: str | None = None,
    ) -> SpecialtyFormSchema:
        return SpecialtyFormSchema(
            schema_id="schema.cardiology.intake",
            specialty_key="cardiology",
            workflow_id="decisionmed.cardiology.workflow.v1",
            step_key="context",
            version="0.1.0",
            fields=fields,
            status=status,
            reviewed_on=reviewed_on,
            validated_by=validated_by,
        )

    @staticmethod
    def _evidence(status: EvidenceStatus) -> EvidenceSource:
        return EvidenceSource(
            source_id="evidence.sample",
            title="Structural test source",
            publication_year=2025,
            evidence_type=EvidenceType.GUIDELINE,
            evidence_quality=EvidenceQuality.INSUFFICIENT,
            recommendation_strength=RecommendationStrength.INSUFFICIENT_FOR_RECOMMENDATION,
            locator="test-only",
            version="1.0.0",
            status=status,
            specialties=("cardiology",),
            reviewed_on=date(2026, 7, 21),
            known_conflicts="No conflicts assessed; synthetic fixture.",
            clinical_applicability="Contract tests only.",
        )

    @staticmethod
    def _knowledge(status: KnowledgeStatus) -> KnowledgeObject:
        return KnowledgeObject(
            object_id="knowledge.sample-field",
            official_name="Structural sample field",
            object_type=KnowledgeObjectType.OTHER,
            description="Test-only metadata without a clinical claim.",
            evidence_anchors=(
                EvidenceAnchor(
                    source_id="evidence.sample",
                    section="Synthetic section",
                    locator="https://example.test/source#section",
                ),
            ),
            applicability="Unit tests only.",
            limits="No clinical use.",
            version="1.0.0",
            status=status,
            reviewed_on=date(2026, 7, 21)
            if status is KnowledgeStatus.VALIDATED
            else None,
            validated_by="reviewer-1"
            if status is KnowledgeStatus.VALIDATED
            else None,
        )


if __name__ == "__main__":
    unittest.main()
