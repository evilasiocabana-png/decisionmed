"""Runtime execution monitor."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class ExecutionMonitor:
    current_engine: str | None = None
    completed_engines: tuple[str, ...] = field(default_factory=tuple)
    waiting_engines: tuple[str, ...] = field(default_factory=tuple)
    execution_duration_ms: int = 0
    blocked_engines: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
