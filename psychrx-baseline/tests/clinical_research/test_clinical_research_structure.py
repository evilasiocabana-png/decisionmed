import unittest
from pathlib import Path

from clinical_research import (
    AdrRequirementValidator,
    BenchmarkEngine,
    ComparisonEngine,
    ExperimentLifecycle,
    ResearchCoordinator,
    ResearchExperiment,
    ResearchGovernance,
    ScenarioRegistry,
    ValidationEngine,
)
from clinical_research.audit import ResearchReplay


class ClinicalResearchStructureTest(unittest.TestCase):
    def test_package_structure_exists(self) -> None:
        for dirname in [
            "coordinator",
            "experiments",
            "benchmark",
            "validation",
            "governance",
            "audit",
            "models",
        ]:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("clinical_research") / dirname).is_dir())

    def test_experiment_framework_is_structural(self) -> None:
        lifecycle = ExperimentLifecycle()
        scenarios = ScenarioRegistry().scenarios()

        self.assertTrue(lifecycle.can_transition("draft", "configured"))
        self.assertFalse(lifecycle.can_transition("draft", "completed"))
        self.assertGreaterEqual(len(scenarios), 2)

    def test_benchmark_validation_comparison_and_governance(self) -> None:
        benchmark = BenchmarkEngine().run(("architecture",))
        validation = ValidationEngine().validate()
        comparison = ComparisonEngine().compare("v1", "v2")
        rules = ResearchGovernance().all()
        adr_errors = AdrRequirementValidator().validate(("ADR", "benchmark report"))

        self.assertIn("architecture", benchmark.measured_items)
        self.assertIn("contract_compliance", validation.checks)
        self.assertEqual(comparison, ("comparison:v1->v2",))
        self.assertIn("Research cannot modify production", rules)
        self.assertIn("missing:documentation update", adr_errors)

    def test_research_coordinator_is_read_only_and_not_runtime_integrated(self) -> None:
        result = ResearchCoordinator().run_structural_experiment(
            ResearchExperiment(name="Operating Mind comparison", status="configured")
        )
        replayed = ResearchReplay().replay(result)
        payload = str(result.to_dict()).lower()

        self.assertEqual(result.runtime_version, "not_connected")
        self.assertEqual(result.promotion_decision.state, "Approved for Experimental Branch")
        self.assertTrue(result.read_only_mode)
        self.assertEqual(replayed, result)
        self.assertNotIn("prescrever", payload)
        self.assertNotIn("dose recomendada", payload)


if __name__ == "__main__":
    unittest.main()

