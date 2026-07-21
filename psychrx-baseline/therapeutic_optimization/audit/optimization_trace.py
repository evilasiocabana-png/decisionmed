"""Optimization execution trace."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class OptimizationExecutionTrace:
    trace_id: str = field(default_factory=lambda: f"TOE-EXEC-{uuid4()}")
    safety_trace: str = "not_bound"
    evidence_trace: str = "not_bound"
    runtime_trace: str = "not_bound"
    knowledge_version: str = "not_bound"
