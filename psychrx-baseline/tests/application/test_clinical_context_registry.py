import unittest

from application.clinical_context_registry import ClinicalContextRegistry


class ClinicalContextRegistryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = ClinicalContextRegistry()

    def test_registry_covers_priority_context_categories(self) -> None:
        categories = {item.category for item in self.registry.all()}

        self.assertTrue({"acute_risk", "adverse_syndrome", "substance_context", "diagnostic_boundary", "population_boundary"}.issubset(categories))
        self.assertGreaterEqual(len(self.registry.all()), 20)

    def test_registry_never_authorizes_treatment_rules(self) -> None:
        self.assertTrue(all(not item.treatment_rule_allowed for item in self.registry.all()))

    def test_blocking_context_interrupts_routine_ranking(self) -> None:
        result = self.registry.assess(("DELIRIUM_CONCERN", "SEROTONIN_SYNDROME"))

        self.assertEqual(2, len(result.selected))
        self.assertEqual(2, len(result.blocking_warnings))

    def test_review_context_is_recorded_without_invented_blocking_rule(self) -> None:
        result = self.registry.assess(("CANNABIS_CONTEXT", "AKATHISIA"))

        self.assertEqual(2, len(result.display_lines()))
        self.assertEqual((), result.blocking_warnings)

    def test_unknown_context_is_explicitly_blocked(self) -> None:
        result = self.registry.assess(("NOT_REGISTERED",))

        self.assertEqual(("NOT_REGISTERED",), result.unknown_ids)
        self.assertIn("Contexto clinico desconhecido", result.blocking_warnings[0])


if __name__ == "__main__":
    unittest.main()
