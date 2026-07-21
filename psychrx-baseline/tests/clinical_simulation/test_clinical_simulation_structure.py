import unittest
from pathlib import Path

from clinical_simulation import (
    BranchEngine,
    OutcomeComparator,
    ScenarioLifecycle,
    ScenarioRegistry,
    ScenarioValidator,
    SimulationCoordinator,
    SimulationExport,
    SimulationReplay,
    SimulationReportEngine,
    SimulationRunner,
    SimulationSandboxEngine,
    SimulationScenario,
    TwinCloneEngine,
)
from digital_clinical_twin import TwinCoordinator


class ClinicalSimulationStructureTest(unittest.TestCase):
    def test_package_structure_exists(self) -> None:
        for dirname in [
            "coordinator",
            "sandbox",
            "scenario",
            "branch",
            "comparison",
            "reports",
            "audit",
            "models",
            "runner",
        ]:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("clinical_simulation") / dirname).is_dir())

    def test_sandbox_clone_and_scenario_validation_are_isolated(self) -> None:
        twin = TwinCoordinator().build_twin()
        sandbox = SimulationSandboxEngine().create()
        clone = TwinCloneEngine().clone(twin)
        scenario = SimulationScenario(status="validated", inputs=("input",))

        self.assertTrue(sandbox.isolated)
        self.assertFalse(clone.shared_mutable_state)
        self.assertEqual(clone.source_twin_id, twin.twin_id)
        self.assertEqual(ScenarioValidator().validate(scenario, sandbox, clone), ())
        self.assertTrue(ScenarioLifecycle().can_transition("draft", "configured"))
        self.assertEqual(ScenarioRegistry().register(scenario), scenario)

    def test_branch_runner_comparison_report_export_and_replay(self) -> None:
        twin = TwinCoordinator().build_twin()
        sandbox = SimulationSandboxEngine().create()
        clone = TwinCloneEngine().clone(twin)
        scenario = SimulationScenario(status="validated", inputs=("input",))
        branch = BranchEngine().create(scenario, clone)
        outcome = SimulationRunner().run(sandbox, scenario, branch)
        comparison = OutcomeComparator().compare(clone, clone, (branch,))
        report = SimulationReportEngine().generate(scenario, branch, comparison.comparison_id)
        result = SimulationCoordinator().simulate(scenario)

        self.assertEqual(outcome.status, "completed")
        self.assertIn(f"branch:{branch.branch_id}", comparison.branch_differences)
        self.assertEqual(SimulationExport().export(report, "internal_json")[0], "exported")
        self.assertEqual(SimulationExport().export(report, "production")[0], "rejected")
        self.assertEqual(SimulationReplay().replay(result), result)

    def test_simulation_coordinator_is_non_prescriptive(self) -> None:
        result = SimulationCoordinator().simulate()
        payload = str(result.to_dict()).lower()

        self.assertTrue(result.read_only_mode)
        self.assertIn("does_not_modify_official_twin", result.limitations)
        self.assertNotIn("prescrever", payload)
        self.assertNotIn("dose recomendada", payload)
        self.assertNotIn("diagnostico definitivo", payload)


if __name__ == "__main__":
    unittest.main()

