"""Immutable models for Clinical Simulation Platform."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class SimulationSandbox:
    sandbox_id: str = field(default_factory=lambda: f"SBX-{uuid4()}")
    isolated: bool = True
    temporary_state: bool = True
    cleanup_policy: str = "automatic"
    version: str = "0.1.0"


@dataclass(frozen=True)
class TwinClone:
    clone_id: str = field(default_factory=lambda: f"CLONE-{uuid4()}")
    source_twin_id: str = ""
    snapshot_refs: tuple[str, ...] = field(default_factory=tuple)
    timeline_ref: str = ""
    knowledge_version: str = ""
    operating_mind_version: str = ""
    quality_refs: tuple[str, ...] = field(default_factory=tuple)
    shared_mutable_state: bool = False


@dataclass(frozen=True)
class SimulationScenario:
    scenario_id: str = field(default_factory=lambda: f"SCN-SIM-{uuid4()}")
    scenario_type: str = "architecture"
    status: str = "draft"
    version: str = "0.1.0"
    inputs: tuple[str, ...] = field(default_factory=tuple)
    dependencies: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class SimulationBranch:
    branch_id: str = field(default_factory=lambda: f"BR-{uuid4()}")
    scenario_id: str = ""
    parent_clone_id: str = ""
    immutable_history: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class SimulationOutcome:
    outcome_id: str = field(default_factory=lambda: f"OUT-{uuid4()}")
    status: str = "completed"
    differences: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class SimulationComparison:
    comparison_id: str = field(default_factory=lambda: f"CMP-SIM-{uuid4()}")
    original_twin: str = ""
    simulated_twin: str = ""
    branch_differences: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class SimulationReport:
    report_id: str = field(default_factory=lambda: f"SIM-RPT-{uuid4()}")
    scenario: str = ""
    changes: tuple[str, ...] = field(default_factory=tuple)
    branch_summary: str = ""
    limitations: tuple[str, ...] = ("research_artifact_only", "no_clinical_recommendations")
    quality: str = "structural"
    trace: str = ""


@dataclass(frozen=True)
class ClinicalSimulationResult:
    simulation_id: str = field(default_factory=lambda: f"SIM-{uuid4()}")
    sandbox_id: str = ""
    twin_clone_id: str = ""
    scenario_id: str = ""
    execution_plan: tuple[str, ...] = field(default_factory=tuple)
    simulation_branch: SimulationBranch = field(default_factory=SimulationBranch)
    simulation_outcome: SimulationOutcome = field(default_factory=SimulationOutcome)
    comparison: SimulationComparison = field(default_factory=SimulationComparison)
    limitations: tuple[str, ...] = ("isolated_sandbox_only", "not_clinical_output")
    metadata: tuple[str, ...] = field(default_factory=tuple)
    trace_id: str = field(default_factory=lambda: f"SIM-TRC-{uuid4()}")
    timestamp: str = field(default_factory=_now)
    read_only_mode: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

