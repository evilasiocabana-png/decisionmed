"""Immutable models for Clinical Intelligence Platform."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ClinicalIntelligenceCapability:
    capability_id: str = field(default_factory=lambda: f"CAP-{uuid4()}")
    name: str = "structural_capability"
    category: str = "assistive"
    owner: str = "Clinical Intelligence Platform"
    version: str = "0.1.0"
    status: str = "registered"
    dependencies: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class IntelligenceContext:
    snapshot: str = ""
    timeline: str = ""
    operating_mind: str = ""
    quality_result: str = ""
    knowledge_version: str = ""
    read_only: bool = True


@dataclass(frozen=True)
class IntelligenceContract:
    capability_id: str
    inputs: tuple[str, ...] = field(default_factory=tuple)
    outputs: tuple[str, ...] = field(default_factory=tuple)
    immutable: bool = True
    trace_required: bool = True
    quality_requirements: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class PermissionPolicy:
    capability_id: str
    requested: tuple[str, ...] = field(default_factory=tuple)
    granted: tuple[str, ...] = field(default_factory=tuple)
    default_access: str = "read_only"


@dataclass(frozen=True)
class GovernanceDecision:
    outcome: str = "hold"
    reason: str = "governance_not_evaluated"
    allowed: bool = False


@dataclass(frozen=True)
class ClinicalIntelligenceResult:
    intelligence_id: str = field(default_factory=lambda: f"CIP-{uuid4()}")
    capability: ClinicalIntelligenceCapability = field(default_factory=ClinicalIntelligenceCapability)
    context: IntelligenceContext = field(default_factory=IntelligenceContext)
    contracts: tuple[IntelligenceContract, ...] = field(default_factory=tuple)
    permissions: tuple[PermissionPolicy, ...] = field(default_factory=tuple)
    outputs: tuple[str, ...] = field(default_factory=tuple)
    explanations: tuple[str, ...] = field(default_factory=tuple)
    quality_validation: str = "not_evaluated"
    governance_decision: GovernanceDecision = field(default_factory=GovernanceDecision)
    audit: tuple[str, ...] = field(default_factory=tuple)
    trace_id: str = field(default_factory=lambda: f"CIP-TRC-{uuid4()}")
    timestamp: str = field(default_factory=_now)
    read_only_mode: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

