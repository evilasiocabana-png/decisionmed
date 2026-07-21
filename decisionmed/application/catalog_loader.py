"""Strict loader for an external, versioned DecisionMEd knowledge catalog."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from hashlib import sha256
import hmac
import json
from pathlib import Path
import re
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
_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
_HASH = re.compile(r"^[0-9a-f]{64}$")
_CATALOG_FILES = ("evidence.json", "knowledge.json", "form-schemas.json")


class CatalogLoadError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True, slots=True)
class GovernedCatalogs:
    manifest: CatalogReleaseManifest
    evidence: EvidenceRegistry
    knowledge: KnowledgeRegistry
    form_schemas: SpecialtyFormSchemaRegistry


@dataclass(frozen=True, slots=True)
class CatalogReleaseManifest:
    catalog_id: str
    release_version: str
    status: KnowledgeStatus
    released_on: date | None
    validated_by: str | None
    file_hashes: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.catalog_id, str) or not _IDENTIFIER.fullmatch(self.catalog_id):
            raise CatalogLoadError("catalog.manifest_id", "catalog id must be canonical")
        if not isinstance(self.release_version, str) or not _VERSION.fullmatch(self.release_version):
            raise CatalogLoadError("catalog.manifest_version", "release version is invalid")
        if not isinstance(self.status, KnowledgeStatus):
            raise TypeError("status must be a KnowledgeStatus")
        hashes = tuple(self.file_hashes)
        if tuple(name for name, _ in hashes) != _CATALOG_FILES or any(
            not isinstance(value, str) or not _HASH.fullmatch(value)
            for _, value in hashes
        ):
            raise CatalogLoadError("catalog.manifest_hashes", "manifest hashes are invalid")
        object.__setattr__(self, "file_hashes", hashes)
        if self.released_on is not None and not isinstance(self.released_on, date):
            raise TypeError("released_on must be a date or None")
        if self.validated_by is not None and (
            not isinstance(self.validated_by, str)
            or not _IDENTIFIER.fullmatch(self.validated_by)
        ):
            raise CatalogLoadError("catalog.manifest_validator", "validator is invalid")
        if self.status is KnowledgeStatus.VALIDATED and (
            self.released_on is None or self.validated_by is None
        ):
            raise CatalogLoadError(
                "catalog.manifest_validation",
                "validated release requires review metadata",
            )

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


def load_governed_catalogs(root: Path) -> GovernedCatalogs:
    """Load three fixed files from an external catalog directory, fail closed."""

    root = root.resolve()
    if not root.is_dir():
        raise CatalogLoadError("catalog.root", "catalog root is not a directory")
    try:
        manifest = _load_manifest(root / "catalog-manifest.json")
        hashes = dict(manifest.file_hashes)
        evidence_payload = _load_file(root / "evidence.json", hashes["evidence.json"])
        knowledge_payload = _load_file(root / "knowledge.json", hashes["knowledge.json"])
        schema_payload = _load_file(
            root / "form-schemas.json", hashes["form-schemas.json"]
        )

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
    return GovernedCatalogs(manifest, evidence, knowledge, schemas)


def _load_manifest(path: Path) -> CatalogReleaseManifest:
    payload = _decode_json(_read_file(path), path.name)
    expected = {
        "schema_version", "catalog_id", "release_version", "status",
        "released_on", "validated_by", "files",
    }
    if not isinstance(payload, dict) or set(payload) != expected:
        raise CatalogLoadError("catalog.manifest", "invalid catalog manifest")
    if payload["schema_version"] != CATALOG_SCHEMA_VERSION:
        raise CatalogLoadError("catalog.version", "unsupported manifest version")
    files = payload["files"]
    if not isinstance(files, dict) or set(files) != set(_CATALOG_FILES):
        raise CatalogLoadError("catalog.manifest_hashes", "manifest hashes are invalid")
    return CatalogReleaseManifest(
        catalog_id=payload["catalog_id"],
        release_version=payload["release_version"],
        status=KnowledgeStatus(payload["status"]),
        released_on=_date_or_none(payload["released_on"]),
        validated_by=payload["validated_by"],
        file_hashes=tuple((name, files[name]) for name in _CATALOG_FILES),
    )


def _load_file(path: Path, expected_hash: str) -> dict[str, Any]:
    data = _read_file(path)
    actual_hash = sha256(data).hexdigest()
    if not hmac.compare_digest(actual_hash, expected_hash):
        raise CatalogLoadError("catalog.integrity", f"catalog hash mismatch: {path.name}")
    payload = _decode_json(data, path.name)
    if not isinstance(payload, dict) or set(payload) != {"schema_version", "items"}:
        raise CatalogLoadError("catalog.envelope", f"invalid catalog envelope: {path.name}")
    if payload["schema_version"] != CATALOG_SCHEMA_VERSION:
        raise CatalogLoadError("catalog.version", f"unsupported catalog version: {path.name}")
    return payload


def _read_file(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise CatalogLoadError("catalog.file", f"required catalog file unavailable: {path.name}")
    if path.stat().st_size > MAX_CATALOG_BYTES:
        raise CatalogLoadError("catalog.size", f"catalog file too large: {path.name}")
    try:
        return path.read_bytes()
    except OSError as exc:
        raise CatalogLoadError("catalog.file", f"catalog file unreadable: {path.name}") from exc


def _decode_json(data: bytes, filename: str) -> Any:
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=_object)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise CatalogLoadError("catalog.json", f"invalid catalog JSON: {filename}") from exc


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
