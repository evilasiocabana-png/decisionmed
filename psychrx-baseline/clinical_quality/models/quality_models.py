"""Immutable quality assurance models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class QualityDimension:
    name: str
    status: str = "not_evaluated"
    score: float = 0.0
    details: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class QualityWarning:
    code: str
    message: str
    severity: str = "warning"


@dataclass(frozen=True)
class BlockingIssue:
    code: str
    message: str
    source: str


@dataclass(frozen=True)
class PublicationDecision:
    outcome: str = "hold_publication"
    explainable_reason: str = "quality_not_evaluated"
    publish_allowed: bool = False


@dataclass(frozen=True)
class QualityMetrics:
    completeness: float = 0.0
    consistency: float = 0.0
    traceability: float = 0.0
    explainability: float = 0.0

    def average(self) -> float:
        return round(
            (self.completeness + self.consistency + self.traceability + self.explainability) / 4,
            3,
        )


@dataclass(frozen=True)
class QualitySummary:
    blocking_issues: tuple[BlockingIssue, ...] = field(default_factory=tuple)
    warnings: tuple[QualityWarning, ...] = field(default_factory=tuple)
    metrics: QualityMetrics = field(default_factory=QualityMetrics)
    publication_decision: PublicationDecision = field(default_factory=PublicationDecision)


@dataclass(frozen=True)
class ClinicalQualityResult:
    quality_id: str = field(default_factory=lambda: f"CQ-{uuid4()}")
    status: str = "not_evaluated"
    quality_score: float = 0.0
    completeness: QualityDimension = field(default_factory=lambda: QualityDimension("completeness"))
    consistency: QualityDimension = field(default_factory=lambda: QualityDimension("consistency"))
    traceability: QualityDimension = field(default_factory=lambda: QualityDimension("traceability"))
    explainability: QualityDimension = field(default_factory=lambda: QualityDimension("explainability"))
    missing_data: tuple[str, ...] = field(default_factory=tuple)
    conflicts: tuple[str, ...] = field(default_factory=tuple)
    blocking_issues: tuple[BlockingIssue, ...] = field(default_factory=tuple)
    warnings: tuple[QualityWarning, ...] = field(default_factory=tuple)
    publication_decision: PublicationDecision = field(default_factory=PublicationDecision)
    trace_id: str = field(default_factory=lambda: f"CQ-TRC-{uuid4()}")
    timestamp: str = field(default_factory=_utc_now)
    read_only_mode: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

