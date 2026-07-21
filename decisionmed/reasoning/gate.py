"""Fail-closed prerequisites for future clinical reasoning."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re

from decisionmed.domain import ClinicalSnapshot
from decisionmed.safety import (
    SafetyAssessment,
    SafetyGateStatus,
    SafetyReviewDisposition,
    SafetyReviewRecord,
)


_FINGERPRINT = re.compile(r"^[0-9a-f]{64}$")


class ReasoningError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class ReasoningGateStatus(str, Enum):
    SNAPSHOT_INCOMPLETE = "snapshot_incomplete"
    SAFETY_INCOMPLETE = "safety_incomplete"
    SAFETY_BLOCKED = "safety_blocked"
    SAFETY_HUMAN_REVIEW_REQUIRED = "safety_human_review_required"
    AWAITING_HUMAN_SAFETY_VALIDATION = "awaiting_human_safety_validation"
    SAFETY_REASSESSMENT_REQUIRED = "safety_reassessment_required"
    SAFETY_REVIEW_RECORDED = "safety_review_recorded"


@dataclass(frozen=True, slots=True)
class ReasoningGateResult:
    status: ReasoningGateStatus
    snapshot_id: str
    safety_status: SafetyGateStatus
    reasons: tuple[str, ...]
    trace_id: str
    safety_review_fingerprint: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.status, ReasoningGateStatus):
            raise TypeError("status must be a ReasoningGateStatus")
        if not isinstance(self.safety_status, SafetyGateStatus):
            raise TypeError("safety_status must be a SafetyGateStatus")
        for field_name in ("snapshot_id", "trace_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ReasoningError(
                    f"reasoning.{field_name}", f"{field_name} cannot be empty"
                )
        reasons = tuple(self.reasons)
        if not reasons or any(
            not isinstance(reason, str) or not reason.strip() for reason in reasons
        ):
            raise ReasoningError(
                "reasoning.reasons", "at least one non-empty reason is required"
            )
        object.__setattr__(self, "reasons", reasons)
        review_states = {
            ReasoningGateStatus.SAFETY_REASSESSMENT_REQUIRED,
            ReasoningGateStatus.SAFETY_REVIEW_RECORDED,
        }
        if self.status in review_states:
            if (
                not isinstance(self.safety_review_fingerprint, str)
                or not _FINGERPRINT.fullmatch(self.safety_review_fingerprint)
            ):
                raise ReasoningError(
                    "reasoning.safety_review_fingerprint",
                    "review state requires a SHA-256 safety review fingerprint",
                )
        elif self.safety_review_fingerprint is not None:
            raise ReasoningError(
                "reasoning.unexpected_safety_review_fingerprint",
                "non-review state cannot contain a safety review fingerprint",
            )

    @property
    def reasoning_execution_allowed(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


class ReasoningGate:
    """Require snapshot and safety review before any future reasoning engine."""

    def assess(
        self,
        snapshot: ClinicalSnapshot,
        safety: SafetyAssessment,
        review: SafetyReviewRecord | None = None,
    ) -> ReasoningGateResult:
        if not isinstance(snapshot, ClinicalSnapshot):
            raise TypeError("snapshot must be a ClinicalSnapshot")
        if not isinstance(safety, SafetyAssessment):
            raise TypeError("safety must be a SafetyAssessment")
        if review is not None and not isinstance(review, SafetyReviewRecord):
            raise TypeError("review must be a SafetyReviewRecord or None")
        if snapshot.trace_id != safety.trace_id:
            raise ReasoningError(
                "reasoning.trace_mismatch",
                "snapshot and safety assessment must share a trace",
            )

        if not snapshot.structurally_complete:
            status = ReasoningGateStatus.SNAPSHOT_INCOMPLETE
            reasons = tuple(
                f"missing_snapshot_section:{section.value}"
                for section in snapshot.missing_sections
            )
        elif safety.status is SafetyGateStatus.INCOMPLETE:
            status = ReasoningGateStatus.SAFETY_INCOMPLETE
            reasons = safety.blocking_reasons
        elif safety.status is SafetyGateStatus.BLOCKED:
            status = ReasoningGateStatus.SAFETY_BLOCKED
            reasons = safety.blocking_reasons
        elif safety.status is SafetyGateStatus.HUMAN_REVIEW_REQUIRED:
            status = ReasoningGateStatus.SAFETY_HUMAN_REVIEW_REQUIRED
            reasons = safety.blocking_reasons
        else:
            if review is None:
                status = ReasoningGateStatus.AWAITING_HUMAN_SAFETY_VALIDATION
                reasons = ("human_safety_validation_required",)
            elif not review.matches(safety):
                raise ReasoningError(
                    "reasoning.safety_review_mismatch",
                    "safety review must match the exact safety assessment",
                )
            elif review.reviewed_at < snapshot.captured_at:
                raise ReasoningError(
                    "reasoning.safety_review_stale",
                    "safety review cannot predate the clinical snapshot",
                )
            elif (
                review.disposition
                is SafetyReviewDisposition.REASSESSMENT_REQUIRED
            ):
                status = ReasoningGateStatus.SAFETY_REASSESSMENT_REQUIRED
                reasons = ("human_safety_reassessment_required",)
            else:
                status = ReasoningGateStatus.SAFETY_REVIEW_RECORDED
                reasons = (
                    "human_safety_review_recorded",
                    "reasoning_implementation_required",
                )

        return ReasoningGateResult(
            status=status,
            snapshot_id=str(snapshot.snapshot_id),
            safety_status=safety.status,
            reasons=reasons,
            trace_id=snapshot.trace_id,
            safety_review_fingerprint=(
                review.assessment_fingerprint
                if status
                in {
                    ReasoningGateStatus.SAFETY_REASSESSMENT_REQUIRED,
                    ReasoningGateStatus.SAFETY_REVIEW_RECORDED,
                }
                else None
            ),
        )
