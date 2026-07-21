"""Runtime adapter for Safety Engine."""

from __future__ import annotations

from clinical_runtime.context import RuntimeContext
from safety_engine import SafetyCoordinator, SafetyResult


class RuntimeSafetyAdapter:
    """Runs Safety Engine from Clinical Runtime context in read-only mode."""

    def __init__(self, coordinator: SafetyCoordinator | None = None) -> None:
        self._coordinator = coordinator or SafetyCoordinator()

    def evaluate(self, context: RuntimeContext | None = None) -> SafetyResult:
        runtime_context = context or RuntimeContext()
        return self._coordinator.execute(runtime_context.to_dict())
