"""Fail-closed prerequisites for future clinical reasoning."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from decisionmed.domain import ClinicalSnapshot
from decisionmed.safety import SafetyAssessment, SafetyGateStatus


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


@dataclass(frozen=True, slots=True)
class ReasoningGateResult:
    status: ReasoningGateStatus
    snapshot_id: str
    safety_status: SafetyGateStatus
    reasons: tuple[str, ...]
    trace_id: str

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

    @property
    def reasoning_execution_allowed(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


class ReasoningGate:
    """Require snapshot and safety review before any future reasoning engine."""

    def assess(
        self, snapshot: ClinicalSnapshot, safety: SafetyAssessment
    ) -> ReasoningGateResult:
        if not isinstance(snapshot, ClinicalSnapshot):
            raise TypeError("snapshot must be a ClinicalSnapshot")
        if not isinstance(safety, SafetyAssessment):
            raise TypeError("safety must be a SafetyAssessment")
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
            status = ReasoningGateStatus.AWAITING_HUMAN_SAFETY_VALIDATION
            reasons = ("human_safety_validation_required",)

        return ReasoningGateResult(
            status=status,
            snapshot_id=str(snapshot.snapshot_id),
            safety_status=safety.status,
            reasons=reasons,
            trace_id=snapshot.trace_id,
        )
