"""Safety Engine coordinator."""

from __future__ import annotations

from typing import Any

from safety_engine.alerts import AlertEngine
from safety_engine.audit import SafetyAudit, SafetyAuditEntry
from safety_engine.blocking import BlockingEngine
from safety_engine.evaluators import (
    ContraindicationEvaluator,
    ConstraintEvaluator,
    InteractionEvaluator,
    RiskEvaluator,
)
from safety_engine.models import SafetyResult
from safety_engine.snapshot import SafetySnapshotBuilder


class SafetyCoordinator:
    """Coordinates structural safety components without clinical decision logic."""

    def __init__(self) -> None:
        self.constraint_evaluator = ConstraintEvaluator()
        self.risk_evaluator = RiskEvaluator()
        self.contraindication_evaluator = ContraindicationEvaluator()
        self.interaction_evaluator = InteractionEvaluator()
        self.alert_engine = AlertEngine()
        self.blocking_engine = BlockingEngine()
        self.snapshot_builder = SafetySnapshotBuilder()
        self.audit = SafetyAudit()

    def execute(self, patient_context: dict[str, Any] | None = None) -> SafetyResult:
        context = patient_context or {}
        constraint_result = self.constraint_evaluator.evaluate(context)
        risk_result = self.risk_evaluator.evaluate(context)
        contraindication_result = self.contraindication_evaluator.evaluate(context)
        interaction_result = self.interaction_evaluator.evaluate(context)
        alerts = self.alert_engine.generate(
            constraints=constraint_result.matched_constraints,
            risks=risk_result.matched_risks,
            contraindications=contraindication_result.contraindications,
            interactions=interaction_result.interactions,
        )
        blocking_decision = self.blocking_engine.decide(alerts=alerts)
        snapshot = self.snapshot_builder.build(
            constraints=constraint_result.matched_constraints,
            risks=risk_result.matched_risks,
            contraindications=contraindication_result.contraindications,
            interactions=interaction_result.interactions,
            alerts=alerts,
            blocking_flags=blocking_decision.reasons
            if blocking_decision.status == "block"
            else (),
        )
        result = SafetyResult(
            status="completed_read_only",
            constraints=constraint_result.matched_constraints,
            risks=risk_result.matched_risks,
            contraindications=contraindication_result.contraindications,
            interactions=interaction_result.interactions,
            alerts=alerts,
            blocking_flags=blocking_decision.reasons
            if blocking_decision.status == "block"
            else (),
            blocking_decision=blocking_decision,
            snapshot=snapshot,
        )
        self.audit.record(
            SafetyAuditEntry(
                event="SafetyEvaluationFinished",
                inputs={"context_keys": tuple(sorted(context.keys()))},
                outputs={"status": result.status, "blocking": blocking_decision.status},
                trace_id=result.trace_id,
            )
        )
        return result
