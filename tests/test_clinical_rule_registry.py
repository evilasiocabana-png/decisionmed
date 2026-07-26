from datetime import date, timedelta
import unittest

from decisionmed.knowledge import (
    ClinicalContentStatus,
    ClinicalEntityType,
    ClinicalModuleDefinition,
    ClinicalModuleRegistry,
    ClinicalModuleStatus,
    ClinicalRuleCondition,
    ClinicalRuleDefinition,
    ClinicalRuleEffect,
    ClinicalRuleOperator,
    ClinicalRuleRegistry,
    ClinicalRuleStatus,
    ClinicalRuleStrength,
    KnowledgeError,
    TerminologyStatus,
)


def module() -> ClinicalModuleDefinition:
    return ClinicalModuleDefinition(
        module_id="module.cardiology.acute-thoracic-syndrome",
        version="0.1.0",
        official_name="Síndrome torácica aguda",
        display_name="Síndrome torácica aguda",
        entity_type=ClinicalEntityType.INITIAL_SYNDROME,
        primary_specialty="cardiology",
        legacy_keys=("cardiovascular_discomfort",),
    )


def condition() -> ClinicalRuleCondition:
    return ClinicalRuleCondition(
        all_of=(
            ClinicalRuleCondition(
                fact="complaint",
                operator=ClinicalRuleOperator.EQUALS,
                value="Dor",
            ),
            ClinicalRuleCondition(
                fact="values",
                operator=ClinicalRuleOperator.CONTAINS_ANY,
                values=("Peito", "Braço / ombro"),
            ),
        )
    )


def rule(**overrides: object) -> ClinicalRuleDefinition:
    values: dict[str, object] = {
        "rule_id": "route.pattern.acute-thoracic",
        "module_id": "module.cardiology.acute-thoracic-syndrome",
        "version": "0.1.0",
        "effect": ClinicalRuleEffect.ROUTE,
        "strength": ClinicalRuleStrength.MODERATE,
        "rationale": "Combinação abre revisão cardiovascular.",
        "when": condition(),
        "output_key": "cardiology",
    }
    values.update(overrides)
    return ClinicalRuleDefinition(**values)


class ClinicalRuleRegistryTest(unittest.TestCase):
    def test_nested_rule_is_registered_but_never_authorizes_execution(self) -> None:
        modules = ClinicalModuleRegistry((module(),))
        registry = ClinicalRuleRegistry(modules, (rule(),))

        stored = registry.require("route.pattern.acute-thoracic")

        self.assertEqual(
            "module.cardiology.acute-thoracic-syndrome",
            stored.module_id,
        )
        self.assertEqual(
            stored,
            registry.for_module("cardiovascular_discomfort")[0],
        )
        self.assertFalse(stored.clinical_execution_allowed)
        self.assertEqual({"draft": 1}, registry.counts_by_status())

    def test_missing_module_and_duplicate_rule_fail_closed(self) -> None:
        modules = ClinicalModuleRegistry((module(),))
        with self.assertRaises(KnowledgeError):
            ClinicalRuleRegistry(
                modules,
                (
                    rule(
                        module_id="module.cardiology.missing",
                    ),
                ),
            )
        with self.assertRaises(KnowledgeError):
            ClinicalRuleRegistry(modules, (rule(), rule()))

    def test_operator_specific_fields_are_strict(self) -> None:
        with self.assertRaises(KnowledgeError):
            ClinicalRuleCondition(
                fact="values",
                operator=ClinicalRuleOperator.COUNT_AT_LEAST,
                values=("Peito",),
                threshold=2,
            )
        with self.assertRaises(KnowledgeError):
            ClinicalRuleCondition(
                fact="note",
                operator=ClinicalRuleOperator.MATCHES,
                pattern="(",
            )
        with self.assertRaises(KnowledgeError):
            ClinicalRuleCondition(
                fact="complaint",
                operator=ClinicalRuleOperator.PRESENT,
                value="not-allowed",
            )

    def test_validated_rule_requires_complete_review_metadata(self) -> None:
        with self.assertRaises(KnowledgeError):
            rule(status=ClinicalRuleStatus.VALIDATED)

        reviewed_on = date.today() - timedelta(days=1)
        validated = rule(
            rule_id="route.pattern.reviewed",
            status=ClinicalRuleStatus.VALIDATED,
            source_ids=("evidence.source",),
            reviewed_on=reviewed_on,
            reviewed_by="reviewer.clinical",
            review_due_on=date.today() + timedelta(days=365),
        )
        self.assertEqual(ClinicalRuleStatus.VALIDATED, validated.status)

    def test_non_route_rule_requires_a_display_output(self) -> None:
        with self.assertRaises(KnowledgeError):
            rule(
                effect=ClinicalRuleEffect.SUPPORT,
                output_key=None,
            )

        support = rule(
            rule_id="support.differential.musculoskeletal",
            effect=ClinicalRuleEffect.SUPPORT,
            output_key=None,
            output_value="Dor musculoesquelética da parede torácica",
        )

        self.assertEqual(
            "Dor musculoesquelética da parede torácica",
            support.output_value,
        )


if __name__ == "__main__":
    unittest.main()
