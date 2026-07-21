"""Scientific validation trace."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class ScientificTrace:
    source: str
    version: str
    review: str
    editorial_decision: str
    publication_report: str
    knowledge_version: str
    trace_id: str = field(default_factory=lambda: f"SVF-TRACE-{uuid4()}")

