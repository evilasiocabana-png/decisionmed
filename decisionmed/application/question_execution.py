"""Authorized, audited, and validated Question Engine orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Callable

from decisionmed.audit import AuditLedger
from decisionmed.domain import DomainError, DomainEvent
from decisionmed.reasoning import (
    GovernedReasoningInput,
    QuestionEngineOutputValidator,
    QuestionEngineReadiness,
    QuestionEngineReadinessStatus,
    QuestionEngineRegistry,
    QuestionEngineResult,
    QuestionEngineValidationReceipt,
)

from .question_invocation_authority import (
    QuestionEngineInvocationAuthority,
    QuestionEngineInvocationAuthorityDecision,
)


class QuestionEngineExecutionError(DomainError):
    """Stable failure raised by Question Engine application orchestration."""


@dataclass(frozen=True, slots=True)
class QuestionEngineInvocationResult:
    """One validated output with the exact external authorization reference."""

    result: QuestionEngineResult = field(repr=False)
    receipt: QuestionEngineValidationReceipt
    decision_reference: str

    @property
    def engine_invocation_allowed(self) -> bool:
        return False

    @property
    def reasoning_execution_allowed(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


class QuestionEngineExecutionApplicationService:
    """Invoke a registered engine only after exact authorization and audit gates."""

    def __init__(
        self,
        readiness: QuestionEngineReadiness,
        registry: QuestionEngineRegistry,
        authority: QuestionEngineInvocationAuthority,
        validator: QuestionEngineOutputValidator,
        audit: AuditLedger,
        max_authority_age: timedelta = timedelta(minutes=5),
        now: Callable[[], datetime] | None = None,
    ) -> None:
        if not isinstance(readiness, QuestionEngineReadiness):
            raise TypeError("readiness must be a QuestionEngineReadiness")
        if not isinstance(registry, QuestionEngineRegistry):
            raise TypeError("registry must be a QuestionEngineRegistry")
        if not isinstance(authority, QuestionEngineInvocationAuthority):
            raise TypeError("authority must satisfy QuestionEngineInvocationAuthority")
        if not isinstance(validator, QuestionEngineOutputValidator):
            raise TypeError("validator must be a QuestionEngineOutputValidator")
        if not isinstance(audit, AuditLedger):
            raise TypeError("audit must be an AuditLedger")
        if (
            not isinstance(max_authority_age, timedelta)
            or max_authority_age <= timedelta(0)
        ):
            raise ValueError("max_authority_age must be positive")
        self._readiness = readiness
        self._registry = registry
        self._authority = authority
        self._validator = validator
        self._audit = audit
        self._max_authority_age = max_authority_age
        self._now = now or (lambda: datetime.now(timezone.utc))

    def generate(
        self,
        input_value: GovernedReasoningInput,
        *,
        engine_id: str,
        reviewer_id: str,
        authority_reference: str,
    ) -> QuestionEngineInvocationResult:
        if not isinstance(input_value, GovernedReasoningInput):
            raise TypeError("input_value must be a GovernedReasoningInput")
        metadata = self._metadata(input_value, engine_id)
        try:
            readiness = self._readiness.assess(
                input_value, self._registry, engine_id
            )
        except Exception as error:
            self._append(
                input_value,
                "reasoning.question-engine-readiness-failed",
                metadata + (("error_type", type(error).__name__),),
            )
            raise
        if (
            readiness.status
            is not QuestionEngineReadinessStatus.STRUCTURAL_PREREQUISITES_PRESENT
        ):
            self._append(
                input_value,
                "reasoning.question-engine-invocation-blocked",
                metadata
                + (
                    ("readiness_status", readiness.status.value),
                    ("reason_count", str(len(readiness.reasons))),
                ),
            )
            raise QuestionEngineExecutionError(
                "question_engine_execution.not_ready",
                "structural prerequisites are not present",
            )
        engine = self._registry.get(engine_id)
        if engine is None:
            raise AssertionError("ready engine must be registered")

        request_metadata = metadata + (
            ("reviewer_id", reviewer_id),
            ("authority_reference", authority_reference),
            ("engine_contract_version", engine.contract_version),
        )
        try:
            decision = self._authority.verify(
                reviewer_id=reviewer_id,
                authority_reference=authority_reference,
                trace_id=input_value.trace_id,
                governed_input_fingerprint=input_value.content_fingerprint,
                engine_id=engine.engine_id,
                engine_contract_version=engine.contract_version,
            )
        except Exception as error:
            self._append(
                input_value,
                "reasoning.question-engine-authority-failed",
                request_metadata + (("error_type", type(error).__name__),),
            )
            raise
        if (
            not isinstance(decision, QuestionEngineInvocationAuthorityDecision)
            or decision.authority_provider != self._authority.provider
            or not decision.matches_request(
                reviewer_id=reviewer_id,
                authority_reference=authority_reference,
                trace_id=input_value.trace_id,
                governed_input_fingerprint=input_value.content_fingerprint,
                engine_id=engine.engine_id,
                engine_contract_version=engine.contract_version,
            )
        ):
            self._append(
                input_value,
                "reasoning.question-engine-authority-invalid",
                request_metadata + (("reason", "decision_mismatch"),),
            )
            raise QuestionEngineExecutionError(
                "question_engine_execution.authority_decision_mismatch",
                "authority decision does not match the invocation request",
            )
        if not decision.invocation_allowed:
            self._append(
                input_value,
                "reasoning.question-engine-authority-denied",
                request_metadata
                + (
                    ("authority_provider", decision.authority_provider),
                    ("decision_reference", decision.decision_reference),
                ),
            )
            raise QuestionEngineExecutionError(
                "question_engine_execution.authority_denied",
                "authority denied Question Engine invocation",
            )
        if self._authority_expired(decision):
            self._append(
                input_value,
                "reasoning.question-engine-authority-expired",
                request_metadata
                + (
                    ("authority_provider", decision.authority_provider),
                    ("decision_reference", decision.decision_reference),
                    ("verified_at", decision.verified_at.isoformat()),
                ),
            )
            raise QuestionEngineExecutionError(
                "question_engine_execution.authority_expired",
                "authority decision is no longer current",
            )
        self._append(
            input_value,
            "reasoning.question-engine-invocation-authorized",
            request_metadata
            + (
                ("authority_provider", decision.authority_provider),
                ("decision_reference", decision.decision_reference),
            ),
        )
        try:
            result = engine.generate(input_value)
        except Exception as error:
            self._append(
                input_value,
                "reasoning.question-engine-generation-failed",
                request_metadata
                + (
                    ("authority_provider", decision.authority_provider),
                    ("decision_reference", decision.decision_reference),
                    ("error_type", type(error).__name__),
                ),
            )
            raise
        try:
            receipt = self._validator.validate(input_value, result, engine)
        except Exception as error:
            self._append(
                input_value,
                "reasoning.question-engine-output-rejected",
                request_metadata
                + (
                    ("authority_provider", decision.authority_provider),
                    ("decision_reference", decision.decision_reference),
                    ("error_type", type(error).__name__),
                ),
            )
            raise
        self._append(
            input_value,
            "reasoning.question-engine-generated",
            request_metadata
            + (
                ("authority_provider", decision.authority_provider),
                ("decision_reference", decision.decision_reference),
                ("result_fingerprint", receipt.result_fingerprint),
                ("receipt_fingerprint", receipt.content_fingerprint),
                ("result_state", result.state.value),
                ("question_count", str(len(result.questions))),
                ("open_gap_count", str(len(result.open_gap_field_keys))),
            ),
        )
        return QuestionEngineInvocationResult(
            result=result,
            receipt=receipt,
            decision_reference=decision.decision_reference,
        )

    @property
    def engine_invocation_allowed(self) -> bool:
        return False

    @property
    def reasoning_execution_allowed(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False

    @staticmethod
    def _metadata(
        input_value: GovernedReasoningInput, engine_id: str
    ) -> tuple[tuple[str, str], ...]:
        return (
            ("engine_id", engine_id),
            ("governed_input_fingerprint", input_value.content_fingerprint),
            ("knowledge_binding_fingerprint", input_value.knowledge_binding_fingerprint),
            ("specialty", input_value.specialty_key),
            ("engine_invocation_allowed", "false"),
            ("reasoning_execution_allowed", "false"),
            ("clinical_execution_allowed", "false"),
        )

    def _authority_expired(
        self, decision: QuestionEngineInvocationAuthorityDecision
    ) -> bool:
        current_time = self._now()
        if (
            not isinstance(current_time, datetime)
            or current_time.tzinfo is None
            or current_time.utcoffset() is None
        ):
            raise TypeError("now must return a timezone-aware datetime")
        return current_time - decision.verified_at > self._max_authority_age

    def _append(
        self,
        input_value: GovernedReasoningInput,
        event_name: str,
        payload: tuple[tuple[str, str], ...],
    ) -> None:
        self._audit.append(
            DomainEvent(
                name=event_name,
                aggregate_id=input_value.input_id,
                payload=payload,
            ),
            input_value.trace_id,
        )
