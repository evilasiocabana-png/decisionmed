import unittest
from pathlib import Path

from safety_engine import SafetyCoordinator
from safety_engine.alerts import AlertEngine, AlertFormatter
from safety_engine.audit import SafetyAudit, SafetyAuditEntry, SafetyReplay, SafetyTrace
from safety_engine.blocking import BlockingEngine
from safety_engine.evaluators import ConstraintEvaluator, RiskEvaluator
from safety_engine.models import Constraint, Risk
from safety_engine.registry import ConstraintRegistry, RiskRegistry


class SafetyEngineStructureTest(unittest.TestCase):
    def test_safety_engine_package_structure_exists(self) -> None:
        required_dirs = [
            "coordinator",
            "evaluators",
            "alerts",
            "blocking",
            "snapshot",
            "audit",
            "models",
            "registry",
            "integration",
        ]

        for dirname in required_dirs:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("safety_engine") / dirname).is_dir())

    def test_coordinator_returns_structural_safety_result(self) -> None:
        result = SafetyCoordinator().execute({"patient": "structural"})

        self.assertEqual(result.status, "completed_read_only")
        self.assertEqual(result.blocking_decision.status, "allow")
        self.assertEqual(result.snapshot.status, "evaluated_read_only")
        self.assertEqual(result.alerts, ())

    def test_registries_and_evaluators_do_not_hardcode_clinical_rules(self) -> None:
        constraint_registry = ConstraintRegistry()
        risk_registry = RiskRegistry()
        constraint = Constraint("CONSTRAINT-STRUCTURAL", category="test")
        risk = Risk("RISK-STRUCTURAL", category="test")

        constraint_registry.register(constraint)
        risk_registry.register(risk)

        constraints = ConstraintEvaluator(constraint_registry).evaluate({})
        risks = RiskEvaluator(risk_registry).evaluate({})

        self.assertEqual(constraints.matched_constraints, (constraint,))
        self.assertEqual(risks.matched_risks, (risk,))
        self.assertEqual(constraint_registry.categories(), ("test",))
        self.assertEqual(risk_registry.categories(), ("test",))

    def test_alert_blocking_audit_trace_and_replay_are_structural(self) -> None:
        critical_risk = Risk("RISK-CRITICAL-STRUCTURAL", severity="critical")
        alerts = AlertEngine().generate(risks=(critical_risk,))
        decision = BlockingEngine().decide(alerts=alerts)
        audit = SafetyAudit()
        entry = SafetyAuditEntry(event="SafetyEvaluationFinished")
        trace = SafetyTrace(evaluated_components=("RiskEvaluator",))

        audit.record(entry)
        replayed = SafetyReplay(audit.snapshot()).replay()

        self.assertEqual(len(alerts), 1)
        self.assertEqual(decision.status, "block")
        self.assertIn("Structured safety item", AlertFormatter().for_log(alerts[0]))
        self.assertEqual(replayed[0].event, "SafetyEvaluationFinished")
        self.assertTrue(trace.trace_id.startswith("SFT-TRC-"))

    def test_safety_engine_does_not_prescribe(self) -> None:
        payload = str(SafetyCoordinator().execute({}).to_dict()).lower()

        self.assertNotIn("dose recomendada", payload)
        self.assertNotIn("prescrever", payload)
        self.assertNotIn("medicamento escolhido", payload)


if __name__ == "__main__":
    unittest.main()
