"""Structural executor for future Clinical Kernel engines."""

from __future__ import annotations

from clinical_kernel.execution.kernel_result import KernelResult
from clinical_kernel.registry.engine_registry import EngineDescriptor


class EngineExecutor:
    """Executor skeleton that never runs clinical logic."""

    def execute(self, engines: tuple[EngineDescriptor, ...]) -> KernelResult:
        """Return a blocked read-only result for all future engines."""
        engine_names = tuple(engine.name for engine in engines)
        result = KernelResult.read_only_blocked()
        return KernelResult(
            status=result.status,
            context=result.context,
            messages=result.messages
            + tuple(f"{name}: future_integration" for name in engine_names),
            warnings=result.warnings,
            blocked_reason=result.blocked_reason,
            audit_metadata={
                **result.audit_metadata,
                "engines": engine_names,
                "engine_execution": "not_implemented",
            },
        )
