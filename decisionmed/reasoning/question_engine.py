"""Structural Question Engine contracts with no concrete implementation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Protocol, runtime_checkable

from .gate import ReasoningError
from .governed_input import GovernedReasoningInput


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
_FINGERPRINT = re.compile(r"^[0-9a-f]{64}$")


class QuestionRequirement(str, Enum):
    REQUIRED = "required"
    CONDITIONAL = "conditional"


class QuestionEngineState(str, Enum):
    COLLECTION_PENDING = "collection_pending"
    COLLECTION_SUFFICIENT = "collection_sufficient"
    UNCERTAINTY_PERSISTS = "uncertainty_persists"


@dataclass(frozen=True, slots=True)
class QuestionEngineItem:
    """One traceable Reasoning output record, not a Domain entity."""

    question_id: str
    field_key: str
    prompt: str
    requirement: QuestionRequirement
    priority_rank: int
    rationale: str
    knowledge_object_ids: tuple[str, ...]
    evidence_source_ids: tuple[str, ...]
    trace_id: str
    governed_input_fingerprint: str

    def __post_init__(self) -> None:
        _identifier("question_id", self.question_id)
        _identifier("field_key", self.field_key)
        _text("prompt", self.prompt, 2000)
        if not isinstance(self.requirement, QuestionRequirement):
            raise TypeError("requirement must be a QuestionRequirement")
        if (
            not isinstance(self.priority_rank, int)
            or isinstance(self.priority_rank, bool)
            or not 1 <= self.priority_rank <= 1000
        ):
            _fail("priority_rank", "priority rank must be between 1 and 1000")
        _text("rationale", self.rationale, 4000)
        object.__setattr__(
            self,
            "knowledge_object_ids",
            _identifiers("knowledge_object_ids", self.knowledge_object_ids),
        )
        object.__setattr__(
            self,
            "evidence_source_ids",
            _identifiers("evidence_source_ids", self.evidence_source_ids),
        )
        _text("trace_id", self.trace_id, 200)
        _fingerprint(self.governed_input_fingerprint)

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class QuestionEngineResult:
    """Prioritized, structurally validated Question Engine output."""

    engine_id: str
    engine_version: str
    provider: str
    governed_input_fingerprint: str
    trace_id: str
    state: QuestionEngineState
    questions: tuple[QuestionEngineItem, ...]
    open_gap_field_keys: tuple[str, ...]
    explanation: str

    def __post_init__(self) -> None:
        _identifier("engine_id", self.engine_id)
        _identifier("provider", self.provider)
        if not isinstance(self.engine_version, str) or not _VERSION.fullmatch(
            self.engine_version
        ):
            _fail("engine_version", "engine version must use semantic versioning")
        _fingerprint(self.governed_input_fingerprint)
        _text("trace_id", self.trace_id, 200)
        if not isinstance(self.state, QuestionEngineState):
            raise TypeError("state must be a QuestionEngineState")

        questions = tuple(self.questions)
        if not all(isinstance(item, QuestionEngineItem) for item in questions):
            raise TypeError("questions must contain QuestionEngineItem values")
        questions = tuple(sorted(questions, key=lambda item: item.priority_rank))
        if len({item.question_id for item in questions}) != len(questions):
            _fail("questions", "question ids must be unique")
        if tuple(item.priority_rank for item in questions) != tuple(
            range(1, len(questions) + 1)
        ):
            _fail("questions", "question priority ranks must be contiguous")
        if any(
            item.trace_id != self.trace_id
            or item.governed_input_fingerprint
            != self.governed_input_fingerprint
            for item in questions
        ):
            _fail("questions", "questions must match the exact engine input")

        gaps = _identifiers(
            "open_gap_field_keys",
            self.open_gap_field_keys,
            allow_empty=True,
        )
        if not {item.field_key for item in questions}.issubset(gaps):
            _fail("open_gap_field_keys", "every question must address an open gap")
        if self.state is QuestionEngineState.COLLECTION_SUFFICIENT and (
            questions or gaps
        ):
            _fail("state", "sufficient collection cannot contain open questions")
        if self.state is QuestionEngineState.COLLECTION_PENDING and (
            not questions or not gaps
        ):
            _fail("state", "pending collection requires questions and open gaps")
        if self.state is QuestionEngineState.UNCERTAINTY_PERSISTS and not gaps:
            _fail("state", "persistent uncertainty requires an explicit open gap")
        _text("explanation", self.explanation, 4000)
        object.__setattr__(self, "questions", questions)
        object.__setattr__(self, "open_gap_field_keys", gaps)

    @property
    def knowledge_object_ids(self) -> tuple[str, ...]:
        return tuple(
            dict.fromkeys(
                value
                for question in self.questions
                for value in question.knowledge_object_ids
            )
        )

    @property
    def evidence_source_ids(self) -> tuple[str, ...]:
        return tuple(
            dict.fromkeys(
                value
                for question in self.questions
                for value in question.evidence_source_ids
            )
        )

    @property
    def reasoning_execution_allowed(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


@runtime_checkable
class QuestionEngine(Protocol):
    """Port for a future governed Question Engine implementation."""

    @property
    def engine_id(self) -> str: ...

    @property
    def provider(self) -> str: ...

    @property
    def contract_version(self) -> str: ...

    def generate(self, input_value: GovernedReasoningInput) -> QuestionEngineResult: ...


def _identifier(field_name: str, value: object) -> None:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        _fail(field_name, f"{field_name} must be canonical")


def _identifiers(
    field_name: str,
    values: object,
    *,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        _fail(field_name, f"{field_name} must be a collection")
    items = tuple(values)  # type: ignore[arg-type]
    if not items and not allow_empty:
        _fail(field_name, f"{field_name} cannot be empty")
    for value in items:
        _identifier(field_name, value)
    if len(set(items)) != len(items):
        _fail(field_name, f"{field_name} must be unique")
    return items


def _text(field_name: str, value: object, maximum: int) -> None:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        _fail(field_name, f"{field_name} must contain 1 to {maximum} characters")


def _fingerprint(value: object) -> None:
    if not isinstance(value, str) or not _FINGERPRINT.fullmatch(value):
        _fail("governed_input_fingerprint", "input fingerprint must be SHA-256")


def _fail(field_name: str, message: str) -> None:
    raise ReasoningError(f"question_engine.{field_name}", message)
