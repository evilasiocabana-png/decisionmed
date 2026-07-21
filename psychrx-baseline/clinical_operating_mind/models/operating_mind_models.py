"""Immutable models for the Clinical Operating Mind."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class OperatingMindPhase:
    name: str
    order: int
    required_engine: str
    purpose: str


@dataclass(frozen=True)
class OperatingMindTransition:
    source: str
    target: str
    required_trace: str = ""
    allowed: bool = True
    reason: str = ""


@dataclass(frozen=True)
class OperatingMindLifecycle:
    phases: tuple[OperatingMindPhase, ...] = field(default_factory=tuple)
    transitions: tuple[OperatingMindTransition, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class OperatingMindContract:
    engine: str
    input_contract: tuple[str, ...]
    output_contract: tuple[str, ...]
    immutable_upstream: bool = True
    trace_required: bool = True
    failure_behavior: str = "return_structured_error"


@dataclass(frozen=True)
class OperatingMindAudit:
    event: str
    phase: str = ""
    transition: str = ""
    validation_result: str = "not_evaluated"
    trace_id: str = field(default_factory=lambda: f"OM-AUD-{uuid4()}")
    timestamp: str = field(default_factory=_utc_now)


@dataclass(frozen=True)
class OperatingMindTrace:
    runtime_trace: str = "runtime-structural"
    safety_trace: str = ""
    evidence_trace: str = ""
    optimization_trace: str = ""
    explanation_trace: str = ""
    snapshot_id: str = ""
    timeline_id: str = ""
    navigation_session: str = ""
    trace_id: str = field(default_factory=lambda: f"OM-TRC-{uuid4()}")

    def complete(self) -> bool:
        return all(
            (
                self.runtime_trace,
                self.safety_trace,
                self.evidence_trace,
                self.optimization_trace,
                self.explanation_trace,
                self.snapshot_id,
                self.timeline_id,
                self.navigation_session,
            )
        )


@dataclass(frozen=True)
class ClinicalOperatingMindState:
    mind_id: str = field(default_factory=lambda: f"OM-{uuid4()}")
    status: str = "idle"
    current_phase: str = "Context Intake"
    completed_phases: tuple[str, ...] = field(default_factory=tuple)
    lifecycle: OperatingMindLifecycle = field(default_factory=OperatingMindLifecycle)
    contracts: tuple[OperatingMindContract, ...] = field(default_factory=tuple)
    audit: tuple[OperatingMindAudit, ...] = field(default_factory=tuple)
    trace: OperatingMindTrace = field(default_factory=OperatingMindTrace)
    governance_warnings: tuple[str, ...] = field(default_factory=tuple)
    blocking_reason: str = ""
    read_only_mode: bool = True

    def with_update(self, **changes: Any) -> "ClinicalOperatingMindState":
        return replace(self, **changes)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class OperatingMindResult:
    state: ClinicalOperatingMindState
    validation_errors: tuple[str, ...] = field(default_factory=tuple)
    blocked: bool = False
    prescription: str = "not_available"
    clinical_decision: str = "not_implemented"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

