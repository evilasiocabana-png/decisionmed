"""Intelligence trace."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class IntelligenceTrace:
    operating_mind_version: str
    knowledge_version: str
    scientific_validation_version: str
    semantic_version: str
    quality_result: str
    simulation_version: str = ""
    trace_id: str = field(default_factory=lambda: f"CIP-TRACE-{uuid4()}")

