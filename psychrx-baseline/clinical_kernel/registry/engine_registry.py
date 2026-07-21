"""Read-only registry of future Clinical Kernel engines."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EngineDescriptor:
    """Structural descriptor for a future engine."""

    name: str
    status: str = "future_integration"


class EngineRegistry:
    """Registry skeleton. It does not instantiate or execute clinical engines."""

    _engine_names = (
        "Investigation Engine",
        "Snapshot Engine",
        "Safety Engine",
        "Objective Engine",
        "Strategy Engine",
        "Monitoring Engine",
        "Explanation Engine",
    )

    def list_engines(self) -> tuple[EngineDescriptor, ...]:
        """Return all future engines as unavailable placeholders."""
        return tuple(EngineDescriptor(name=name) for name in self._engine_names)
