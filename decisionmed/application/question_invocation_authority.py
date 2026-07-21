"""External authorization contract for a governed Question Engine call."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import re
from typing import Protocol, runtime_checkable


QUESTION_ENGINE_INVOCATION_ACTION = "reasoning.question-engine.generate"

_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_FINGERPRINT = re.compile(r"^[0-9a-f]{64}$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class QuestionEngineInvocationAuthorityStatus(str, Enum):
    AUTHORIZED = "authorized"
    DENIED = "denied"


@dataclass(frozen=True, slots=True)
class QuestionEngineInvocationAuthorityDecision:
    """Exact metadata-only authorization for one non-clinical engine call."""

    reviewer_id: str
    authority_reference: str
    authority_provider: str
    action: str
    trace_id: str
    governed_input_fingerprint: str
    engine_id: str
    engine_contract_version: str
    status: QuestionEngineInvocationAuthorityStatus
    decision_reference: str
    verified_at: datetime

    def __post_init__(self) -> None:
        for field_name in (
            "reviewer_id",
            "authority_reference",
            "authority_provider",
            "engine_id",
            "decision_reference",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
                raise ValueError(f"{field_name} must be canonical")
        if self.action != QUESTION_ENGINE_INVOCATION_ACTION:
            raise ValueError("action must identify Question Engine invocation")
        if not isinstance(self.trace_id, str) or not self.trace_id.strip():
            raise ValueError("trace_id cannot be empty")
        if (
            not isinstance(self.governed_input_fingerprint, str)
            or not _FINGERPRINT.fullmatch(self.governed_input_fingerprint)
        ):
            raise ValueError("governed_input_fingerprint must be SHA-256")
        if (
            not isinstance(self.engine_contract_version, str)
            or not _VERSION.fullmatch(self.engine_contract_version)
        ):
            raise ValueError("engine_contract_version must use semantic versioning")
        if not isinstance(self.status, QuestionEngineInvocationAuthorityStatus):
            raise TypeError("status must be a QuestionEngineInvocationAuthorityStatus")
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
        trace_id: str,
        governed_input_fingerprint: str,
        engine_id: str,
        engine_contract_version: str,
    ) -> bool:
        return (
            self.reviewer_id == reviewer_id
            and self.authority_reference == authority_reference
            and self.action == QUESTION_ENGINE_INVOCATION_ACTION
            and self.trace_id == trace_id
            and self.governed_input_fingerprint == governed_input_fingerprint
            and self.engine_id == engine_id
            and self.engine_contract_version == engine_contract_version
        )

    @property
    def invocation_allowed(self) -> bool:
        return self.status is QuestionEngineInvocationAuthorityStatus.AUTHORIZED

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


@runtime_checkable
class QuestionEngineInvocationAuthority(Protocol):
    """Port implemented by an external identity and authorization adapter."""

    @property
    def provider(self) -> str: ...

    def verify(
        self,
        *,
        reviewer_id: str,
        authority_reference: str,
        trace_id: str,
        governed_input_fingerprint: str,
        engine_id: str,
        engine_contract_version: str,
    ) -> QuestionEngineInvocationAuthorityDecision: ...
