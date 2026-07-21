"""Runtime explanation mapper."""

from __future__ import annotations

from typing import Any

from clinical_explanation.models import ExplanationNode, ExplanationSource


class RuntimeExplanationMapper:
    """Maps runtime artifacts into explanation nodes without interpretation."""

    def map(self, runtime_result: dict[str, Any]) -> tuple[ExplanationNode, ...]:
        outputs = runtime_result.get("result", {}).get("outputs", {})
        steps = ", ".join(outputs.keys()) if isinstance(outputs, dict) else "not_available"
        return (
            ExplanationNode(
                node_id="runtime-order",
                title="Runtime execution order",
                text=f"Completed structural steps: {steps}.",
                source=ExplanationSource("runtime", "runtime_trace"),
            ),
        )
