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


class EvidenceQuality(str, Enum):
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    VERY_LOW = "very_low"
    INSUFFICIENT = "insufficient"


class RecommendationStrength(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    CONDITIONAL = "conditional"
    INSUFFICIENT_FOR_RECOMMENDATION = "insufficient_for_recommendation"


@dataclass(frozen=True, slots=True)
class EvidenceSource:
    """Versioned catalog record for one scientific or regulatory source."""

    source_id: str
    title: str
    publication_year: int
    evidence_type: EvidenceType
    evidence_quality: EvidenceQuality
    recommendation_strength: RecommendationStrength
    locator: str
    version: str
    status: EvidenceStatus
    specialties: tuple[str, ...]
    reviewed_on: date
    known_conflicts: str
    clinical_applicability: str

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
        if not isinstance(self.evidence_quality, EvidenceQuality):
            raise TypeError("evidence_quality must be an EvidenceQuality")
        if not isinstance(self.recommendation_strength, RecommendationStrength):
            raise TypeError(
                "recommendation_strength must be a RecommendationStrength"
            )
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

        if not isinstance(self.reviewed_on, date):
            raise TypeError("reviewed_on must be a date")
        if self.reviewed_on > date.today():
            self._fail("reviewed_on", "review date cannot be in the future")
        self._text("known_conflicts", self.known_conflicts, 4000)
        self._text("clinical_applicability", self.clinical_applicability, 4000)

    @staticmethod
    def _fail(field_name: str, message: str) -> None:
        raise EvidenceContractError(f"evidence_source.{field_name}", message)

    @classmethod
    def _text(cls, field_name: str, value: object, maximum: int) -> None:
        if not isinstance(value, str) or not value.strip() or len(value) > maximum:
            cls._fail(
                field_name,
                f"{field_name} must contain 1 to {maximum} characters",
            )

    @property
    def runtime_eligible(self) -> bool:
        """Source metadata alone never clears a clinical runtime gate."""

        return False
