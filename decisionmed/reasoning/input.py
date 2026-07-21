"""Exact, non-executable input envelope for future reasoning engines."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import re

from decisionmed.domain import ClinicalSnapshot
from decisionmed.safety import (
    SafetyAssessment,
    SafetyReviewRecord,
    safety_assessment_fingerprint,
)

from .gate import (
    ReasoningError,
    ReasoningGate,
    ReasoningGateResult,
    ReasoningGateStatus,
)


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


@dataclass(frozen=True, slots=True)
class ReasoningInputEnvelope:
    """Prepared identity chain; never permission to invoke clinical reasoning."""

    envelope_id: str
    contract_version: str
    producer: str
    prepared_at: datetime
    snapshot: ClinicalSnapshot = field(repr=False)
    safety: SafetyAssessment = field(repr=False)
    safety_review: SafetyReviewRecord = field(repr=False)
    gate_result: ReasoningGateResult = field(repr=False)

    def __post_init__(self) -> None:
        for field_name in ("envelope_id", "producer"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
                _fail(field_name, f"{field_name} must be canonical")
        if (
            not isinstance(self.contract_version, str)
            or not _VERSION.fullmatch(self.contract_version)
        ):
            _fail("contract_version", "contract version must use semantic versioning")
        if not isinstance(self.snapshot, ClinicalSnapshot):
            raise TypeError("snapshot must be a ClinicalSnapshot")
        if not isinstance(self.safety, SafetyAssessment):
            raise TypeError("safety must be a SafetyAssessment")
        if not isinstance(self.safety_review, SafetyReviewRecord):
            raise TypeError("safety_review must be a SafetyReviewRecord")
        if not isinstance(self.gate_result, ReasoningGateResult):
            raise TypeError("gate_result must be a ReasoningGateResult")
        if (
            not isinstance(self.prepared_at, datetime)
            or self.prepared_at.tzinfo is None
            or self.prepared_at.utcoffset() is None
        ):
            raise TypeError("prepared_at must be a timezone-aware datetime")
        if self.prepared_at > datetime.now(timezone.utc):
            _fail("prepared_at", "preparation time cannot be in the future")
        if self.prepared_at < self.snapshot.captured_at:
            _fail("prepared_at", "preparation cannot predate the snapshot")
        if self.prepared_at < self.safety_review.reviewed_at:
            _fail("prepared_at", "preparation cannot predate the safety review")

        expected_gate = ReasoningGate().assess(
            self.snapshot,
            self.safety,
            self.safety_review,
        )
        if expected_gate.status is not ReasoningGateStatus.SAFETY_REVIEW_RECORDED:
            _fail(
                "gate_status",
                "only an exact validated safety review can prepare reasoning input",
            )
        if self.gate_result != expected_gate:
            _fail("gate_result", "gate result does not match the exact input chain")

    @classmethod
    def prepare(
        cls,
        snapshot: ClinicalSnapshot,
        safety: SafetyAssessment,
        safety_review: SafetyReviewRecord,
        *,
        envelope_id: str,
        producer: str,
        prepared_at: datetime,
        contract_version: str = "0.1.0",
    ) -> ReasoningInputEnvelope:
        gate_result = ReasoningGate().assess(snapshot, safety, safety_review)
        return cls(
            envelope_id=envelope_id,
            contract_version=contract_version,
            producer=producer,
            prepared_at=prepared_at,
            snapshot=snapshot,
            safety=safety,
            safety_review=safety_review,
            gate_result=gate_result,
        )

    @property
    def trace_id(self) -> str:
        return self.snapshot.trace_id

    @property
    def snapshot_fingerprint(self) -> str:
        return self.snapshot.content_fingerprint

    @property
    def safety_assessment_fingerprint(self) -> str:
        return safety_assessment_fingerprint(self.safety)

    @property
    def knowledge_binding_complete(self) -> bool:
        return False

    @property
    def engine_invocation_allowed(self) -> bool:
        return False

    @property
    def reasoning_execution_allowed(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


def _fail(field_name: str, message: str) -> None:
    raise ReasoningError(f"reasoning_input.{field_name}", message)
