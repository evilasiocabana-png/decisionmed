import unittest
from pathlib import Path

from therapeutic_optimization import OptimizationCoordinator
from therapeutic_optimization.audit import (
    OptimizationAudit,
    OptimizationAuditEntry,
    OptimizationExecutionTrace,
    OptimizationReplay,
)
from therapeutic_optimization.goals import GoalInterpreter, GoalValidator
from therapeutic_optimization.models import ClinicalGoal, Uncertainty
from therapeutic_optimization.scoring import ConfidenceCalculator
from therapeutic_optimization.hypothesis import UncertaintyRegistry


class TherapeuticOptimizationStructureTest(unittest.TestCase):
    def test_package_structure_exists(self) -> None:
        required_dirs = [
            "coordinator",
            "goals",
            "generator",
            "comparator",
            "matcher",
            "scoring",
            "explanation",
            "hypothesis",
            "audit",
            "models",
            "integration",
        ]

        for dirname in required_dirs:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("therapeutic_optimization") / dirname).is_dir())

    def test_coordinator_returns_non_prescriptive_result(self) -> None:
        goal = ClinicalGoal("GOAL-STRUCTURAL", "structural goal", priority=1)
        result = OptimizationCoordinator().execute(
            goals=(goal,),
            safety_result={"blocking_flags": ()},
            evidence_result={"citations": ()},
        )

        self.assertEqual(result.status, "completed_read_only")
        self.assertEqual(len(result.candidate_strategies), 1)
        self.assertEqual(len(result.hypotheses), 1)
        self.assertEqual(result.hypotheses[0].candidate_strategy_id, "CAND-GOAL-STRUCTURAL")

    def test_goal_processing_and_confidence_are_structural(self) -> None:
        goals = (
            ClinicalGoal("B", "second", priority=2),
            ClinicalGoal("A", "first", priority=1),
        )
        normalized = GoalInterpreter().normalize(goals)
        validation = GoalValidator().validate(normalized)
        confidence = ConfidenceCalculator().calculate(
            knowledge_completeness=1,
            evidence_quality=0,
            constraint_coverage=1,
            missing_data=0,
        )

        self.assertEqual(normalized[0].goal_id, "A")
        self.assertFalse(validation.missing_goals)
        self.assertEqual(confidence, 0.75)

    def test_uncertainty_audit_trace_and_replay_are_structural(self) -> None:
        registry = UncertaintyRegistry()
        audit = OptimizationAudit()
        trace = OptimizationExecutionTrace(knowledge_version="0.1")
        entry = OptimizationAuditEntry(event="TherapeuticOptimizationFinished")

        registry.register(Uncertainty("missing_context", "No explicit goals."))
        audit.record(entry)
        replayed = OptimizationReplay(audit.snapshot()).replay()

        self.assertEqual(registry.all()[0].category, "missing_context")
        self.assertEqual(replayed[0].event, "TherapeuticOptimizationFinished")
        self.assertTrue(trace.trace_id.startswith("TOE-EXEC-"))

    def test_engine_does_not_prescribe_or_recommend(self) -> None:
        payload = str(OptimizationCoordinator().execute().to_dict()).lower()

        self.assertNotIn("dose recomendada", payload)
        self.assertNotIn("prescrever", payload)
        self.assertNotIn("tomar", payload)
        self.assertNotIn("estrategia superior", payload)


if __name__ == "__main__":
    unittest.main()
