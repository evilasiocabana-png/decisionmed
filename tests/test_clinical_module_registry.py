from datetime import date, timedelta
import unittest

from decisionmed.knowledge import (
    ClinicalContentStatus,
    ClinicalEntityType,
    ClinicalModuleDefinition,
    ClinicalModuleRegistry,
    ClinicalModuleStatus,
    KnowledgeError,
    TerminologyStatus,
)


class ClinicalModuleRegistryTest(unittest.TestCase):
    def test_draft_skeleton_is_catalogued_but_never_runtime_enabled(self) -> None:
        module = self._module()
        registry = ClinicalModuleRegistry((module,))

        self.assertEqual(module, registry.require(module.module_id))
        self.assertEqual(module, registry.require("cardiovascular_discomfort"))
        self.assertFalse(module.clinical_execution_allowed)
        self.assertEqual({"cardiology": 1}, registry.counts_by_specialty())
        self.assertEqual(
            {"initial_syndrome": 1},
            registry.counts_by_entity_type(),
        )
        self.assertEqual({"draft": 1}, registry.counts_by_status())

    def test_duplicate_ids_names_and_legacy_keys_fail_closed(self) -> None:
        first = self._module()
        with self.assertRaisesRegex(KnowledgeError, "duplicate module id"):
            ClinicalModuleRegistry((first, self._module()))
        with self.assertRaisesRegex(KnowledgeError, "duplicate official name"):
            ClinicalModuleRegistry(
                (
                    first,
                    self._module(
                        module_id="module.other",
                        official_name="Sindrome toracica aguda",
                        legacy_keys=("other_legacy",),
                    ),
                )
            )
        with self.assertRaisesRegex(KnowledgeError, "duplicate legacy key"):
            ClinicalModuleRegistry(
                (
                    first,
                    self._module(
                        module_id="module.other",
                        official_name="Outra apresentação",
                    ),
                )
            )

    def test_missing_relationships_fail_closed(self) -> None:
        with self.assertRaisesRegex(KnowledgeError, "references missing modules"):
            ClinicalModuleRegistry(
                (
                    self._module(
                        parent_module_id="module.missing",
                    ),
                )
            )

    def test_validated_module_requires_complete_reviewed_sourced_content(self) -> None:
        with self.assertRaisesRegex(KnowledgeError, "validated module requires"):
            self._module(status=ClinicalModuleStatus.VALIDATED)

        reviewed_on = date.today() - timedelta(days=1)
        module = self._module(
            terminology_status=TerminologyStatus.OFFICIAL,
            content_status=ClinicalContentStatus.COMPLETE,
            status=ClinicalModuleStatus.VALIDATED,
            source_ids=("evidence.sbc.chest-pain-2025",),
            reviewed_on=reviewed_on,
            reviewed_by="reviewer.clinical",
            review_due_on=date.today() + timedelta(days=365),
        )

        self.assertEqual(ClinicalModuleStatus.VALIDATED, module.status)
        self.assertFalse(module.clinical_execution_allowed)

    @staticmethod
    def _module(**changes: object) -> ClinicalModuleDefinition:
        values: dict[str, object] = {
            "module_id": "module.cardiology.acute-thoracic-syndrome",
            "version": "0.1.0",
            "official_name": "Síndrome torácica aguda",
            "display_name": "Síndrome torácica aguda",
            "entity_type": ClinicalEntityType.INITIAL_SYNDROME,
            "primary_specialty": "cardiology",
            "legacy_keys": ("cardiovascular_discomfort",),
        }
        values.update(changes)
        return ClinicalModuleDefinition(**values)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
