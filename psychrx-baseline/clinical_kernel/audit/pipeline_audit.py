"""Structural audit metadata for the Clinical Kernel."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class PipelineAudit:
    """In-memory structural audit metadata, not medico-legal persistence."""

    pipeline_started: bool = True
    planned_steps: tuple[str, ...] = field(default_factory=tuple)
    blocked_steps: tuple[str, ...] = field(default_factory=tuple)
    mode: str = "read-only"
    clinical_reasoning: str = "not_implemented"
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_metadata(self) -> dict[str, Any]:
        """Return audit metadata for KernelResult."""
        return {
            "pipeline_started": self.pipeline_started,
            "planned_steps": self.planned_steps,
            "blocked_steps": self.blocked_steps,
            "mode": self.mode,
            "clinical_reasoning": self.clinical_reasoning,
            "timestamp": self.timestamp,
        }
