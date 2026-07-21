"""Twin trace."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class TwinTrace:
    operating_mind_version: str
    snapshot_ids: tuple[str, ...]
    timeline_version: str
    knowledge_version: str
    quality_results: tuple[str, ...]
    scientific_validation_version: str
    semantic_version: str
    trace_id: str = field(default_factory=lambda: f"DCT-TRACE-{uuid4()}")

