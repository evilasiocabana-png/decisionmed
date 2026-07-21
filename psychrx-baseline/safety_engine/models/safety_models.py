"""Typed Safety Engine models with no embedded clinical knowledge."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

CLASSIFICATION_LEVELS = (
    "informational",
    "caution",
    "restriction",
    "blocking",
    "critical",
)

ALERT_PRIORITIES = ("critical", "high", "medium", "low", "informational")


@dataclass(frozen=True)
class SafetyTraceReference:
    """Trace metadata required for every future safety assertion."""

    origin: str = "structural"
    rule_id: str = "not_bound"
    evidence_reference: str = "not_bound"
    execution_trace: str = field(default_factory=lambda: f"EXE-{uuid4()}")
    runtime_trace: str = field(default_factory=lambda: f"RTT-{uuid4()}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Constraint:
    """Therapeutic limitation candidate supplied by validated knowledge."""

    constraint_id: str
    category: str = "unclassified"
    severity: str = "informational"
    confidence: float = 0.0
    trace: SafetyTraceReference = field(default_factory=SafetyTraceReference)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Risk:
    """Risk candidate supplied by validated knowledge or structured context."""

    risk_id: str
    category: str = "unclassified"
    severity: str = "informational"
    confidence: float = 0.0
    trace: SafetyTraceReference = field(default_factory=SafetyTraceReference)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Contraindication:
    """Contraindication candidate without embedded clinical rule logic."""

    contraindication_id: str
    kind: str = "conditional"
    severity: str = "informational"
    confidence: float = 0.0
    trace: SafetyTraceReference = field(default_factory=SafetyTraceReference)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Interaction:
    """Interaction candidate without medication-specific logic."""

    interaction_id: str
    severity: str = "informational"
    confidence: float = 0.0
    trace: SafetyTraceReference = field(default_factory=SafetyTraceReference)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Alert:
    """Structured alert generated from safety outputs."""

    alert_id: str
    category: str
    severity: str
    message: str
    priority: str = "informational"
    references: tuple[str, ...] = field(default_factory=tuple)
    trace: SafetyTraceReference = field(default_factory=SafetyTraceReference)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BlockingDecision:
    """Generic execution gate decision, not a clinical recommendation."""

    status: str = "allow"
    reasons: tuple[str, ...] = field(default_factory=tuple)
    explanation: str = "No structural blocking flag was produced."
    trace_id: str = field(default_factory=lambda: f"BLK-{uuid4()}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SafetySnapshot:
    """Compact read-only summary of the safety state."""

    status: str = "not_evaluated"
    alert_count: int = 0
    blocking_count: int = 0
    constraint_count: int = 0
    risk_count: int = 0
    interaction_count: int = 0
    contraindication_count: int = 0
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SafetyResult:
    """Complete structural output of the Safety Engine."""

    status: str
    constraints: tuple[Constraint, ...] = field(default_factory=tuple)
    risks: tuple[Risk, ...] = field(default_factory=tuple)
    contraindications: tuple[Contraindication, ...] = field(default_factory=tuple)
    interactions: tuple[Interaction, ...] = field(default_factory=tuple)
    alerts: tuple[Alert, ...] = field(default_factory=tuple)
    blocking_flags: tuple[str, ...] = field(default_factory=tuple)
    blocking_decision: BlockingDecision = field(default_factory=BlockingDecision)
    confidence: float = 0.0
    trace_id: str = field(default_factory=lambda: f"SFT-{uuid4()}")
    snapshot: SafetySnapshot = field(default_factory=SafetySnapshot)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
