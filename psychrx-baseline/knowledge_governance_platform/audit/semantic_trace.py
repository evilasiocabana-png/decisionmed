"""Semantic trace."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class SemanticTrace:
    ontology_version: str
    entity_version: str
    relationship_version: str
    taxonomy_version: str
    scientific_validation_version: str
    knowledge_version: str
    trace_id: str = field(default_factory=lambda: f"KGP-TRACE-{uuid4()}")

