"""Human safety-review attestations bound to exact assessment content."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import json
import re

from .models import SafetyAssessment, SafetyError, SafetyGateStatus


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_FINGERPRINT = re.compile(r"^[0-9a-f]{64}$")


class SafetyReviewDisposition(str, Enum):
    VALIDATED_FOR_REASONING_REVIEW = "validated_for_reasoning_review"
    REASSESSMENT_REQUIRED = "reassessment_required"


@dataclass(frozen=True, slots=True)
class SafetyReviewRecord:
    """Metadata-only attestation; authentication remains an Application concern."""

    assessment_trace_id: str
    assessment_fingerprint: str
    assessment_status: SafetyGateStatus
    reviewer_id: str
    authority_reference: str
    reviewed_at: datetime
    disposition: SafetyReviewDisposition
    rationale: str

    def __post_init__(self) -> None:
        if not isinstance(self.assessment_trace_id, str) or not self.assessment_trace_id.strip():
            _fail("trace_id", "assessment trace id cannot be empty")
        if not isinstance(self.assessment_fingerprint, str) or not _FINGERPRINT.fullmatch(
            self.assessment_fingerprint
        ):
            _fail("fingerprint", "assessment fingerprint must be SHA-256")
        if not isinstance(self.assessment_status, SafetyGateStatus):
            raise TypeError("assessment_status must be a SafetyGateStatus")
        for field_name in ("reviewer_id", "authority_reference"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
                _fail(field_name, f"{field_name} must be canonical")
        if (
            not isinstance(self.reviewed_at, datetime)
            or self.reviewed_at.tzinfo is None
            or self.reviewed_at.utcoffset() is None
        ):
            raise TypeError("reviewed_at must be a timezone-aware datetime")
        if self.reviewed_at > datetime.now(timezone.utc):
            _fail("reviewed_at", "review time cannot be in the future")
        if not isinstance(self.disposition, SafetyReviewDisposition):
            raise TypeError("disposition must be a SafetyReviewDisposition")
        if not isinstance(self.rationale, str) or not self.rationale.strip() or len(self.rationale) > 4000:
            _fail("rationale", "rationale must contain 1 to 4000 characters")
        if (
            self.disposition
            is SafetyReviewDisposition.VALIDATED_FOR_REASONING_REVIEW
            and self.assessment_status is not SafetyGateStatus.READY_FOR_HUMAN_REVIEW
        ):
            _fail(
                "disposition",
                "only an assessment ready for human review can be validated",
            )

    @classmethod
    def create(
        cls,
        assessment: SafetyAssessment,
        *,
        reviewer_id: str,
        authority_reference: str,
        reviewed_at: datetime,
        disposition: SafetyReviewDisposition,
        rationale: str,
    ) -> SafetyReviewRecord:
        if not isinstance(assessment, SafetyAssessment):
            raise TypeError("assessment must be a SafetyAssessment")
        return cls(
            assessment_trace_id=assessment.trace_id,
            assessment_fingerprint=safety_assessment_fingerprint(assessment),
            assessment_status=assessment.status,
            reviewer_id=reviewer_id,
            authority_reference=authority_reference,
            reviewed_at=reviewed_at,
            disposition=disposition,
            rationale=rationale,
        )

    def matches(self, assessment: SafetyAssessment) -> bool:
        if not isinstance(assessment, SafetyAssessment):
            raise TypeError("assessment must be a SafetyAssessment")
        return (
            self.assessment_trace_id == assessment.trace_id
            and self.assessment_status is assessment.status
            and self.assessment_fingerprint
            == safety_assessment_fingerprint(assessment)
        )

    @property
    def reasoning_execution_allowed(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


def safety_assessment_fingerprint(assessment: SafetyAssessment) -> str:
    if not isinstance(assessment, SafetyAssessment):
        raise TypeError("assessment must be a SafetyAssessment")
    payload = {
        "status": assessment.status.value,
        "snapshot_fingerprint": assessment.snapshot_fingerprint,
        "expected_check_ids": assessment.expected_check_ids,
        "results": [
            {
                "check_id": result.check_id,
                "outcome": result.outcome.value,
                "trace_id": result.trace_id,
                "snapshot_fingerprint": result.snapshot_fingerprint,
                "explanation": result.explanation,
                "evidence_source_ids": result.evidence_source_ids,
                "findings": [
                    {
                        "finding_id": finding.finding_id,
                        "severity": finding.severity.value,
                        "explanation": finding.explanation,
                        "evidence_source_ids": finding.evidence_source_ids,
                    }
                    for finding in result.findings
                ],
            }
            for result in assessment.results
        ],
        "missing_check_ids": assessment.missing_check_ids,
        "blocking_reasons": assessment.blocking_reasons,
        "trace_id": assessment.trace_id,
    }
    canonical = json.dumps(
        payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256(canonical).hexdigest()


def _fail(field_name: str, message: str) -> None:
    raise SafetyError(f"safety_review.{field_name}", message)
