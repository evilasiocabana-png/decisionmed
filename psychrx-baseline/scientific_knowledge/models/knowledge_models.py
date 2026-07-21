"""Immutable metadata contracts for the Official Scientific Knowledge Base."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class KnowledgeVersion:
    semantic_version: str = "0.1.0"
    scientific_version: str = "draft-0"
    lifecycle_state: str = "draft"
    compatibility: str = "pending_validation"


@dataclass(frozen=True)
class Traceability:
    trace_id: str = field(default_factory=lambda: f"OSKB-TRC-{uuid4()}")
    source_references: tuple[str, ...] = field(default_factory=tuple)
    evidence_level: str = "not_assigned"
    evidence_quality: str = "not_evaluated"
    reviewed_at: str = ""


@dataclass(frozen=True)
class EditorialReview:
    editorial_status: str = "draft"
    reviewer_ids: tuple[str, ...] = field(default_factory=tuple)
    comments: tuple[str, ...] = field(default_factory=tuple)
    decision: str = "not_reviewed"


@dataclass(frozen=True)
class ScientificEntityContract:
    identifier: str
    entity_type: str
    semantic_id: str
    scientific_id: str
    knowledge_version: KnowledgeVersion = field(default_factory=KnowledgeVersion)
    traceability: Traceability = field(default_factory=Traceability)
    editorial_review: EditorialReview = field(default_factory=EditorialReview)
    ontology_links: tuple[str, ...] = field(default_factory=tuple)
    created_at: str = field(default_factory=_now)
    read_only_mode: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ScientificKnowledgeSchema:
    schema_id: str = "OSKB-SCHEMA-0.1"
    supported_entities: tuple[str, ...] = (
        "Drug",
        "Mechanism",
        "Receptor",
        "Diagnosis",
        "Syndrome",
        "Symptom",
        "TherapeuticGoal",
        "Constraint",
        "Interaction",
        "Contraindication",
        "Monitoring",
        "Evidence",
        "Guideline",
        "Reference",
    )
    required_contract_fields: tuple[str, ...] = (
        "identifier",
        "semantic_id",
        "scientific_id",
        "knowledge_version",
        "source_references",
        "evidence_level",
        "editorial_status",
        "trace_id",
    )
    requires_scientific_validation: bool = True
    requires_knowledge_governance: bool = True
    read_only_mode: bool = True


@dataclass(frozen=True)
class DrugKnowledgeSchema:
    contract: ScientificEntityContract
    mechanism_ids: tuple[str, ...] = field(default_factory=tuple)
    receptor_ids: tuple[str, ...] = field(default_factory=tuple)
    indication_ids: tuple[str, ...] = field(default_factory=tuple)
    contraindication_ids: tuple[str, ...] = field(default_factory=tuple)
    interaction_ids: tuple[str, ...] = field(default_factory=tuple)
    adverse_effect_ids: tuple[str, ...] = field(default_factory=tuple)
    monitoring_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class GuidelineKnowledgeSchema:
    contract: ScientificEntityContract
    organization: str = ""
    publication_year: int = 0
    recommendation_ids: tuple[str, ...] = field(default_factory=tuple)
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    conflict_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class KnowledgePackage:
    package_id: str
    package_type: str
    version: KnowledgeVersion = field(default_factory=KnowledgeVersion)
    entities: tuple[ScientificEntityContract, ...] = field(default_factory=tuple)
    dependencies: tuple[str, ...] = field(default_factory=tuple)
    owner: str = "Scientific Knowledge Governance"
    publication_status: str = "draft"
    read_only_mode: bool = True


@dataclass(frozen=True)
class KnowledgePackageRegistryEntry:
    package_id: str
    package_type: str
    status: str = "draft"
    version: str = "0.1.0"
    owner: str = "Scientific Knowledge Governance"
    dependencies: tuple[str, ...] = field(default_factory=tuple)
    approval: str = "not_approved"


@dataclass(frozen=True)
class ReviewerRecord:
    reviewer_id: str
    role: str = "scientific_reviewer"
    review_history: tuple[str, ...] = field(default_factory=tuple)
    comments: tuple[str, ...] = field(default_factory=tuple)
    decision: str = "not_assigned"


@dataclass(frozen=True)
class ConflictEntry:
    conflict_id: str = field(default_factory=lambda: f"CNF-{uuid4()}")
    source_a: str = ""
    source_b: str = ""
    topic: str = ""
    status: str = "registered_unresolved"
    resolution: str = "not_resolved"


@dataclass(frozen=True)
class PublicationGateResult:
    package_id: str
    scientific_validation_approved: bool = False
    knowledge_governance_approved: bool = False
    editorial_approved: bool = False
    version_assigned: bool = False
    publish_allowed: bool = False
    reason: str = "publication_requirements_incomplete"

