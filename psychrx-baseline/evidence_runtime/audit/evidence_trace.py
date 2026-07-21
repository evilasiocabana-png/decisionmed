"""Evidence trace model."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class EvidenceTrace:
    trace_id: str = field(default_factory=lambda: f"EVD-TRC-{uuid4()}")
    origin: str = "evidence_runtime"
    version: str = "not_bound"
    selection_reason: str = "structural selection"
    execution_trace: str = "not_bound"
