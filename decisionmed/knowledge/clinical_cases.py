"""Deterministic, auditable test-case contracts for DM-300.

These records exercise catalog structure and reasoning traces. They are
synthetic quality-assurance fixtures, never patient records and never
authorization for clinical execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
import re

from .clinical_modules import ClinicalModuleRegistry
from .models import KnowledgeError


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_HASH = re.compile(r"^[0-9a-f]{64}$")


class ClinicalCaseCategory(str, Enum):
    TYPICAL = "typical"
    ATYPICAL = "atypical"
    RED_FLAG = "red_flag"
    MIMIC = "mimic"
    COMORBIDITY = "comorbidity"
    CONTRADICTORY = "contradictory"
    POST_EXAM = "post_exam"


EXPECTED_CATEGORY_COUNTS = {
    ClinicalCaseCategory.TYPICAL: 3,
    ClinicalCaseCategory.ATYPICAL: 2,
    ClinicalCaseCategory.RED_FLAG: 2,
    ClinicalCaseCategory.MIMIC: 2,
    ClinicalCaseCategory.COMORBIDITY: 2,
    ClinicalCaseCategory.CONTRADICTORY: 2,
    ClinicalCaseCategory.POST_EXAM: 2,
}


@dataclass(frozen=True, slots=True)
class ClinicalCaseAnswer:
    fact_id: str
    values: tuple[str, ...]
    detail: str | None = None

    def __post_init__(self) -> None:
        _identifier("fact_id", self.fact_id)
        object.__setattr__(
            self,
            "values",
            _unique_texts("values", self.values, required=True),
        )
        if self.detail is not None:
            _text("detail", self.detail, 2000)


@dataclass(frozen=True, slots=True)
class ClinicalCaseAuditEvent:
    sequence: int
    event_type: str
    payload: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.sequence, int)
            or isinstance(self.sequence, bool)
            or self.sequence < 1
        ):
            _fail("sequence", "sequence must be a positive integer")
        _identifier("event_type", self.event_type)
        _text("payload", self.payload, 8000)
        try:
            parsed = json.loads(self.payload)
        except json.JSONDecodeError as exc:
            _fail("payload", "payload must be canonical JSON")
            raise AssertionError from exc
        canonical = json.dumps(
            parsed,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        if canonical != self.payload:
            _fail("payload", "payload must use canonical JSON serialization")


@dataclass(frozen=True, slots=True)
class ClinicalTestCase:
    case_id: str
    module_id: str
    ordinal: int
    category: ClinicalCaseCategory
    narrative: str
    selected_answers: tuple[ClinicalCaseAnswer, ...]
    positive_details: tuple[str, ...]
    expected_route_module_ids: tuple[str, ...]
    obtained_route_module_ids: tuple[str, ...]
    opened_question_ids: tuple[str, ...]
    initial_classification: str
    differentials: tuple[str, ...]
    physical_examination: tuple[str, ...]
    complementary_exams: tuple[str, ...]
    post_exam_result: str | None
    expected_impression: str
    audit_events: tuple[ClinicalCaseAuditEvent, ...]
    audit_hash: str

    def __post_init__(self) -> None:
        _identifier("case_id", self.case_id)
        _identifier("module_id", self.module_id)
        if (
            not isinstance(self.ordinal, int)
            or isinstance(self.ordinal, bool)
            or self.ordinal < 1
            or self.ordinal > 15
        ):
            _fail("ordinal", "ordinal must be between 1 and 15")
        if not isinstance(self.category, ClinicalCaseCategory):
            raise TypeError("category must be a ClinicalCaseCategory")
        _text("narrative", self.narrative, 8000)
        _text("initial_classification", self.initial_classification, 2000)
        _text("expected_impression", self.expected_impression, 2000)
        if self.post_exam_result is not None:
            _text("post_exam_result", self.post_exam_result, 4000)

        answers = tuple(self.selected_answers)
        if not answers or any(
            not isinstance(item, ClinicalCaseAnswer) for item in answers
        ):
            _fail("selected_answers", "at least one structured answer is required")
        if len({item.fact_id for item in answers}) != len(answers):
            _fail("selected_answers", "fact ids must be unique")
        object.__setattr__(self, "selected_answers", answers)

        events = tuple(self.audit_events)
        if not events or any(
            not isinstance(item, ClinicalCaseAuditEvent) for item in events
        ):
            _fail("audit_events", "at least one audit event is required")
        if tuple(item.sequence for item in events) != tuple(
            range(1, len(events) + 1)
        ):
            _fail("audit_events", "event sequence must be contiguous")
        object.__setattr__(self, "audit_events", events)

        for field_name in (
            "positive_details",
            "expected_route_module_ids",
            "obtained_route_module_ids",
            "opened_question_ids",
            "differentials",
            "physical_examination",
            "complementary_exams",
        ):
            values = getattr(self, field_name)
            if field_name.endswith("_ids"):
                normalized = _unique_identifiers(field_name, values)
            else:
                normalized = _unique_texts(field_name, values)
            object.__setattr__(self, field_name, normalized)
        if not self.expected_route_module_ids:
            _fail(
                "expected_route_module_ids",
                "at least one expected route is required",
            )
        if self.expected_route_module_ids != self.obtained_route_module_ids:
            _fail("route", "obtained routes must match deterministic expectations")
        if not isinstance(self.audit_hash, str) or not _HASH.fullmatch(
            self.audit_hash
        ):
            _fail("audit_hash", "audit hash must be SHA-256")
        if self.audit_hash != audit_hash_for(events):
            _fail("audit_hash", "audit hash does not match audit events")

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


class ClinicalCaseRegistry:
    def __init__(
        self,
        modules: ClinicalModuleRegistry,
        cases: tuple[ClinicalTestCase, ...] | list[ClinicalTestCase] = (),
    ) -> None:
        if not isinstance(modules, ClinicalModuleRegistry):
            raise TypeError("modules must be a ClinicalModuleRegistry")
        self._modules = modules
        self._items: dict[str, ClinicalTestCase] = {}
        self._by_module: dict[str, list[ClinicalTestCase]] = {}
        for case in cases:
            self.register(case)

    def register(self, case: ClinicalTestCase) -> ClinicalTestCase:
        if not isinstance(case, ClinicalTestCase):
            raise TypeError("case must be a ClinicalTestCase")
        if case.case_id in self._items:
            _fail("case_id", f"duplicate case: {case.case_id}")
        self._modules.require(case.module_id)
        self._items[case.case_id] = case
        self._by_module.setdefault(case.module_id, []).append(case)
        return case

    def require(self, case_id: str) -> ClinicalTestCase:
        try:
            return self._items[case_id]
        except KeyError as exc:
            raise KnowledgeError(
                "clinical_case_registry.unknown",
                f"unknown clinical case: {case_id}",
            ) from exc

    def all(self) -> tuple[ClinicalTestCase, ...]:
        return tuple(self._items.values())

    def for_module(
        self, module_id_or_legacy_key: str
    ) -> tuple[ClinicalTestCase, ...]:
        module = self._modules.require(module_id_or_legacy_key)
        return tuple(self._by_module.get(module.module_id, ()))

    def validate_dm300_distribution(self) -> None:
        modules = self._modules.all()
        if len(modules) != 300 or len(self._items) != 4500:
            _fail("distribution", "DM-300 requires 300 modules and 4,500 cases")
        for module in modules:
            cases = self.for_module(module.module_id)
            if len(cases) != 15:
                _fail(
                    "distribution",
                    f"{module.module_id} must contain exactly 15 cases",
                )
            if {case.ordinal for case in cases} != set(range(1, 16)):
                _fail(
                    "distribution",
                    f"{module.module_id} ordinals must cover 1 through 15",
                )
            counts = {
                category: sum(case.category is category for case in cases)
                for category in ClinicalCaseCategory
            }
            if counts != EXPECTED_CATEGORY_COUNTS:
                _fail(
                    "distribution",
                    f"{module.module_id} has an invalid category distribution",
                )


def audit_hash_for(events: tuple[ClinicalCaseAuditEvent, ...]) -> str:
    canonical = json.dumps(
        [
            {
                "sequence": item.sequence,
                "event_type": item.event_type,
                "payload": item.payload,
            }
            for item in events
        ],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return sha256(canonical.encode("utf-8")).hexdigest()


def _unique_identifiers(
    field_name: str, values: tuple[str, ...] | list[str]
) -> tuple[str, ...]:
    if not isinstance(values, (tuple, list)):
        raise TypeError(f"{field_name} must be a tuple or list")
    result = tuple(values)
    for value in result:
        _identifier(field_name, value)
    if len(result) != len(set(result)):
        _fail(field_name, f"{field_name} values must be unique")
    return result


def _unique_texts(
    field_name: str,
    values: tuple[str, ...] | list[str],
    *,
    required: bool = False,
) -> tuple[str, ...]:
    if not isinstance(values, (tuple, list)):
        raise TypeError(f"{field_name} must be a tuple or list")
    result = tuple(values)
    if required and not result:
        _fail(field_name, f"{field_name} cannot be empty")
    for value in result:
        _text(field_name, value, 8000)
    if len(result) != len(set(result)):
        _fail(field_name, f"{field_name} values must be unique")
    return result


def _identifier(field_name: str, value: object) -> None:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        _fail(field_name, f"{field_name} must be canonical")


def _text(field_name: str, value: object, maximum: int) -> None:
    if (
        not isinstance(value, str)
        or not value.strip()
        or len(value) > maximum
    ):
        _fail(field_name, f"{field_name} must contain 1 to {maximum} characters")


def _fail(field_name: str, message: str) -> None:
    raise KnowledgeError(f"clinical_case.{field_name}", message)
