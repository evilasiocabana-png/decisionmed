"""Authorized and audited application flow for safety-review recording."""

from __future__ import annotations

from datetime import datetime

from decisionmed.audit import AuditLedger
from decisionmed.domain import DomainError, DomainEvent
from decisionmed.safety import (
    SafetyAssessment,
    SafetyReviewDisposition,
    SafetyReviewRecord,
    safety_assessment_fingerprint,
)

from .reviewer_authority import (
    SafetyReviewerAuthority,
    SafetyReviewerAuthorityDecision,
)


class SafetyReviewApplicationError(DomainError):
    """Stable failure raised by safety-review application orchestration."""


class SafetyReviewApplicationService:
    """Return a review record only after exact authority and audit checks."""

    def __init__(
        self, authority: SafetyReviewerAuthority, audit: AuditLedger
    ) -> None:
        if not isinstance(authority, SafetyReviewerAuthority):
            raise TypeError("authority must implement SafetyReviewerAuthority")
        if not isinstance(audit, AuditLedger):
            raise TypeError("audit must be an AuditLedger")
        self._authority = authority
        self._audit = audit

    def record(
        self,
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
        fingerprint = safety_assessment_fingerprint(assessment)
        request_metadata = (
            ("reviewer_id", reviewer_id),
            ("authority_reference", authority_reference),
            ("assessment_fingerprint", fingerprint),
            ("clinical_execution_allowed", "false"),
            ("reasoning_execution_allowed", "false"),
        )

        try:
            decision = self._authority.verify(
                reviewer_id=reviewer_id,
                authority_reference=authority_reference,
                assessment_trace_id=assessment.trace_id,
                assessment_fingerprint=fingerprint,
            )
        except Exception as error:
            self._append(
                assessment,
                "safety.review_authority_failed",
                request_metadata + (("error_type", type(error).__name__),),
            )
            raise

        if not isinstance(decision, SafetyReviewerAuthorityDecision):
            self._append(
                assessment,
                "safety.review_authority_invalid",
                request_metadata + (("reason", "invalid_decision_type"),),
            )
            raise SafetyReviewApplicationError(
                "safety_review.invalid_authority_decision",
                "authority returned an invalid decision",
            )
        if (
            decision.authority_provider != self._authority.provider
            or not decision.matches_request(
                reviewer_id=reviewer_id,
                authority_reference=authority_reference,
                assessment_trace_id=assessment.trace_id,
                assessment_fingerprint=fingerprint,
            )
        ):
            self._append(
                assessment,
                "safety.review_authority_invalid",
                request_metadata
                + (
                    ("authority_provider", decision.authority_provider),
                    ("decision_reference", decision.decision_reference),
                    ("reason", "decision_mismatch"),
                ),
            )
            raise SafetyReviewApplicationError(
                "safety_review.authority_decision_mismatch",
                "authority decision does not match the review request",
            )
        if not decision.review_recording_allowed:
            self._append(
                assessment,
                "safety.review_authority_denied",
                request_metadata
                + (
                    ("authority_provider", decision.authority_provider),
                    ("decision_reference", decision.decision_reference),
                ),
            )
            raise SafetyReviewApplicationError(
                "safety_review.authority_denied",
                "authority denied safety-review recording",
            )

        try:
            record = SafetyReviewRecord.create(
                assessment,
                reviewer_id=reviewer_id,
                authority_reference=authority_reference,
                reviewed_at=reviewed_at,
                disposition=disposition,
                rationale=rationale,
            )
        except Exception as error:
            self._append(
                assessment,
                "safety.review_record_rejected",
                request_metadata
                + (
                    ("authority_provider", decision.authority_provider),
                    ("decision_reference", decision.decision_reference),
                    ("error_type", type(error).__name__),
                ),
            )
            raise

        self._append(
            assessment,
            "safety.review_recorded",
            request_metadata
            + (
                ("authority_provider", decision.authority_provider),
                ("decision_reference", decision.decision_reference),
                ("assessment_status", assessment.status.value),
                ("disposition", record.disposition.value),
            ),
        )
        return record

    @property
    def reasoning_execution_allowed(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False

    def _append(
        self,
        assessment: SafetyAssessment,
        event_name: str,
        payload: tuple[tuple[str, str], ...],
    ) -> None:
        self._audit.append(
            DomainEvent(
                name=event_name,
                aggregate_id=assessment.trace_id,
                payload=payload,
            ),
            assessment.trace_id,
        )
