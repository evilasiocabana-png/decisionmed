"""Typed immutable Clinical Snapshot models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class SnapshotVersion:
    major: int = 0
    minor: int = 1
    patch: int = 0
    lineage_id: str = field(default_factory=lambda: f"LIN-{uuid4()}")

    def label(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass(frozen=True)
class SnapshotMetadata:
    creation_time: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    runtime_version: str = "structural"
    knowledge_version: str = "not_bound"
    evidence_version: str = "not_bound"
    workspace_version: str = "0.1-structural"
    builder_version: str = "0.1-structural"


@dataclass(frozen=True)
class SnapshotReference:
    runtime_trace: str = "not_bound"
    safety_trace: str = "not_bound"
    evidence_trace: str = "not_bound"
    optimization_trace: str = "not_bound"
    explanation_trace: str = "not_bound"
    knowledge_version: str = "not_bound"


@dataclass(frozen=True)
class SnapshotConfidence:
    value: float = 0.0
    explanation: str = "Structural confidence only."


@dataclass(frozen=True)
class SnapshotStatistics:
    safety_alerts: int = 0
    evidence_items: int = 0
    hypotheses: int = 0
    explanations: int = 0
    uncertainties: int = 0


@dataclass(frozen=True)
class SnapshotSummary:
    main_findings: tuple[str, ...] = field(default_factory=tuple)
    major_changes: tuple[str, ...] = field(default_factory=tuple)
    active_alerts: tuple[str, ...] = field(default_factory=tuple)
    confidence_summary: str = "No clinical interpretation."


@dataclass(frozen=True)
class ClinicalSnapshot:
    snapshot_id: str = field(default_factory=lambda: f"SNP-{uuid4()}")
    runtime_id: str = "not_bound"
    patient_context: dict[str, Any] = field(default_factory=dict)
    clinical_context: dict[str, Any] = field(default_factory=dict)
    goals: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    constraints: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    safety: dict[str, Any] = field(default_factory=dict)
    evidence: dict[str, Any] = field(default_factory=dict)
    hypotheses: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    explanations: dict[str, Any] = field(default_factory=dict)
    confidence: SnapshotConfidence = field(default_factory=SnapshotConfidence)
    uncertainties: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    metadata: SnapshotMetadata = field(default_factory=SnapshotMetadata)
    version: SnapshotVersion = field(default_factory=SnapshotVersion)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    trace_id: str = field(default_factory=lambda: f"SNP-TRC-{uuid4()}")
    references: SnapshotReference = field(default_factory=SnapshotReference)
    statistics: SnapshotStatistics = field(default_factory=SnapshotStatistics)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
