"""Safety trace wrapper."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class SafetyTrace:
    trace_id: str = field(default_factory=lambda: f"SFT-TRC-{uuid4()}")
    origin: str = "safety_engine"
    runtime_trace: str = "not_bound"
    evidence_references: tuple[str, ...] = field(default_factory=tuple)
    evaluated_components: tuple[str, ...] = field(default_factory=tuple)
