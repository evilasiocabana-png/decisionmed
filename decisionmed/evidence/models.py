"""Metadata-only scientific source contracts.

The contracts catalog sources. They do not contain clinical claims and cannot
authorize runtime use, recommendations, alerts, or prescribing.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
import re

_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class EvidenceError(ValueError):
    """Base Evidence Layer error with a stable code."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class EvidenceContractError(EvidenceError):
    """Raised when EvidenceSource metadata violates its contract."""


class EvidenceType(str, Enum):
    GUIDELINE = "guideline"
    SYSTEMATIC_REVIEW = "systematic_review"
    META_ANALYSIS = "meta_analysis"
    RANDOMIZED_TRIAL = "randomized_trial"
    OBSERVATIONAL_STUDY = "observational_study"
    CONSENSUS = "consensus"
    REGULATORY_DOCUMENT = "regulatory_document"
    SAFETY_NOTICE = "safety_notice"
    REFERENCE_WORK = "reference_work"
    OTHER = "other"


class EvidenceStatus(str, Enum):
    DRAFT = "draft"
    AWAITING_VALIDATION = "awaiting_validation"
    VALIDATED = "validated"
    DEPRECATED = "deprecated"
    CONFLICTING_EVIDENCE = "conflicting_evidence"


@dataclass(frozen=True, slots=True)
class EvidenceSource:
    """Versioned catalog record for one scientific or regulatory source."""

    source_id: str
    title: str
    publication_year: int
    evidence_type: EvidenceType
    locator: str
    version: str
    status: EvidenceStatus
    specialties: tuple[str, ...]
    reviewed_on: date | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.source_id, str) or not _IDENTIFIER.fullmatch(
            self.source_id
        ):
            self._fail("source_id", "source id must be canonical")
        if not isinstance(self.title, str) or not self.title.strip():
            self._fail("title", "title cannot be empty")
        if len(self.title) > 500:
            self._fail("title", "title is too long")
        if (
            not isinstance(self.publication_year, int)
            or isinstance(self.publication_year, bool)
            or not 1500 <= self.publication_year <= date.today().year + 1
        ):
            self._fail("publication_year", "publication year is invalid")
        if not isinstance(self.evidence_type, EvidenceType):
            raise TypeError("evidence_type must be an EvidenceType")
        if not isinstance(self.locator, str) or not self.locator.strip():
            self._fail("locator", "source locator cannot be empty")
        if len(self.locator) > 1000:
            self._fail("locator", "source locator is too long")
        if not isinstance(self.version, str) or not _VERSION.fullmatch(self.version):
            self._fail("version", "version must use semantic versioning")
        if not isinstance(self.status, EvidenceStatus):
            raise TypeError("status must be an EvidenceStatus")

        specialties = tuple(self.specialties)
        if not specialties:
            self._fail("specialties", "at least one specialty is required")
        if any(
            not isinstance(item, str) or not _IDENTIFIER.fullmatch(item)
            for item in specialties
        ):
            self._fail("specialties", "specialty keys must be canonical")
        if len(set(specialties)) != len(specialties):
            self._fail("specialties", "specialty keys must be unique")
        object.__setattr__(self, "specialties", specialties)

        if self.reviewed_on is not None and not isinstance(self.reviewed_on, date):
            raise TypeError("reviewed_on must be a date or None")
        if self.status is EvidenceStatus.VALIDATED and self.reviewed_on is None:
            self._fail("reviewed_on", "validated metadata requires a review date")

    @staticmethod
    def _fail(field_name: str, message: str) -> None:
        raise EvidenceContractError(f"evidence_source.{field_name}", message)

    @property
    def runtime_eligible(self) -> bool:
        """Source metadata alone never clears a clinical runtime gate."""

        return False
