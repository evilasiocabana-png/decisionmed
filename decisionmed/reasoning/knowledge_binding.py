"""Governed Knowledge and Evidence binding for future reasoning inputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from hashlib import sha256
import json
import re

from decisionmed.evidence import EvidenceSource, EvidenceStatus
from decisionmed.knowledge import KnowledgeObject, KnowledgeStatus

from .gate import ReasoningError


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


@dataclass(frozen=True, slots=True)
class ReasoningKnowledgeBinding:
    """Exact validated catalog subset; never executable clinical knowledge."""

    catalog_id: str
    catalog_version: str
    catalog_status: KnowledgeStatus
    catalog_released_on: date
    catalog_validated_by: str
    specialty_key: str
    bound_at: datetime
    knowledge_objects: tuple[KnowledgeObject, ...] = field(repr=False)
    evidence_sources: tuple[EvidenceSource, ...] = field(repr=False)
    content_fingerprint: str = field(init=False)

    def __post_init__(self) -> None:
        for field_name in (
            "catalog_id",
            "catalog_validated_by",
            "specialty_key",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
                _fail(field_name, f"{field_name} must be canonical")
        if (
            not isinstance(self.catalog_version, str)
            or not _VERSION.fullmatch(self.catalog_version)
        ):
            _fail("catalog_version", "catalog version must use semantic versioning")
        if self.catalog_status is not KnowledgeStatus.VALIDATED:
            _fail("catalog_status", "catalog release must be validated")
        if not isinstance(self.catalog_released_on, date):
            raise TypeError("catalog_released_on must be a date")
        if self.catalog_released_on > _today():
            _fail("catalog_released_on", "catalog release cannot be in the future")
        if (
            not isinstance(self.bound_at, datetime)
            or self.bound_at.tzinfo is None
            or self.bound_at.utcoffset() is None
        ):
            raise TypeError("bound_at must be a timezone-aware datetime")
        if self.bound_at > datetime.now(timezone.utc):
            _fail("bound_at", "binding time cannot be in the future")

        objects = tuple(self.knowledge_objects)
        sources = tuple(self.evidence_sources)
        if not objects or not all(isinstance(item, KnowledgeObject) for item in objects):
            _fail("knowledge_objects", "validated knowledge objects are required")
        if not sources or not all(isinstance(item, EvidenceSource) for item in sources):
            _fail("evidence_sources", "validated evidence sources are required")
        objects = tuple(sorted(objects, key=lambda item: item.object_id))
        sources = tuple(sorted(sources, key=lambda item: item.source_id))
        if len({item.object_id for item in objects}) != len(objects):
            _fail("knowledge_objects", "knowledge object ids must be unique")
        if len({item.source_id for item in sources}) != len(sources):
            _fail("evidence_sources", "evidence source ids must be unique")
        if any(
            item.status is not KnowledgeStatus.VALIDATED
            or item.review_due_on is None
            or item.review_due_on <= _today()
            for item in objects
        ):
            _fail("knowledge_status", "knowledge review must be validated and current")
        if any(
            item.status is not EvidenceStatus.VALIDATED
            or item.review_due_on is None
            or item.review_due_on <= _today()
            for item in sources
        ):
            _fail("evidence_status", "evidence review must be validated and current")
        if any(self.specialty_key not in item.specialties for item in sources):
            _fail(
                "evidence_specialty",
                "every evidence source must apply to the binding specialty",
            )

        referenced_source_ids = {
            source_id
            for item in objects
            for source_id in item.evidence_source_ids
        }
        supplied_source_ids = {item.source_id for item in sources}
        if referenced_source_ids != supplied_source_ids:
            _fail(
                "evidence_binding",
                "evidence sources must exactly match knowledge references",
            )

        object.__setattr__(self, "knowledge_objects", objects)
        object.__setattr__(self, "evidence_sources", sources)
        object.__setattr__(self, "content_fingerprint", self._fingerprint())

    @property
    def knowledge_object_ids(self) -> tuple[str, ...]:
        return tuple(item.object_id for item in self.knowledge_objects)

    @property
    def evidence_source_ids(self) -> tuple[str, ...]:
        return tuple(item.source_id for item in self.evidence_sources)

    @property
    def knowledge_binding_complete(self) -> bool:
        return self.review_current

    @property
    def review_current(self) -> bool:
        return (
            self.catalog_status is KnowledgeStatus.VALIDATED
            and all(
                item.status is KnowledgeStatus.VALIDATED
                and item.review_due_on is not None
                and item.review_due_on > _today()
                for item in self.knowledge_objects
            )
            and all(
                item.status is EvidenceStatus.VALIDATED
                and item.review_due_on is not None
                and item.review_due_on > _today()
                for item in self.evidence_sources
            )
        )

    @property
    def engine_invocation_allowed(self) -> bool:
        return False

    @property
    def reasoning_execution_allowed(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False

    def _fingerprint(self) -> str:
        payload = {
            "catalog_id": self.catalog_id,
            "catalog_version": self.catalog_version,
            "catalog_status": self.catalog_status.value,
            "catalog_released_on": self.catalog_released_on.isoformat(),
            "catalog_validated_by": self.catalog_validated_by,
            "specialty_key": self.specialty_key,
            "knowledge_objects": [
                {
                    "object_id": item.object_id,
                    "official_name": item.official_name,
                    "object_type": item.object_type.value,
                    "description": item.description,
                    "evidence_anchors": [
                        {
                            "source_id": anchor.source_id,
                            "section": anchor.section,
                            "locator": anchor.locator,
                        }
                        for anchor in sorted(
                            item.evidence_anchors,
                            key=lambda value: (
                                value.source_id,
                                value.section,
                                value.locator,
                            ),
                        )
                    ],
                    "applicability": item.applicability,
                    "limits": item.limits,
                    "version": item.version,
                    "status": item.status.value,
                    "reviewed_on": item.reviewed_on.isoformat(),
                    "validated_by": item.validated_by,
                    "review_due_on": item.review_due_on.isoformat(),
                }
                for item in self.knowledge_objects
            ],
            "evidence_sources": [
                {
                    "source_id": item.source_id,
                    "title": item.title,
                    "publication_year": item.publication_year,
                    "evidence_type": item.evidence_type.value,
                    "evidence_quality": item.evidence_quality.value,
                    "recommendation_strength": item.recommendation_strength.value,
                    "locator": item.locator,
                    "version": item.version,
                    "status": item.status.value,
                    "specialties": sorted(item.specialties),
                    "reviewed_on": item.reviewed_on.isoformat(),
                    "known_conflicts": item.known_conflicts,
                    "clinical_applicability": item.clinical_applicability,
                    "review_due_on": item.review_due_on.isoformat(),
                }
                for item in self.evidence_sources
            ],
        }
        canonical = json.dumps(
            payload,
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return sha256(canonical).hexdigest()


def _fail(field_name: str, message: str) -> None:
    raise ReasoningError(f"reasoning_knowledge.{field_name}", message)


def _today() -> date:
    return date.today()
