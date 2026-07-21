"""Safety First structural contracts with no embedded clinical rules."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")


class SafetyError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class SafetySeverity(str, Enum):
    INFORMATION = "information"
    CAUTION = "caution"
    CRITICAL = "critical"


class SafetyCheckOutcome(str, Enum):
    PASSED = "passed"
    FINDING = "finding"
    NOT_EVALUATED = "not_evaluated"


class SafetyGateStatus(str, Enum):
    INCOMPLETE = "incomplete"
    BLOCKED = "blocked"
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    READY_FOR_HUMAN_REVIEW = "ready_for_human_review"


@dataclass(frozen=True, slots=True)
class SafetyFinding:
    finding_id: str
    severity: SafetySeverity
    explanation: str
    evidence_source_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _identifier("finding_id", self.finding_id)
        if not isinstance(self.severity, SafetySeverity):
            raise TypeError("severity must be a SafetySeverity")
        _text("explanation", self.explanation)
        object.__setattr__(
            self,
            "evidence_source_ids",
            _identifiers("evidence_source_ids", self.evidence_source_ids),
        )


@dataclass(frozen=True, slots=True)
class SafetyCheckResult:
    check_id: str
    outcome: SafetyCheckOutcome
    trace_id: str
    explanation: str
    evidence_source_ids: tuple[str, ...] = ()
    findings: tuple[SafetyFinding, ...] = ()

    def __post_init__(self) -> None:
        _identifier("check_id", self.check_id)
        if not isinstance(self.outcome, SafetyCheckOutcome):
            raise TypeError("outcome must be a SafetyCheckOutcome")
        _text("trace_id", self.trace_id)
        _text("explanation", self.explanation)
        if len(self.explanation) > 4000:
            _fail("explanation", "explanation cannot exceed 4000 characters")
        source_ids = tuple(self.evidence_source_ids)
        if self.outcome is not SafetyCheckOutcome.NOT_EVALUATED:
            source_ids = _identifiers("evidence_source_ids", source_ids)
        elif source_ids:
            source_ids = _identifiers("evidence_source_ids", source_ids)
        findings = tuple(self.findings)
        if not all(isinstance(item, SafetyFinding) for item in findings):
            raise TypeError("findings must contain only SafetyFinding values")
        if self.outcome is SafetyCheckOutcome.FINDING and not findings:
            _fail("findings", "finding outcome requires at least one finding")
        if self.outcome is not SafetyCheckOutcome.FINDING and findings:
            _fail("findings", "only finding outcome may include findings")
        object.__setattr__(self, "evidence_source_ids", source_ids)
        object.__setattr__(self, "findings", findings)


@dataclass(frozen=True, slots=True)
class SafetyAssessment:
    status: SafetyGateStatus
    expected_check_ids: tuple[str, ...]
    results: tuple[SafetyCheckResult, ...]
    missing_check_ids: tuple[str, ...]
    blocking_reasons: tuple[str, ...]
    trace_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.status, SafetyGateStatus):
            raise TypeError("status must be a SafetyGateStatus")
        expected = tuple(self.expected_check_ids)
        results = tuple(self.results)
        missing = tuple(self.missing_check_ids)
        reasons = tuple(self.blocking_reasons)
        if not expected or len(set(expected)) != len(expected):
            _fail("expected_check_ids", "expected checks must be non-empty and unique")
        for check_id in expected:
            _identifier("expected_check_ids", check_id)
        if not all(isinstance(item, SafetyCheckResult) for item in results):
            raise TypeError("results must contain only SafetyCheckResult values")
        if not set(missing).issubset(expected):
            _fail("missing_check_ids", "missing checks must be expected checks")
        if any(not isinstance(reason, str) or not reason for reason in reasons):
            _fail("blocking_reasons", "reasons must be non-empty strings")
        if self.status is SafetyGateStatus.READY_FOR_HUMAN_REVIEW and reasons:
            _fail("blocking_reasons", "ready state cannot contain blocking reasons")
        if self.status is not SafetyGateStatus.READY_FOR_HUMAN_REVIEW and not reasons:
            _fail("blocking_reasons", "non-ready state requires a reason")
        _text("trace_id", self.trace_id)
        object.__setattr__(self, "expected_check_ids", expected)
        object.__setattr__(self, "results", results)
        object.__setattr__(self, "missing_check_ids", missing)
        object.__setattr__(self, "blocking_reasons", reasons)

    @property
    def clinical_execution_allowed(self) -> bool:
        """Safety assessment never makes or authorizes a clinical decision."""

        return False


def _identifier(field_name: str, value: object) -> None:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        _fail(field_name, f"{field_name} must be canonical")


def _identifiers(field_name: str, values: object) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        _fail(field_name, f"{field_name} must be a collection")
    items = tuple(values)  # type: ignore[arg-type]
    if not items:
        _fail(field_name, f"{field_name} cannot be empty")
    for value in items:
        _identifier(field_name, value)
    if len(set(items)) != len(items):
        _fail(field_name, f"{field_name} must be unique")
    return items


def _text(field_name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        _fail(field_name, f"{field_name} cannot be empty")


def _fail(field_name: str, message: str) -> None:
    raise SafetyError(f"safety.{field_name}", message)
