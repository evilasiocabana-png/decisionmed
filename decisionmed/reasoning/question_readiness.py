"""Non-executing readiness assessment for a governed Question Engine path."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re

from .gate import ReasoningError, ReasoningGateStatus
from .governed_input import GovernedReasoningInput
from .question_registry import QuestionEngineRegistry


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")


class QuestionEngineReadinessStatus(str, Enum):
    BLOCKED = "blocked"
    STRUCTURAL_PREREQUISITES_PRESENT = "structural_prerequisites_present"


@dataclass(frozen=True, slots=True)
class QuestionEngineReadinessReport:
    """Structural status only; never permission to invoke clinical reasoning."""

    status: QuestionEngineReadinessStatus
    engine_id: str
    governed_input_fingerprint: str
    trace_id: str
    reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.status, QuestionEngineReadinessStatus):
            raise TypeError("status must be a QuestionEngineReadinessStatus")
        if not isinstance(self.engine_id, str) or not _IDENTIFIER.fullmatch(
            self.engine_id
        ):
            _fail("engine_id", "engine id must be canonical")
        if (
            not isinstance(self.governed_input_fingerprint, str)
            or not re.fullmatch(r"[0-9a-f]{64}", self.governed_input_fingerprint)
        ):
            _fail("governed_input_fingerprint", "input fingerprint must be SHA-256")
        if not isinstance(self.trace_id, str) or not self.trace_id.strip():
            _fail("trace_id", "trace id cannot be empty")
        reasons = tuple(self.reasons)
        if not reasons or any(
            not isinstance(reason, str) or not reason.strip() for reason in reasons
        ):
            _fail("reasons", "at least one non-empty reason is required")
        if len(set(reasons)) != len(reasons):
            _fail("reasons", "reasons must be unique")
        ready_reasons = (
            "structural_prerequisites_present",
            "audited_invocation_orchestration_required",
        )
        if (
            self.status
            is QuestionEngineReadinessStatus.STRUCTURAL_PREREQUISITES_PRESENT
            and reasons != ready_reasons
        ):
            _fail("reasons", "ready status requires the exact structural reasons")
        if (
            self.status is QuestionEngineReadinessStatus.BLOCKED
            and "structural_prerequisites_present" in reasons
        ):
            _fail("reasons", "blocked status cannot claim structural readiness")
        object.__setattr__(self, "reasons", reasons)

    @property
    def structural_prerequisites_present(self) -> bool:
        return (
            self.status
            is QuestionEngineReadinessStatus.STRUCTURAL_PREREQUISITES_PRESENT
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


class QuestionEngineReadiness:
    """Report missing structural prerequisites without calling an engine."""

    def assess(
        self,
        input_value: GovernedReasoningInput,
        registry: QuestionEngineRegistry,
        engine_id: str,
    ) -> QuestionEngineReadinessReport:
        if not isinstance(input_value, GovernedReasoningInput):
            raise TypeError("input_value must be a GovernedReasoningInput")
        if not isinstance(registry, QuestionEngineRegistry):
            raise TypeError("registry must be a QuestionEngineRegistry")
        if not isinstance(engine_id, str) or not _IDENTIFIER.fullmatch(engine_id):
            _fail("engine_id", "engine id must be canonical")

        binding_ids = {item.engine_id for item in registry.bindings}
        reasons = []
        if engine_id not in binding_ids:
            reasons.append("engine_binding_missing")
        elif registry.get(engine_id) is None:
            reasons.append("engine_implementation_missing")
        if not input_value.envelope.snapshot.structurally_complete:
            reasons.append("snapshot_incomplete")
        if (
            input_value.envelope.gate_result.status
            is not ReasoningGateStatus.SAFETY_REVIEW_RECORDED
        ):
            reasons.append("safety_review_not_recorded")
        if not input_value.knowledge_binding_complete:
            reasons.append("governed_knowledge_not_current")

        if reasons:
            status = QuestionEngineReadinessStatus.BLOCKED
        else:
            status = (
                QuestionEngineReadinessStatus.STRUCTURAL_PREREQUISITES_PRESENT
            )
            reasons = [
                "structural_prerequisites_present",
                "audited_invocation_orchestration_required",
            ]
        return QuestionEngineReadinessReport(
            status=status,
            engine_id=engine_id,
            governed_input_fingerprint=input_value.content_fingerprint,
            trace_id=input_value.trace_id,
            reasons=tuple(reasons),
        )


def _fail(field_name: str, message: str) -> None:
    raise ReasoningError(f"question_engine_readiness.{field_name}", message)
