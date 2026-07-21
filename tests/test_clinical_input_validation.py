from dataclasses import FrozenInstanceError, fields
from datetime import date
import math
import unittest

from decisionmed.application import ClinicalInputStructureValidator
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
    KnowledgeObject,
    KnowledgeObjectType,
    KnowledgeRegistry,
    KnowledgeStatus,
    SpecialtyFormSchema,
    SpecialtyFormSchemaRegistry,
)


class ClinicalInputStructureValidatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = ClinicalInputStructureValidator(self._schemas())

    def test_valid_payload_is_structural_only_and_never_clinically_active(self) -> None:
        result = self.validator.validate(
            "cardiology",
            {
                "symptoms.present": True,
                "symptoms.count": 2,
                "symptoms.score": 1.5,
                "symptoms.note": "bounded structural value",
                "symptoms.state": "unknown",
            },
        )

        self.assertTrue(result.structurally_valid)
        self.assertEqual(5, result.accepted_field_count)
        self.assertEqual("draft", result.schema_status)
        self.assertFalse(result.clinical_execution_allowed)

    def test_required_and_unknown_fields_are_reported_without_values(self) -> None:
        secret = "patient-secret-value"
        result = self.validator.validate("cardiology", {"unexpected": secret})

        self.assertFalse(result.structurally_valid)
        self.assertEqual(
            {
                ("symptoms.present", "required"),
                ("symptoms.state", "required"),
                ("unexpected", "unknown_field"),
            },
            {(issue.field_key, issue.code) for issue in result.issues},
        )
        self.assertNotIn(secret, repr(result))

    def test_primitive_types_are_strict_and_finite(self) -> None:
        invalid = {
            "symptoms.present": 1,
            "symptoms.count": True,
            "symptoms.score": math.inf,
            "symptoms.note": " ",
            "symptoms.state": "not-allowed",
        }

        result = self.validator.validate("cardiology", invalid)

        self.assertEqual(0, result.accepted_field_count)
        self.assertEqual(5, len(result.issues))
        self.assertTrue(all(issue.code == "invalid_value" for issue in result.issues))

    def test_optional_fields_may_be_omitted(self) -> None:
        result = self.validator.validate(
            "cardiology",
            {"symptoms.present": False, "symptoms.state": "absent"},
        )

        self.assertTrue(result.structurally_valid)
        self.assertEqual(2, result.accepted_field_count)

    def test_large_integer_decimal_does_not_raise_or_lose_structure(self) -> None:
        result = self.validator.validate(
            "cardiology",
            {
                "symptoms.present": False,
                "symptoms.score": 10**1000,
                "symptoms.state": "absent",
            },
        )

        self.assertTrue(result.structurally_valid)
        self.assertEqual(3, result.accepted_field_count)

    def test_result_is_immutable_and_contains_no_input_values(self) -> None:
        result = self.validator.validate(
            "cardiology",
            {"symptoms.present": False, "symptoms.state": "absent"},
        )

        self.assertEqual(
            {
                "schema_id",
                "schema_version",
                "schema_status",
                "accepted_field_count",
                "issues",
            },
            {item.name for item in fields(result)},
        )
        with self.assertRaises(FrozenInstanceError):
            result.schema_status = "validated"  # type: ignore[misc]

    @staticmethod
    def _schemas() -> SpecialtyFormSchemaRegistry:
        evidence = EvidenceRegistry(
            (
                EvidenceSource(
                    source_id="evidence.form-structure",
                    title="Structural test source",
                    publication_year=2025,
                    evidence_type=EvidenceType.GUIDELINE,
                    evidence_quality=EvidenceQuality.INSUFFICIENT,
                    recommendation_strength=RecommendationStrength.INSUFFICIENT_FOR_RECOMMENDATION,
                    locator="test-only",
                    version="1.0.0",
                    status=EvidenceStatus.DRAFT,
                    specialties=("cardiology",),
                    reviewed_on=date(2026, 7, 21),
                    known_conflicts="No conflicts assessed; synthetic fixture.",
                    clinical_applicability="Contract tests only.",
                ),
            )
        )
        knowledge = KnowledgeRegistry(
            evidence,
            tuple(
                KnowledgeObject(
                    object_id=f"knowledge.{suffix}",
                    official_name=f"Structural {suffix}",
                    object_type=KnowledgeObjectType.OTHER,
                    description="Test-only metadata without a clinical claim.",
                    evidence_source_ids=("evidence.form-structure",),
                    applicability="Unit tests only.",
                    limits="No clinical use.",
                    version="1.0.0",
                    status=KnowledgeStatus.DRAFT,
                )
                for suffix in ("present", "count", "score", "note", "state")
            ),
        )
        definitions = (
            ("present", ClinicalFieldValueType.BOOLEAN, True, ()),
            ("count", ClinicalFieldValueType.INTEGER, False, ()),
            ("score", ClinicalFieldValueType.DECIMAL, False, ()),
            ("note", ClinicalFieldValueType.TEXT, False, ()),
            (
                "state",
                ClinicalFieldValueType.CODED_CHOICE,
                True,
                ("present", "absent", "unknown"),
            ),
        )
        schema = SpecialtyFormSchema(
            schema_id="schema.cardiology.structural",
            specialty_key="cardiology",
            version="0.1.0",
            fields=tuple(
                ClinicalFieldDefinition(
                    field_key=f"symptoms.{suffix}",
                    label=f"Structural {suffix}",
                    section=ClinicalSnapshotSection.SYMPTOMS,
                    value_type=value_type,
                    knowledge_object_id=f"knowledge.{suffix}",
                    required=required,
                    allowed_values=allowed_values,
                )
                for suffix, value_type, required, allowed_values in definitions
            ),
            status=KnowledgeStatus.DRAFT,
        )
        return SpecialtyFormSchemaRegistry(knowledge, (schema,))


if __name__ == "__main__":
    unittest.main()
