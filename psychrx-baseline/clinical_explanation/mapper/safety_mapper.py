"""Safety explanation mapper."""

from __future__ import annotations

from typing import Any

from clinical_explanation.models import ExplanationNode, ExplanationSource


class SafetyExplanationMapper:
    """Maps SafetyResult into explanation nodes without altering it."""

    def map(self, safety_result: dict[str, Any]) -> tuple[ExplanationNode, ...]:
        decision = safety_result.get("blocking_decision", {}).get("status", "not_available")
        alerts = safety_result.get("snapshot", {}).get("alert_count", 0)
        return (
            ExplanationNode(
                node_id="safety-summary",
                title="Safety findings",
                text=f"SafetyResult was reviewed structurally. Blocking status: {decision}. Alerts: {alerts}.",
                source=ExplanationSource("safety", "safety_result"),
            ),
        )
