"""Runtime pipeline result."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class PipelineResult:
    status: str
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    outputs: dict[str, Any] = field(default_factory=dict)
    duration_ms: int = 0
    trace_id: str = field(default_factory=lambda: f"TRC-{uuid4()}")
    execution_id: str = field(default_factory=lambda: f"EXE-{uuid4()}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
