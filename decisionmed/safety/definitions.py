"""Governed safety-check metadata with no executable clinical rules."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
import re

from .models import SafetyError


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class SafetyCheckStatus(str, Enum):
    DRAFT = "draft"
    AWAITING_VALIDATION = "awaiting_validation"
    VALIDATED = "validated"
    DEPRECATED = "deprecated"


@dataclass(frozen=True, slots=True)
class SafetyCheckSpecification:
    """Versioned check metadata; never a patient-specific evaluation."""

    check_id: str
    specialty_key: str
    purpose: str
    limits: str
    evidence_source_ids: tuple[str, ...]
    version: str
    status: SafetyCheckStatus = SafetyCheckStatus.DRAFT
    reviewed_on: date | None = None
    validated_by: str | None = None
    review_due_on: date | None = None

    def __post_init__(self) -> None:
        _identifier("check_id", self.check_id)
        _identifier("specialty_key", self.specialty_key)
        _text("purpose", self.purpose)
        _text("limits", self.limits)
        source_ids = _identifiers("evidence_source_ids", self.evidence_source_ids)
        object.__setattr__(self, "evidence_source_ids", source_ids)
        if not isinstance(self.version, str) or not _VERSION.fullmatch(self.version):
            _fail("version", "version must use semantic versioning")
        if not isinstance(self.status, SafetyCheckStatus):
            raise TypeError("status must be a SafetyCheckStatus")
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
        if self.status is SafetyCheckStatus.VALIDATED and (
            self.reviewed_on is None
            or self.validated_by is None
            or self.review_due_on is None
            or self.review_due_on <= date.today()
        ):
            _fail(
                "validation",
                "validated specification requires review metadata and a future due date",
            )

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

    @property
    def runtime_eligible(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


def _identifier(field_name: str, value: object) -> None:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        _fail(field_name, f"{field_name} must be canonical")


def _identifiers(field_name: str, values: object) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        _fail(field_name, f"{field_name} must be a collection")
    items = tuple(values)  # type: ignore[arg-type]
    if not items:
        _fail(field_name, f"{field_name} cannot be empty")
    for item in items:
        _identifier(field_name, item)
    if len(set(items)) != len(items):
        _fail(field_name, f"{field_name} must be unique")
    return items


def _text(field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip() or len(value) > 4000:
        _fail(field_name, f"{field_name} must contain 1 to 4000 characters")


def _fail(field_name: str, message: str) -> None:
    raise SafetyError(f"safety_check_specification.{field_name}", message)
