"""Structural Clinical Pipeline skeleton."""

from __future__ import annotations

from clinical_kernel.context.clinical_context import ClinicalContext
from clinical_kernel.execution.engine_executor import EngineExecutor
from clinical_kernel.execution.kernel_result import KernelResult
from clinical_kernel.registry.engine_registry import EngineRegistry


class PipelineSkeleton:
    """Read-only pipeline skeleton. It does not execute clinical reasoning."""

    steps = (
        "ClinicalContext",
        "Investigation",
        "Snapshot",
        "Safety",
        "Objectives",
        "Strategy Block",
        "Monitoring",
        "Explanation",
    )

    def __init__(
        self,
        registry: EngineRegistry | None = None,
        executor: EngineExecutor | None = None,
    ) -> None:
        self._registry = registry or EngineRegistry()
        self._executor = executor or EngineExecutor()

    def run(self, context: ClinicalContext | None = None) -> KernelResult:
        """Return a structural blocked result without clinical execution."""
        result = self._executor.execute(self._registry.list_engines())
        return KernelResult(
            status=result.status,
            context=context or ClinicalContext.empty(),
            messages=result.messages + ("Pipeline skeleton completed read-only.",),
            warnings=result.warnings,
            blocked_reason=result.blocked_reason,
            audit_metadata={
                **result.audit_metadata,
                "pipeline_steps": self.steps,
                "read_only": True,
            },
        )
