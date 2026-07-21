"""Runtime adapter for Evidence Runtime."""

from __future__ import annotations

from clinical_runtime.context import RuntimeContext
from evidence_runtime import EvidenceCoordinator, EvidenceRequest, EvidenceResult


class RuntimeEvidenceAdapter:
    """Runs Evidence Runtime from Clinical Runtime context in read-only mode."""

    def __init__(self, coordinator: EvidenceCoordinator | None = None) -> None:
        self._coordinator = coordinator or EvidenceCoordinator()

    def resolve(self, context: RuntimeContext | None = None) -> EvidenceResult:
        runtime_context = context or RuntimeContext()
        request = EvidenceRequest(
            query=str(runtime_context.current_hypothesis or ""),
            category="",
            scope="",
            status="",
        )
        return self._coordinator.execute(request)
