"""Application port for externally verified safety-review authority."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import re
from typing import Protocol, runtime_checkable


SAFETY_REVIEW_ACTION = "safety_review.attest"

_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_FINGERPRINT = re.compile(r"^[0-9a-f]{64}$")


class SafetyReviewerAuthorityStatus(str, Enum):
    AUTHORIZED = "authorized"
    DENIED = "denied"


@dataclass(frozen=True, slots=True)
class SafetyReviewerAuthorityDecision:
    """Metadata-only result returned by an external authority provider."""

    reviewer_id: str
    authority_reference: str
    authority_provider: str
    action: str
    assessment_trace_id: str
    assessment_fingerprint: str
    status: SafetyReviewerAuthorityStatus
    decision_reference: str
    verified_at: datetime

    def __post_init__(self) -> None:
        for field_name in (
            "reviewer_id",
            "authority_reference",
            "authority_provider",
            "decision_reference",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
                raise ValueError(f"{field_name} must be canonical")
        if self.action != SAFETY_REVIEW_ACTION:
            raise ValueError("action must identify the safety-review attestation")
        if (
            not isinstance(self.assessment_trace_id, str)
            or not self.assessment_trace_id.strip()
        ):
            raise ValueError("assessment_trace_id cannot be empty")
        if (
            not isinstance(self.assessment_fingerprint, str)
            or not _FINGERPRINT.fullmatch(self.assessment_fingerprint)
        ):
            raise ValueError("assessment_fingerprint must be SHA-256")
        if not isinstance(self.status, SafetyReviewerAuthorityStatus):
            raise TypeError("status must be a SafetyReviewerAuthorityStatus")
        if (
            not isinstance(self.verified_at, datetime)
            or self.verified_at.tzinfo is None
            or self.verified_at.utcoffset() is None
        ):
            raise TypeError("verified_at must be a timezone-aware datetime")
        if self.verified_at > datetime.now(timezone.utc):
            raise ValueError("verified_at cannot be in the future")

    def matches_request(
        self,
        *,
        reviewer_id: str,
        authority_reference: str,
        assessment_trace_id: str,
        assessment_fingerprint: str,
    ) -> bool:
        return (
            self.reviewer_id == reviewer_id
            and self.authority_reference == authority_reference
            and self.action == SAFETY_REVIEW_ACTION
            and self.assessment_trace_id == assessment_trace_id
            and self.assessment_fingerprint == assessment_fingerprint
        )

    @property
    def review_recording_allowed(self) -> bool:
        return self.status is SafetyReviewerAuthorityStatus.AUTHORIZED

    @property
    def reasoning_execution_allowed(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


@runtime_checkable
class SafetyReviewerAuthority(Protocol):
    """Port implemented by a future identity and authorization adapter."""

    @property
    def provider(self) -> str: ...

    def verify(
        self,
        *,
        reviewer_id: str,
        authority_reference: str,
        assessment_trace_id: str,
        assessment_fingerprint: str,
    ) -> SafetyReviewerAuthorityDecision: ...
