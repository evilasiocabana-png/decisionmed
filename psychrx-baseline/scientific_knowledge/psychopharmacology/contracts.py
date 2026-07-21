"""Metadata contracts for psychopharmacology library packages."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
from uuid import uuid4

from scientific_knowledge.models import EditorialReview, KnowledgeVersion, Traceability


@dataclass(frozen=True)
class DrugMetadata:
    identifier: str
    generic_name: str
    atc_code: str = ""
    semantic_id: str = ""
    knowledge_id: str = ""
    editorial_owner: str = "Psychopharmacology Editorial Board"
    review_status: str = "registered"
    publication_status: str = "not_populated"
    validation_status: str = "not_validated"
    read_only_mode: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DrugTemplate:
    metadata: DrugMetadata
    sections: tuple[str, ...] = (
        "identity",
        "classification",
        "mechanism",
        "receptors",
        "indications",
        "contraindications",
        "interactions",
        "adverse_effects",
        "monitoring",
        "evidence",
        "guidelines",
        "ontology_links",
        "editorial_review",
        "traceability",
    )
    populated_sections: tuple[str, ...] = field(default_factory=tuple)
    allows_scientific_content: bool = False
    allows_therapeutic_rule: bool = False
    allows_prescription: bool = False

    def missing_sections(self) -> tuple[str, ...]:
        return tuple(section for section in self.sections if section not in self.populated_sections)


@dataclass(frozen=True)
class DrugPackageContract:
    package_id: str = field(default_factory=lambda: f"DRUG-PKG-{uuid4()}")
    package_name: str = ""
    drug_metadata: tuple[DrugMetadata, ...] = field(default_factory=tuple)
    scientific_references: tuple[str, ...] = field(default_factory=tuple)
    knowledge_version: KnowledgeVersion = field(default_factory=KnowledgeVersion)
    editorial_review: EditorialReview = field(default_factory=EditorialReview)
    ontology_mapping: tuple[str, ...] = field(default_factory=tuple)
    validation_status: str = "not_validated"
    publication_status: str = "not_populated"
    traceability: Traceability = field(default_factory=Traceability)
    read_only_mode: bool = True

