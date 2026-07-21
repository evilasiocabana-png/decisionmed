import unittest
from pathlib import Path

from clinical_operating_mind import (
    ClinicalOperatingMindCoordinator,
    EngineContractRegistry,
    GovernanceRuleRegistry,
    LifecycleDefinition,
    OperatingMindStateMachine,
    TransitionValidator,
)
from clinical_operating_mind.governance import SafetyGovernanceGate, StructuralChangeGuard
from clinical_operating_mind.models import ClinicalOperatingMindState
from clinical_operating_mind.replay import OperatingMindReplay


class ClinicalOperatingMindStructureTest(unittest.TestCase):
    def test_package_structure_exists(self) -> None:
        for dirname in [
            "coordinator",
            "state",
            "contracts",
            "lifecycle",
            "transitions",
            "governance",
            "audit",
            "models",
            "replay",
            "integration",
        ]:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("clinical_operating_mind") / dirname).is_dir())

    def test_lifecycle_preserves_official_engine_order(self) -> None:
        lifecycle = LifecycleDefinition().build()
        self.assertEqual(
            tuple(phase.required_engine for phase in lifecycle.phases),
            (
                "Runtime",
                "Safety",
                "Evidence",
                "Optimization",
                "Explanation",
                "Snapshot",
                "Timeline",
                "Navigation",
            ),
        )
        self.assertEqual(lifecycle.phases[1].name, "Safety Evaluation")

    def test_state_machine_and_transition_validator_block_shortcuts(self) -> None:
        machine = OperatingMindStateMachine()
        validator = TransitionValidator()

        self.assertTrue(machine.can_transition("context_loaded", "safety_checked"))
        self.assertFalse(machine.can_transition("context_loaded", "hypotheses_generated"))
        self.assertIn(
            "skipped_phase:Safety Evaluation",
            validator.validate_completed(("Context Intake", "Evidence Resolution")),
        )

    def test_contracts_governance_safety_gate_and_replay_are_structural(self) -> None:
        contracts = EngineContractRegistry().operating_contracts()
        rules = GovernanceRuleRegistry().all()
        safety_allowed, blocking_reason = SafetyGovernanceGate().evaluate(
            {"blocking_decision": {"status": "blocked"}}
        )
        guard_errors = StructuralChangeGuard().validate("lifecycle")
        state = ClinicalOperatingMindState(status="navigation_ready")

        self.assertEqual(len(contracts), 8)
        self.assertIn("Safety before Optimization", rules)
        self.assertFalse(safety_allowed)
        self.assertEqual(blocking_reason, "safety_blocking_decision")
        self.assertEqual(guard_errors, ("adr_required:lifecycle",))
        self.assertEqual(OperatingMindReplay().replay(state), state)

    def test_coordinator_outputs_read_only_non_prescriptive_result(self) -> None:
        result = ClinicalOperatingMindCoordinator().coordinate(
            {"status": "ok", "trace_id": "SAFETY-1", "blocking_decision": {"status": "allow"}},
            {"status": "ok", "trace_id": "EVIDENCE-1"},
            {"status": "ok", "trace_id": "OPT-1"},
            {"status": "ok", "trace": {"trace_id": "EXP-1"}},
            {"snapshot_id": "SNP-1"},
            {"timeline_id": "TML-1"},
            {"navigation_id": "NAV-1"},
        )
        payload = str(result.to_dict()).lower()

        self.assertEqual(result.state.status, "navigation_ready")
        self.assertTrue(result.state.read_only_mode)
        self.assertTrue(result.state.trace.complete())
        self.assertEqual(result.clinical_decision, "not_implemented")
        self.assertEqual(result.prescription, "not_available")
        self.assertNotIn("dose recomendada", payload)
        self.assertNotIn("prescrever agora", payload)


if __name__ == "__main__":
    unittest.main()

