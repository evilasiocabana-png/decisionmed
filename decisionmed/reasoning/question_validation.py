"""Fail-closed validation for externally produced Question Engine results."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import json
import re

from .gate import ReasoningError
from .governed_input import GovernedReasoningInput
from .question_engine import QuestionEngine, QuestionEngineResult


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
_FINGERPRINT = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True)
class QuestionEngineValidationReceipt:
    """Immutable proof that one result matched one governed input and port."""

    validator_id: str
    validator_version: str
    validated_at: datetime
    engine_id: str
    provider: str
    engine_contract_version: str
    governed_input_fingerprint: str
    result_fingerprint: str
    trace_id: str
    content_fingerprint: str = field(init=False)

    def __post_init__(self) -> None:
        for field_name in ("validator_id", "engine_id", "provider"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
                _fail(field_name, f"{field_name} must be canonical")
        for field_name in ("validator_version", "engine_contract_version"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not _VERSION.fullmatch(value):
                _fail(field_name, f"{field_name} must use semantic versioning")
        if (
            not isinstance(self.validated_at, datetime)
            or self.validated_at.tzinfo is None
            or self.validated_at.utcoffset() is None
        ):
            raise TypeError("validated_at must be a timezone-aware datetime")
        if self.validated_at > datetime.now(timezone.utc):
            _fail("validated_at", "validation time cannot be in the future")
        for field_name in ("governed_input_fingerprint", "result_fingerprint"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not _FINGERPRINT.fullmatch(value):
                _fail(field_name, f"{field_name} must be SHA-256")
        if not isinstance(self.trace_id, str) or not self.trace_id.strip():
            _fail("trace_id", "trace id cannot be empty")
        object.__setattr__(self, "content_fingerprint", self._fingerprint())

    @property
    def engine_invocation_allowed(self) -> bool:
        return False

    @property
    def reasoning_execution_allowed(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False

    def _fingerprint(self) -> str:
        payload = {
            "validator_id": self.validator_id,
            "validator_version": self.validator_version,
            "validated_at": self.validated_at.isoformat(),
            "engine_id": self.engine_id,
            "provider": self.provider,
            "engine_contract_version": self.engine_contract_version,
            "governed_input_fingerprint": self.governed_input_fingerprint,
            "result_fingerprint": self.result_fingerprint,
            "trace_id": self.trace_id,
        }
        return _fingerprint_payload(payload)


class QuestionEngineOutputValidator:
    """Validate output provenance and catalog references without invoking an engine."""

    validator_id = "decisionmed.question-output-validator"
    validator_version = "0.1.0"

    def validate(
        self,
        input_value: GovernedReasoningInput,
        result: QuestionEngineResult,
        engine: QuestionEngine,
        *,
        validated_at: datetime | None = None,
    ) -> QuestionEngineValidationReceipt:
        if not isinstance(input_value, GovernedReasoningInput):
            raise TypeError("input_value must be a GovernedReasoningInput")
        if not isinstance(result, QuestionEngineResult):
            raise TypeError("result must be a QuestionEngineResult")
        if not isinstance(engine, QuestionEngine):
            raise TypeError("engine must satisfy the QuestionEngine protocol")
        if not input_value.knowledge_binding_complete:
            _fail("knowledge_expired", "governed knowledge must remain current")
        if result.governed_input_fingerprint != input_value.content_fingerprint:
            _fail("input_fingerprint", "result must match the exact governed input")
        if result.trace_id != input_value.trace_id:
            _fail("trace_id", "result must preserve the governed input trace")
        if (
            result.engine_id != engine.engine_id
            or result.provider != engine.provider
            or result.engine_version != engine.contract_version
        ):
            _fail("engine_identity", "result identity must match the supplied port")

        binding = input_value.knowledge_binding
        known_fields = {
            field_value.field_key: field_value
            for schema in binding.form_schemas
            for field_value in schema.fields
        }
        unknown_gaps = set(result.open_gap_field_keys) - set(known_fields)
        if unknown_gaps:
            _fail("open_gaps", "open gaps must reference governed schema fields")

        known_object_ids = set(binding.knowledge_object_ids)
        known_source_ids = set(binding.evidence_source_ids)
        objects_by_id = {
            item.object_id: item for item in binding.knowledge_objects
        }
        for question in result.questions:
            field_value = known_fields.get(question.field_key)
            if field_value is None:
                _fail("question_field", "question must reference a governed field")
            object_ids = set(question.knowledge_object_ids)
            source_ids = set(question.evidence_source_ids)
            if not object_ids.issubset(known_object_ids):
                _fail("question_knowledge", "question knowledge must be bound")
            if field_value.knowledge_object_id not in object_ids:
                _fail(
                    "field_knowledge",
                    "question must cite the knowledge governing its field",
                )
            if not source_ids.issubset(known_source_ids):
                _fail("question_evidence", "question evidence must be bound")
            supported_source_ids = {
                anchor.source_id
                for object_id in object_ids
                for anchor in objects_by_id[object_id].evidence_anchors
            }
            if not source_ids.issubset(supported_source_ids):
                _fail(
                    "evidence_support",
                    "question evidence must support its cited knowledge",
                )

        timestamp = validated_at or datetime.now(timezone.utc)
        if (
            isinstance(timestamp, datetime)
            and timestamp.tzinfo is not None
            and timestamp.utcoffset() is not None
            and timestamp < input_value.assembled_at
        ):
            _fail("validated_at", "validation cannot predate input assembly")
        return QuestionEngineValidationReceipt(
            validator_id=self.validator_id,
            validator_version=self.validator_version,
            validated_at=timestamp,
            engine_id=result.engine_id,
            provider=result.provider,
            engine_contract_version=result.engine_version,
            governed_input_fingerprint=input_value.content_fingerprint,
            result_fingerprint=_result_fingerprint(result),
            trace_id=result.trace_id,
        )


def _result_fingerprint(result: QuestionEngineResult) -> str:
    payload = {
        "engine_id": result.engine_id,
        "engine_version": result.engine_version,
        "provider": result.provider,
        "governed_input_fingerprint": result.governed_input_fingerprint,
        "trace_id": result.trace_id,
        "state": result.state.value,
        "questions": [
            {
                "question_id": item.question_id,
                "field_key": item.field_key,
                "prompt": item.prompt,
                "requirement": item.requirement.value,
                "priority_rank": item.priority_rank,
                "rationale": item.rationale,
                "knowledge_object_ids": item.knowledge_object_ids,
                "evidence_source_ids": item.evidence_source_ids,
                "trace_id": item.trace_id,
                "governed_input_fingerprint": item.governed_input_fingerprint,
            }
            for item in result.questions
        ],
        "open_gap_field_keys": result.open_gap_field_keys,
        "explanation": result.explanation,
    }
    return _fingerprint_payload(payload)


def _fingerprint_payload(payload: object) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(canonical).hexdigest()


def _fail(field_name: str, message: str) -> None:
    raise ReasoningError(f"question_validation.{field_name}", message)
