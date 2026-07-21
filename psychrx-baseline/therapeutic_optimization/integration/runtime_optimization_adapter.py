"""Runtime adapter for Therapeutic Optimization Engine."""

from __future__ import annotations

from clinical_runtime.context import RuntimeContext
from therapeutic_optimization import OptimizationCoordinator, TherapeuticOptimizationResult


class RuntimeOptimizationAdapter:
    """Runs therapeutic optimization structurally in read-only mode."""

    def __init__(self, coordinator: OptimizationCoordinator | None = None) -> None:
        self._coordinator = coordinator or OptimizationCoordinator()

    def optimize(
        self,
        context: RuntimeContext | None = None,
        safety_result: dict[str, object] | None = None,
        evidence_result: dict[str, object] | None = None,
    ) -> TherapeuticOptimizationResult:
        _ = context or RuntimeContext()
        return self._coordinator.execute(
            goals=(),
            safety_result=safety_result or {},
            evidence_result=evidence_result or {},
            knowledge_context={},
        )
