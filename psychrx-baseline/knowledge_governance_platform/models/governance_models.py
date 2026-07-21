"""Immutable models for Knowledge Governance Platform."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class SemanticVersion:
    major: int = 0
    minor: int = 1
    patch: int = 0
    breaking_change: bool = False
    migration_metadata: tuple[str, ...] = field(default_factory=tuple)

    def value(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass(frozen=True)
class OntologyDefinition:
    ontology_id: str = field(default_factory=lambda: f"ONT-{uuid4()}")
    name: str = "PsychRx Ontology"
    version: SemanticVersion = field(default_factory=SemanticVersion)
    status: str = "draft"
    owner: str = "Knowledge Governance"
    dependencies: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class EntityDefinition:
    entity_id: str
    name: str
    owner: str = "Knowledge Governance"
    aliases: tuple[str, ...] = field(default_factory=tuple)
    status: str = "draft"
    version: SemanticVersion = field(default_factory=SemanticVersion)


@dataclass(frozen=True)
class RelationshipDefinition:
    relationship_id: str
    source: str
    target: str
    relationship_type: str
    direction: str = "directed"
    multiplicity: str = "many_to_many"
    constraints: tuple[str, ...] = field(default_factory=tuple)
    traceability: str = ""


@dataclass(frozen=True)
class TaxonomyDefinition:
    taxonomy_id: str = field(default_factory=lambda: f"TAX-{uuid4()}")
    categories: tuple[str, ...] = field(default_factory=tuple)
    version: SemanticVersion = field(default_factory=SemanticVersion)


@dataclass(frozen=True)
class DependencyGraph:
    nodes: tuple[str, ...] = field(default_factory=tuple)
    edges: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    issues: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class KnowledgeGovernanceResult:
    governance_id: str = field(default_factory=lambda: f"KGP-{uuid4()}")
    ontology_version: str = "0.1.0"
    entity_registry: tuple[EntityDefinition, ...] = field(default_factory=tuple)
    relationship_registry: tuple[RelationshipDefinition, ...] = field(default_factory=tuple)
    taxonomy_version: str = "0.1.0"
    dependency_graph: DependencyGraph = field(default_factory=DependencyGraph)
    semantic_validation: tuple[str, ...] = field(default_factory=tuple)
    version_status: str = "compatible"
    publication_decision: str = "semantic_validation_required"
    audit: tuple[str, ...] = field(default_factory=tuple)
    trace_id: str = field(default_factory=lambda: f"KGP-TRC-{uuid4()}")
    timestamp: str = field(default_factory=_now)
    read_only_mode: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

