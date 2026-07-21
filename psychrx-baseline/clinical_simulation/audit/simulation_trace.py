"""Simulation trace."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class SimulationTrace:
    twin_version: str
    operating_mind_version: str
    knowledge_version: str
    scenario_version: str
    research_version: str
    architecture_version: str
    trace_id: str = field(default_factory=lambda: f"SIM-TRACE-{uuid4()}")

