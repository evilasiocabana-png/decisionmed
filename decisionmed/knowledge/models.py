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
class KnowledgeObject:
    """Versioned content record; never an executable rule or runtime output."""

    object_id: str
    official_name: str
    object_type: KnowledgeObjectType
    description: str
    evidence_source_ids: tuple[str, ...]
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

        source_ids = tuple(self.evidence_source_ids)
        if not source_ids:
            self._fail("evidence_source_ids", "at least one source is required")
        for source_id in source_ids:
            self._identifier("evidence_source_ids", source_id)
        if len(set(source_ids)) != len(source_ids):
            self._fail("evidence_source_ids", "source ids must be unique")
        object.__setattr__(self, "evidence_source_ids", source_ids)

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
