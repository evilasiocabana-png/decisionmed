"""Governed knowledge-object contracts with no executable clinical logic."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
import re


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class KnowledgeError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class KnowledgeObjectType(str, Enum):
    EVIDENCE = "evidence"
    CLINICAL_RULE = "clinical_rule"
    CONTRAINDICATION = "contraindication"
    INTERACTION = "interaction"
    MONITORING_RECOMMENDATION = "monitoring_recommendation"
    OTHER = "other"


class KnowledgeStatus(str, Enum):
    DRAFT = "draft"
    AWAITING_VALIDATION = "awaiting_validation"
    VALIDATED = "validated"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


@dataclass(frozen=True, slots=True)
class EvidenceAnchor:
    """Exact source location supporting a knowledge object."""

    source_id: str
    section: str
    locator: str

    def __post_init__(self) -> None:
        if not isinstance(self.source_id, str) or not _IDENTIFIER.fullmatch(
            self.source_id
        ):
            raise KnowledgeError(
                "evidence_anchor.source_id", "source id must be canonical"
            )
        for field_name, value, maximum in (
            ("section", self.section, 500),
            ("locator", self.locator, 1000),
        ):
            if (
                not isinstance(value, str)
                or not value.strip()
                or len(value) > maximum
            ):
                raise KnowledgeError(
                    f"evidence_anchor.{field_name}",
                    f"{field_name} must contain 1 to {maximum} characters",
                )

    @property
    def runtime_eligible(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class KnowledgeObject:
    """Versioned content record; never an executable rule or runtime output."""

    object_id: str
    official_name: str
    object_type: KnowledgeObjectType
    description: str
    evidence_anchors: tuple[EvidenceAnchor, ...]
    applicability: str
    limits: str
    version: str
    status: KnowledgeStatus = KnowledgeStatus.DRAFT
    reviewed_on: date | None = None
    validated_by: str | None = None

    def __post_init__(self) -> None:
        self._identifier("object_id", self.object_id)
        self._text("official_name", self.official_name)
        if not isinstance(self.object_type, KnowledgeObjectType):
            raise TypeError("object_type must be a KnowledgeObjectType")
        self._text("description", self.description)
        self._text("applicability", self.applicability)
        self._text("limits", self.limits)
        if not isinstance(self.version, str) or not _VERSION.fullmatch(self.version):
            self._fail("version", "version must use semantic versioning")
        if not isinstance(self.status, KnowledgeStatus):
            raise TypeError("status must be a KnowledgeStatus")

        anchors = tuple(self.evidence_anchors)
        if not anchors:
            self._fail("evidence_anchors", "at least one evidence anchor is required")
        if any(not isinstance(anchor, EvidenceAnchor) for anchor in anchors):
            raise TypeError("evidence_anchors must contain EvidenceAnchor values")
        if len(set(anchors)) != len(anchors):
            self._fail("evidence_anchors", "evidence anchors must be unique")
        object.__setattr__(self, "evidence_anchors", anchors)

        if self.reviewed_on is not None and not isinstance(self.reviewed_on, date):
            raise TypeError("reviewed_on must be a date or None")
        if self.validated_by is not None:
            self._identifier("validated_by", self.validated_by)
        if self.status is KnowledgeStatus.VALIDATED and (
            self.reviewed_on is None or self.validated_by is None
        ):
            self._fail(
                "validation",
                "validated knowledge requires review date and validator",
            )

    @classmethod
    def _identifier(cls, field_name: str, value: object) -> None:
        if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
            cls._fail(field_name, f"{field_name} must be canonical")

    @classmethod
    def _text(cls, field_name: str, value: object) -> None:
        if not isinstance(value, str) or not value.strip():
            cls._fail(field_name, f"{field_name} cannot be empty")
        if len(value) > 4000:
            cls._fail(field_name, f"{field_name} is too long")

    @staticmethod
    def _fail(field_name: str, message: str) -> None:
        raise KnowledgeError(f"knowledge_object.{field_name}", message)

    @property
    def runtime_eligible(self) -> bool:
        """Foundation contracts never authorize clinical runtime use."""

        return False

    @property
    def evidence_source_ids(self) -> tuple[str, ...]:
        """Unique source identifiers derived from the precise anchors."""

        return tuple(dict.fromkeys(anchor.source_id for anchor in self.evidence_anchors))
