"""Governed, non-executable form-schema contracts for specialty data capture."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
import re

from decisionmed.domain import ClinicalSnapshotSection

from .models import KnowledgeError, KnowledgeStatus


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class ClinicalFieldValueType(str, Enum):
    BOOLEAN = "boolean"
    INTEGER = "integer"
    DECIMAL = "decimal"
    TEXT = "text"
    CODED_CHOICE = "coded_choice"


@dataclass(frozen=True, slots=True)
class ClinicalFieldDefinition:
    """One capture field whose clinical meaning is owned by a KnowledgeObject."""

    field_key: str
    label: str
    section: ClinicalSnapshotSection
    value_type: ClinicalFieldValueType
    knowledge_object_id: str
    required: bool
    allowed_values: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _identifier("field_key", self.field_key)
        _text("label", self.label, 200)
        if not isinstance(self.section, ClinicalSnapshotSection):
            raise TypeError("section must be a ClinicalSnapshotSection")
        if not isinstance(self.value_type, ClinicalFieldValueType):
            raise TypeError("value_type must be a ClinicalFieldValueType")
        _identifier("knowledge_object_id", self.knowledge_object_id)
        if not isinstance(self.required, bool):
            raise TypeError("required must be a bool")

        values = tuple(self.allowed_values)
        if self.value_type is ClinicalFieldValueType.CODED_CHOICE:
            if not values:
                _fail("allowed_values", "coded choice requires allowed values")
            for value in values:
                _identifier("allowed_values", value)
            if len(set(values)) != len(values):
                _fail("allowed_values", "allowed values must be unique")
        elif values:
            _fail("allowed_values", "only coded choice may define allowed values")
        object.__setattr__(self, "allowed_values", values)

    @property
    def runtime_eligible(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class SpecialtyFormSchema:
    """Versioned field collection; never a clinical rule or decision engine."""

    schema_id: str
    specialty_key: str
    workflow_id: str
    step_key: str
    version: str
    fields: tuple[ClinicalFieldDefinition, ...]
    status: KnowledgeStatus = KnowledgeStatus.DRAFT
    reviewed_on: date | None = None
    validated_by: str | None = None
    review_due_on: date | None = None

    def __post_init__(self) -> None:
        _identifier("schema_id", self.schema_id)
        _identifier("specialty_key", self.specialty_key)
        _identifier("workflow_id", self.workflow_id)
        _identifier("step_key", self.step_key)
        if not isinstance(self.version, str) or not _VERSION.fullmatch(self.version):
            _fail("version", "version must use semantic versioning")
        if not isinstance(self.status, KnowledgeStatus):
            raise TypeError("status must be a KnowledgeStatus")

        fields = tuple(self.fields)
        if not fields or not all(
            isinstance(item, ClinicalFieldDefinition) for item in fields
        ):
            _fail("fields", "schema requires clinical field definitions")
        keys = tuple(item.field_key for item in fields)
        if len(set(keys)) != len(keys):
            _fail("fields", "field keys must be unique")
        object.__setattr__(self, "fields", fields)

        if self.reviewed_on is not None and not isinstance(self.reviewed_on, date):
            raise TypeError("reviewed_on must be a date or None")
        if self.reviewed_on is not None and self.reviewed_on > date.today():
            _fail("reviewed_on", "review date cannot be in the future")
        if self.validated_by is not None:
            _identifier("validated_by", self.validated_by)
        if self.review_due_on is not None:
            if not isinstance(self.review_due_on, date):
                raise TypeError("review_due_on must be a date or None")
            if self.reviewed_on is None or self.review_due_on <= self.reviewed_on:
                _fail("review_due_on", "review due date must follow the review date")
        if self.status is KnowledgeStatus.VALIDATED and (
            self.reviewed_on is None
            or self.validated_by is None
            or self.review_due_on is None
            or self.review_due_on <= date.today()
        ):
            _fail(
                "validation",
                "validated schema requires review metadata and a future due date",
            )

    @property
    def runtime_eligible(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False

    @property
    def review_state(self) -> str:
        if self.review_due_on is None:
            return "unscheduled"
        if self.review_due_on < date.today():
            return "overdue"
        if self.review_due_on == date.today():
            return "due_today"
        return "current"

    @property
    def review_overdue(self) -> bool:
        return self.review_state == "overdue"


def _identifier(field_name: str, value: object) -> None:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        _fail(field_name, f"{field_name} must be canonical")


def _text(field_name: str, value: object, maximum: int) -> None:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        _fail(field_name, f"{field_name} must contain 1 to {maximum} characters")


def _fail(field_name: str, message: str) -> None:
    raise KnowledgeError(f"specialty_form_schema.{field_name}", message)
