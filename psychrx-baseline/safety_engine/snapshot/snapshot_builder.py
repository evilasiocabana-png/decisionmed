"""Safety Snapshot builder."""

from __future__ import annotations

from safety_engine.models import Alert, Constraint, Contraindication, Interaction, Risk, SafetySnapshot


class SafetySnapshotBuilder:
    """Builds a compact read-only safety summary."""

    def build(
        self,
        constraints: tuple[Constraint, ...] = (),
        risks: tuple[Risk, ...] = (),
        contraindications: tuple[Contraindication, ...] = (),
        interactions: tuple[Interaction, ...] = (),
        alerts: tuple[Alert, ...] = (),
        blocking_flags: tuple[str, ...] = (),
    ) -> SafetySnapshot:
        status = "blocked" if blocking_flags else "evaluated_read_only"
        return SafetySnapshot(
            status=status,
            alert_count=len(alerts),
            blocking_count=len(blocking_flags),
            constraint_count=len(constraints),
            risk_count=len(risks),
            interaction_count=len(interactions),
            contraindication_count=len(contraindications),
        )
