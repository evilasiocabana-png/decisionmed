"""Immutable models for Scientific Validation Framework."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ScientificSource:
    source_id: str = field(default_factory=lambda: f"SRC-{uuid4()}")
    source_type: str = "candidate"
    title: str = ""
    authors: tuple[str, ...] = field(default_factory=tuple)
    organization: str = ""
    publication_year: int = 0
    revision_date: str = ""
    doi: str = ""
    pmid: str = ""
    isbn: str = ""
    language: str = ""
    country: str = ""
    lifecycle_state: str = "candidate"


@dataclass(frozen=True)
class ScientificEvidence:
    evidence_id: str = field(default_factory=lambda: f"EVD-SCI-{uuid4()}")
    study_design: str = "not_classified"
    methodological_quality: str = "not_evaluated"
    risk_of_bias: str = "not_evaluated"
    external_validity: str = "not_evaluated"
    recommendation_strength: str = "not_assigned"
    references: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class GuidelineReference:
    guideline_id: str = field(default_factory=lambda: f"GL-{uuid4()}")
    organization: str = ""
    edition: str = ""
    version: str = ""
    publication: str = ""
    replacement_history: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class QualityAssessment:
    status: str = "pending"
    quality_level: str = "not_evaluated"
    hierarchy_rank: int = 0
    limitations: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class EditorialDecision:
    state: str = "pending"
    reviewers: tuple[str, ...] = field(default_factory=tuple)
    rationale: str = "awaiting_review"


@dataclass(frozen=True)
class PublicationDecision:
    outcome: str = "hold"
    knowledge_version: str = ""
    reason: str = "validation_incomplete"
    publish_allowed: bool = False


@dataclass(frozen=True)
class ScientificValidationResult:
    validation_id: str = field(default_factory=lambda: f"SVF-{uuid4()}")
    knowledge_candidate: str = ""
    scientific_sources: tuple[ScientificSource, ...] = field(default_factory=tuple)
    quality_assessment: QualityAssessment = field(default_factory=QualityAssessment)
    guideline_assessment: tuple[GuidelineReference, ...] = field(default_factory=tuple)
    conflicts: tuple[str, ...] = field(default_factory=tuple)
    editorial_review: EditorialDecision = field(default_factory=EditorialDecision)
    publication_decision: PublicationDecision = field(default_factory=PublicationDecision)
    knowledge_version: str = ""
    audit: tuple[str, ...] = field(default_factory=tuple)
    trace_id: str = field(default_factory=lambda: f"SVF-TRC-{uuid4()}")
    timestamp: str = field(default_factory=_now)
    read_only_mode: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

