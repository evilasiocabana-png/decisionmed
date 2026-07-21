"""Structural blocking decision engine."""

from __future__ import annotations

from safety_engine.models import Alert, BlockingDecision


class BlockingEngine:
    """Produces generic execution gates without prescribing or treating."""

    def decide(
        self,
        blocking_flags: tuple[str, ...] = (),
        alerts: tuple[Alert, ...] = (),
    ) -> BlockingDecision:
        if blocking_flags:
            return BlockingDecision(
                status="block",
                reasons=blocking_flags,
                explanation="Execution blocked by structural safety flags.",
            )
        if any(alert.priority == "critical" for alert in alerts):
            return BlockingDecision(
                status="block",
                reasons=tuple(alert.alert_id for alert in alerts if alert.priority == "critical"),
                explanation="Execution blocked by critical structural alerts.",
            )
        if alerts:
            return BlockingDecision(
                status="allow_with_warning",
                reasons=tuple(alert.alert_id for alert in alerts),
                explanation="Execution allowed structurally with warnings for medical review.",
            )
        return BlockingDecision()
