"""Audited application preparation for a future Question Engine invocation."""

from __future__ import annotations

from decisionmed.audit import AuditLedger
from decisionmed.domain import DomainEvent
from decisionmed.reasoning import (
    GovernedReasoningInput,
    QuestionEngineReadiness,
    QuestionEngineReadinessReport,
    QuestionEngineRegistry,
)


class QuestionEnginePreparationApplicationService:
    """Audit structural readiness without invoking a Question Engine."""

    def __init__(
        self,
        readiness: QuestionEngineReadiness,
        registry: QuestionEngineRegistry,
        audit: AuditLedger,
    ) -> None:
        if not isinstance(readiness, QuestionEngineReadiness):
            raise TypeError("readiness must be a QuestionEngineReadiness")
        if not isinstance(registry, QuestionEngineRegistry):
            raise TypeError("registry must be a QuestionEngineRegistry")
        if not isinstance(audit, AuditLedger):
            raise TypeError("audit must be an AuditLedger")
        self._readiness = readiness
        self._registry = registry
        self._audit = audit

    def prepare(
        self,
        input_value: GovernedReasoningInput,
        *,
        engine_id: str,
    ) -> QuestionEngineReadinessReport:
        if not isinstance(input_value, GovernedReasoningInput):
            raise TypeError("input_value must be a GovernedReasoningInput")
        metadata = (
            ("engine_id", engine_id),
            ("governed_input_fingerprint", input_value.content_fingerprint),
            ("knowledge_binding_fingerprint", input_value.knowledge_binding_fingerprint),
            ("specialty", input_value.specialty_key),
            ("engine_invocation_allowed", "false"),
            ("reasoning_execution_allowed", "false"),
            ("clinical_execution_allowed", "false"),
        )
        try:
            report = self._readiness.assess(
                input_value,
                self._registry,
                engine_id,
            )
        except Exception as error:
            self._append(
                input_value,
                "reasoning.question_engine_preparation_failed",
                metadata + (("error_type", type(error).__name__),),
            )
            raise
        self._append(
            input_value,
            "reasoning.question_engine_preparation_completed",
            metadata
            + (
                ("status", report.status.value),
                ("reason_count", str(len(report.reasons))),
            ),
        )
        return report

    @property
    def engine_invocation_allowed(self) -> bool:
        return False

    @property
    def reasoning_execution_allowed(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False

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
