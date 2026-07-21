"""Runtime execution trace."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class ExecutionTrace:
    trace_id: str = field(default_factory=lambda: f"TRC-{uuid4()}")
    parent_trace: str | None = None
    execution_tree: tuple[str, ...] = field(default_factory=tuple)
    engine_tree: tuple[str, ...] = field(default_factory=tuple)
    widget_tree: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
