import unittest
from pathlib import Path

from digital_clinical_twin import (
    EvolutionEngine,
    TransitionRegistry,
    TwinBuilder,
    TwinComparisonEngine,
    TwinCompatibility,
    TwinCoordinator,
    TwinMigrationPlanner,
    TwinReplay,
    TwinStabilityAnalyzer,
    TwinState,
    TwinStateManager,
    TwinValidator,
    TwinVersionManager,
)


class DigitalClinicalTwinStructureTest(unittest.TestCase):
    def test_package_structure_exists(self) -> None:
        for dirname in [
            "coordinator",
            "builder",
            "state",
            "evolution",
            "comparison",
            "stability",
            "versioning",
            "audit",
            "models",
        ]:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("digital_clinical_twin") / dirname).is_dir())

    def test_builder_validator_and_state_manager_are_immutable(self) -> None:
        twin = TwinBuilder().build(snapshot_ids=("SNP-1", "SNP-2"))
        updated = TwinStateManager().update_state(twin, TwinState(name="new_state"), "Quality")

        self.assertEqual(TwinValidator().validate(twin), ())
        self.assertNotEqual(twin.current_state.state_id, updated.current_state.state_id)
        self.assertEqual(len(updated.state_transitions), len(twin.state_transitions) + 1)
        self.assertTrue(twin.read_only_mode)

    def test_evolution_stability_comparison_versioning_and_migration(self) -> None:
        twin = TwinCoordinator().build_twin()
        changed = TwinBuilder().build(snapshot_ids=("SNP-1", "SNP-3"), knowledge_versions=("0.2.0",))

        self.assertIn("Context", TransitionRegistry().categories())
        self.assertIn("quality_evolution:structural", EvolutionEngine().track(twin))
        self.assertIn("trace_continuity:True", TwinStabilityAnalyzer().analyze(twin))
        self.assertIn("timeline_differences", TwinComparisonEngine().compare(twin, changed))
        self.assertEqual(TwinCompatibility().validate(twin), ())
        self.assertEqual(TwinVersionManager().create(1, 2, 3).value(), "1.2.3")
        self.assertIn(
            "automatic_migration:not_allowed",
            TwinMigrationPlanner().plan(("schema",), ("knowledge",), ("version",)),
        )

    def test_coordinator_summary_and_replay_are_non_prescriptive(self) -> None:
        coordinator = TwinCoordinator()
        twin = coordinator.build_twin()
        summary = coordinator.summarize(twin)
        replayed = TwinReplay().replay(twin)
        payload = str(twin.to_dict()).lower()

        self.assertEqual(summary.current_state, "computational_state")
        self.assertEqual(replayed, twin)
        self.assertNotIn("prescrever", payload)
        self.assertNotIn("dose recomendada", payload)
        self.assertNotIn("diagnostico definitivo", payload)


if __name__ == "__main__":
    unittest.main()

