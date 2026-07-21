"""Strict loader for an external, versioned DecisionMEd knowledge catalog."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path
from typing import Any

from decisionmed.domain import ClinicalSnapshotSection
from decisionmed.evidence import (
    EvidenceRegistry,
    EvidenceSource,
    EvidenceStatus,
    EvidenceType,
)
from decisionmed.knowledge import (
    ClinicalFieldDefinition,
    ClinicalFieldValueType,
    KnowledgeObject,
    KnowledgeObjectType,
    KnowledgeRegistry,
    KnowledgeStatus,
    SpecialtyFormSchema,
    SpecialtyFormSchemaRegistry,
)


CATALOG_SCHEMA_VERSION = "1.0.0"
MAX_CATALOG_BYTES = 1_048_576
MAX_CATALOG_ITEMS = 10_000


class CatalogLoadError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True, slots=True)
class GovernedCatalogs:
    evidence: EvidenceRegistry
    knowledge: KnowledgeRegistry
    form_schemas: SpecialtyFormSchemaRegistry


def load_governed_catalogs(root: Path) -> GovernedCatalogs:
    """Load three fixed files from an external catalog directory, fail closed."""

    root = root.resolve()
    if not root.is_dir():
        raise CatalogLoadError("catalog.root", "catalog root is not a directory")
    try:
        evidence_payload = _load_file(root / "evidence.json")
        knowledge_payload = _load_file(root / "knowledge.json")
        schema_payload = _load_file(root / "form-schemas.json")

        evidence = EvidenceRegistry(
            EvidenceSource(
                source_id=item["source_id"],
                title=item["title"],
                publication_year=item["publication_year"],
                evidence_type=EvidenceType(item["evidence_type"]),
                locator=item["locator"],
                version=item["version"],
                status=EvidenceStatus(item["status"]),
                specialties=_list(item, "specialties"),
                reviewed_on=_date_or_none(item["reviewed_on"]),
            )
            for item in _items(evidence_payload, "evidence.json", _EVIDENCE_KEYS)
        )
        knowledge = KnowledgeRegistry(
            evidence,
            (
                KnowledgeObject(
                    object_id=item["object_id"],
                    official_name=item["official_name"],
                    object_type=KnowledgeObjectType(item["object_type"]),
                    description=item["description"],
                    evidence_source_ids=_list(item, "evidence_source_ids"),
                    applicability=item["applicability"],
                    limits=item["limits"],
                    version=item["version"],
                    status=KnowledgeStatus(item["status"]),
                    reviewed_on=_date_or_none(item["reviewed_on"]),
                    validated_by=item["validated_by"],
                )
                for item in _items(
                    knowledge_payload, "knowledge.json", _KNOWLEDGE_KEYS
                )
            ),
        )
        schemas = SpecialtyFormSchemaRegistry(
            knowledge,
            (
                _form_schema(item)
                for item in _items(
                    schema_payload, "form-schemas.json", _SCHEMA_KEYS
                )
            ),
        )
    except CatalogLoadError:
        raise
    except (KeyError, TypeError, ValueError) as exc:
        raise CatalogLoadError(
            "catalog.invalid_content", "catalog content violates its contracts"
        ) from exc
    return GovernedCatalogs(evidence, knowledge, schemas)


def _load_file(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise CatalogLoadError("catalog.file", f"required catalog file unavailable: {path.name}")
    if path.stat().st_size > MAX_CATALOG_BYTES:
        raise CatalogLoadError("catalog.size", f"catalog file too large: {path.name}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_object)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CatalogLoadError("catalog.json", f"invalid catalog JSON: {path.name}") from exc
    if not isinstance(payload, dict) or set(payload) != {"schema_version", "items"}:
        raise CatalogLoadError("catalog.envelope", f"invalid catalog envelope: {path.name}")
    if payload["schema_version"] != CATALOG_SCHEMA_VERSION:
        raise CatalogLoadError("catalog.version", f"unsupported catalog version: {path.name}")
    return payload


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CatalogLoadError("catalog.duplicate_key", "duplicate JSON key")
        result[key] = value
    return result


def _items(
    payload: dict[str, Any], filename: str, expected_keys: frozenset[str]
) -> tuple[dict[str, Any], ...]:
    values = payload["items"]
    if not isinstance(values, list) or len(values) > MAX_CATALOG_ITEMS:
        raise CatalogLoadError("catalog.items", f"invalid item collection: {filename}")
    if any(not isinstance(item, dict) or set(item) != expected_keys for item in values):
        raise CatalogLoadError("catalog.fields", f"invalid item fields: {filename}")
    return tuple(values)


def _form_schema(item: dict[str, Any]) -> SpecialtyFormSchema:
    raw_fields = item["fields"]
    if not isinstance(raw_fields, list) or not raw_fields:
        raise CatalogLoadError("catalog.schema_fields", "form schema fields are invalid")
    if any(not isinstance(field, dict) or set(field) != _FIELD_KEYS for field in raw_fields):
        raise CatalogLoadError("catalog.schema_fields", "form schema fields are invalid")
    return SpecialtyFormSchema(
        schema_id=item["schema_id"],
        specialty_key=item["specialty_key"],
        version=item["version"],
        fields=tuple(
            ClinicalFieldDefinition(
                field_key=field["field_key"],
                label=field["label"],
                section=ClinicalSnapshotSection(field["section"]),
                value_type=ClinicalFieldValueType(field["value_type"]),
                knowledge_object_id=field["knowledge_object_id"],
                required=field["required"],
                allowed_values=_list(field, "allowed_values"),
            )
            for field in raw_fields
        ),
        status=KnowledgeStatus(item["status"]),
        reviewed_on=_date_or_none(item["reviewed_on"]),
        validated_by=item["validated_by"],
    )


def _date_or_none(value: object) -> date | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise CatalogLoadError("catalog.date", "review date must be ISO text or null")
    return date.fromisoformat(value)


def _list(item: dict[str, Any], key: str) -> tuple[Any, ...]:
    value = item[key]
    if not isinstance(value, list):
        raise CatalogLoadError("catalog.collection", f"{key} must be a JSON array")
    return tuple(value)


_EVIDENCE_KEYS = frozenset(
    {"source_id", "title", "publication_year", "evidence_type", "locator", "version", "status", "specialties", "reviewed_on"}
)
_KNOWLEDGE_KEYS = frozenset(
    {"object_id", "official_name", "object_type", "description", "evidence_source_ids", "applicability", "limits", "version", "status", "reviewed_on", "validated_by"}
)
_SCHEMA_KEYS = frozenset(
    {"schema_id", "specialty_key", "version", "status", "reviewed_on", "validated_by", "fields"}
)
_FIELD_KEYS = frozenset(
    {"field_key", "label", "section", "value_type", "knowledge_object_id", "required", "allowed_values"}
)
