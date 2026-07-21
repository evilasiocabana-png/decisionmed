"""Research trace."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class ResearchTrace:
    operating_mind_version: str = "structural"
    knowledge_version: str = "structural"
    evidence_version: str = "structural"
    architecture_version: str = "structural"
    adr: str = ""
    benchmark_report: str = ""
    trace_id: str = field(default_factory=lambda: f"CRP-TRACE-{uuid4()}")

