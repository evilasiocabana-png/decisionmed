"""Typed Evidence Runtime models with no scientific interpretation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

EVIDENCE_HIERARCHY = (
    "guideline",
    "systematic_review",
    "meta_analysis",
    "randomized_controlled_trial",
    "observational",
    "consensus",
    "textbook",
)


@dataclass(frozen=True)
class EvidenceMetadata:
    """Bibliographic and lifecycle metadata for evidence records."""

    title: str = ""
    authors: tuple[str, ...] = field(default_factory=tuple)
    year: int | None = None
    guideline: str = ""
    journal: str = ""
    organization: str = ""
    version: str = "0.1-draft"
    language: str = ""
    publication_date: str = ""
    status: str = "draft"
    category: str = "unclassified"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceSource:
    """Source description for evidence records."""

    source_id: str
    source_type: str = "unclassified"
    uri: str = ""
    version: str = "0.1-draft"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceReference:
    """Traceable reference to a source and version."""

    reference_id: str
    source_id: str
    version: str = "0.1-draft"
    trace_id: str = field(default_factory=lambda: f"EVR-{uuid4()}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Evidence:
    """Evidence record supplied by validated knowledge structures."""

    evidence_id: str
    evidence_type: str
    metadata: EvidenceMetadata = field(default_factory=EvidenceMetadata)
    source: EvidenceSource | None = None
    references: tuple[EvidenceReference, ...] = field(default_factory=tuple)
    scope: str = "general"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceRequest:
    """Runtime request for evidence without clinical interpretation."""

    query: str = ""
    category: str = ""
    scope: str = ""
    version: str = "latest"
    status: str = "validated"
    trace_id: str = field(default_factory=lambda: f"EVQ-{uuid4()}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Citation:
    """Structured citation, not a formatted bibliography."""

    citation_id: str
    evidence_id: str
    source_id: str = ""
    version: str = ""
    source_link: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceSnapshot:
    """Compact summary of evidence selected for runtime use."""

    selected_count: int = 0
    discarded_count: int = 0
    citation_count: int = 0
    version_policy: str = "latest"
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    trace_id: str = field(default_factory=lambda: f"EVS-{uuid4()}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceResult:
    """Complete structural result from Evidence Runtime."""

    status: str
    query: EvidenceRequest = field(default_factory=EvidenceRequest)
    selected_evidence: tuple[Evidence, ...] = field(default_factory=tuple)
    discarded_evidence: tuple[Evidence, ...] = field(default_factory=tuple)
    ranking: tuple[str, ...] = field(default_factory=tuple)
    sources: tuple[EvidenceSource, ...] = field(default_factory=tuple)
    citations: tuple[Citation, ...] = field(default_factory=tuple)
    snapshot: EvidenceSnapshot = field(default_factory=EvidenceSnapshot)
    confidence: float = 0.0
    trace_id: str = field(default_factory=lambda: f"EVR-{uuid4()}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
