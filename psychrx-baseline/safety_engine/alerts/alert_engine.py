"""Structured alert generation from Safety Engine outputs."""

from __future__ import annotations

from safety_engine.models import Alert, Constraint, Contraindication, Interaction, Risk


class AlertEngine:
    """Generates structural alerts without writing clinical recommendations."""

    def generate(
        self,
        constraints: tuple[Constraint, ...] = (),
        risks: tuple[Risk, ...] = (),
        contraindications: tuple[Contraindication, ...] = (),
        interactions: tuple[Interaction, ...] = (),
    ) -> tuple[Alert, ...]:
        alerts = []
        for item in (*constraints, *risks, *contraindications, *interactions):
            if item.severity in ("critical", "blocking", "restriction"):
                alerts.append(
                    Alert(
                        alert_id=f"ALERT-{getattr(item, 'constraint_id', getattr(item, 'risk_id', getattr(item, 'contraindication_id', getattr(item, 'interaction_id', 'unknown'))))}",
                        category=item.__class__.__name__,
                        severity=item.severity,
                        priority="critical" if item.severity == "critical" else "high",
                        message="Structured safety item requires medical review.",
                        trace=item.trace,
                    )
                )
        return tuple(alerts)
