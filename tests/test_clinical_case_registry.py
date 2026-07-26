import json
import unittest

from decisionmed.knowledge import (
    ClinicalCaseAnswer,
    ClinicalCaseAuditEvent,
    ClinicalCaseCategory,
    ClinicalCaseRegistry,
    ClinicalContentStatus,
    ClinicalEntityType,
    ClinicalModuleDefinition,
    ClinicalModuleRegistry,
    ClinicalModuleStatus,
    ClinicalTestCase,
    KnowledgeError,
    TerminologyStatus,
    audit_hash_for,
)


def module_registry(count: int = 1) -> ClinicalModuleRegistry:
    return ClinicalModuleRegistry(
        tuple(
            ClinicalModuleDefinition(
                module_id=f"module.test.item-{index}",
                version="0.1.0",
                official_name=f"Test item {index}",
                display_name=f"Test item {index}",
                entity_type=ClinicalEntityType.CLINICAL_PRESENTATION,
                primary_specialty="test",
                terminology_status=TerminologyStatus.CANDIDATE,
                content_status=ClinicalContentStatus.SKELETON,
                status=ClinicalModuleStatus.DRAFT,
            )
            for index in range(1, count + 1)
        )
    )


def make_case(
    module_id: str = "module.test.item-1",
    ordinal: int = 1,
    category: ClinicalCaseCategory = ClinicalCaseCategory.TYPICAL,
) -> ClinicalTestCase:
    payload = json.dumps(
        {"module_id": module_id, "ordinal": ordinal},
        sort_keys=True,
        separators=(",", ":"),
    )
    events = (
        ClinicalCaseAuditEvent(
            sequence=1,
            event_type="case.started",
            payload=payload,
        ),
    )
    return ClinicalTestCase(
        case_id=f"case.{module_id.removeprefix('module.')}.{ordinal:02d}",
        module_id=module_id,
        ordinal=ordinal,
        category=category,
        narrative="Synthetic narrative consistent with the selected facts.",
        selected_answers=(
            ClinicalCaseAnswer(
                fact_id="case.category",
                values=(category.value,),
            ),
        ),
        positive_details=("Synthetic structured detail.",),
        expected_route_module_ids=(module_id,),
        obtained_route_module_ids=(module_id,),
        opened_question_ids=("question.test",),
        initial_classification="Draft structural classification.",
        differentials=("Draft competing hypothesis.",),
        physical_examination=("Record directed examination.",),
        complementary_exams=("Record a result only when indicated.",),
        post_exam_result=None,
        expected_impression="Professional confirmation remains required.",
        audit_events=events,
        audit_hash=audit_hash_for(events),
    )


class ClinicalCaseRegistryTest(unittest.TestCase):
    def test_registers_auditable_case(self) -> None:
        registry = ClinicalCaseRegistry(module_registry(), (make_case(),))
        self.assertEqual(1, len(registry.all()))
        self.assertEqual(1, len(registry.for_module("module.test.item-1")))
        self.assertFalse(registry.all()[0].clinical_execution_allowed)

    def test_rejects_hash_mismatch(self) -> None:
        with self.assertRaisesRegex(KnowledgeError, "audit hash"):
            case = make_case()
            ClinicalTestCase(
                **{
                    field: getattr(case, field)
                    for field in case.__dataclass_fields__
                    if field != "audit_hash"
                },
                audit_hash="0" * 64,
            )

    def test_rejects_route_mismatch(self) -> None:
        case = make_case()
        values = {
            field: getattr(case, field) for field in case.__dataclass_fields__
        }
        values["obtained_route_module_ids"] = ("module.test.item-2",)
        with self.assertRaisesRegex(KnowledgeError, "routes"):
            ClinicalTestCase(**values)


if __name__ == "__main__":
    unittest.main()
