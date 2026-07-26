"""Declarative clinical-rule contracts with fail-closed governance.

The contracts describe auditable rule data. They do not authorize diagnosis,
prescription, treatment, or autonomous clinical execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
import re

from .clinical_modules import ClinicalModuleRegistry
from .models import KnowledgeError


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class ClinicalRuleOperator(str, Enum):
    EQUALS = "equals"
    CONTAINS = "contains"
    CONTAINS_ANY = "contains_any"
    CONTAINS_ALL = "contains_all"
    COUNT_AT_LEAST = "count_at_least"
    MATCHES = "matches"
    PRESENT = "present"


class ClinicalRuleEffect(str, Enum):
    SUPPORT = "support"
    OPPOSE = "oppose"
    ALARM = "alarm"
    ROUTE = "route"


class ClinicalRuleStrength(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class ClinicalRuleStatus(str, Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    VALIDATED = "validated"
    RETIRED = "retired"


@dataclass(frozen=True, slots=True)
class ClinicalRuleCondition:
    """A predicate or a recursive ``all``/``any``/``none`` group."""

    fact: str | None = None
    operator: ClinicalRuleOperator | None = None
    value: str | None = None
    values: tuple[str, ...] = ()
    threshold: int | None = None
    pattern: str | None = None
    all_of: tuple[ClinicalRuleCondition, ...] = ()
    any_of: tuple[ClinicalRuleCondition, ...] = ()
    none_of: tuple[ClinicalRuleCondition, ...] = ()

    def __post_init__(self) -> None:
        groups = tuple(self.all_of) + tuple(self.any_of) + tuple(self.none_of)
        is_group = bool(groups)
        if is_group:
            if any(
                value is not None
                for value in (
                    self.fact,
                    self.operator,
                    self.value,
                    self.threshold,
                    self.pattern,
                )
            ) or self.values:
                _fail("condition", "group cannot contain predicate fields")
            if any(
                not isinstance(item, ClinicalRuleCondition) for item in groups
            ):
                raise TypeError(
                    "rule groups must contain ClinicalRuleCondition values"
                )
            object.__setattr__(self, "all_of", tuple(self.all_of))
            object.__setattr__(self, "any_of", tuple(self.any_of))
            object.__setattr__(self, "none_of", tuple(self.none_of))
            return

        _identifier("condition.fact", self.fact)
        if not isinstance(self.operator, ClinicalRuleOperator):
            raise TypeError("condition operator must be a ClinicalRuleOperator")
        values = _unique_texts("condition.values", self.values)
        object.__setattr__(self, "values", values)
        if self.value is not None:
            _text("condition.value", self.value, 500)
        if self.pattern is not None:
            _text("condition.pattern", self.pattern, 500)
            try:
                re.compile(self.pattern)
            except re.error as exc:
                _fail("condition.pattern", "condition pattern is invalid")
                raise AssertionError from exc

        if self.operator is ClinicalRuleOperator.EQUALS:
            _require_only(self, require_value=True)
        elif self.operator is ClinicalRuleOperator.CONTAINS:
            _require_only(self, require_value=True)
        elif self.operator in (
            ClinicalRuleOperator.CONTAINS_ANY,
            ClinicalRuleOperator.CONTAINS_ALL,
        ):
            if not values:
                _fail("condition.values", "condition values cannot be empty")
            _require_only(self, allow_values=True)
        elif self.operator is ClinicalRuleOperator.COUNT_AT_LEAST:
            if not values:
                _fail("condition.values", "condition values cannot be empty")
            if (
                not isinstance(self.threshold, int)
                or isinstance(self.threshold, bool)
                or self.threshold < 1
                or self.threshold > len(values)
            ):
                _fail(
                    "condition.threshold",
                    "threshold must be between 1 and the value count",
                )
            _require_only(self, allow_values=True, allow_threshold=True)
        elif self.operator is ClinicalRuleOperator.MATCHES:
            if self.pattern is None:
                _fail("condition.pattern", "pattern is required")
            _require_only(self, allow_pattern=True)
        elif self.operator is ClinicalRuleOperator.PRESENT:
            _require_only(self)


@dataclass(frozen=True, slots=True)
class ClinicalRuleDefinition:
    rule_id: str
    module_id: str
    version: str
    effect: ClinicalRuleEffect
    strength: ClinicalRuleStrength
    rationale: str
    when: ClinicalRuleCondition
    output_key: str | None = None
    output_value: str | None = None
    priority: bool = False
    source_ids: tuple[str, ...] = ()
    status: ClinicalRuleStatus = ClinicalRuleStatus.DRAFT
    reviewed_on: date | None = None
    reviewed_by: str | None = None
    review_due_on: date | None = None

    def __post_init__(self) -> None:
        _identifier("rule_id", self.rule_id)
        _identifier("module_id", self.module_id)
        if not isinstance(self.version, str) or not _VERSION.fullmatch(self.version):
            _fail("version", "version must use semantic versioning")
        if not isinstance(self.effect, ClinicalRuleEffect):
            raise TypeError("effect must be a ClinicalRuleEffect")
        if not isinstance(self.strength, ClinicalRuleStrength):
            raise TypeError("strength must be a ClinicalRuleStrength")
        if not isinstance(self.status, ClinicalRuleStatus):
            raise TypeError("status must be a ClinicalRuleStatus")
        if not isinstance(self.when, ClinicalRuleCondition):
            raise TypeError("when must be a ClinicalRuleCondition")
        if not isinstance(self.priority, bool):
            raise TypeError("priority must be boolean")
        _text("rationale", self.rationale, 1000)
        source_ids = _unique_identifiers("source_ids", self.source_ids)
        object.__setattr__(self, "source_ids", source_ids)

        if self.effect is ClinicalRuleEffect.ROUTE:
            _identifier("output_key", self.output_key)
            if self.output_value is not None:
                _fail(
                    "output_value",
                    "output value is not valid for route effects",
                )
        else:
            if self.output_key is not None:
                _fail("output_key", "output key is only valid for route effects")
            _text("output_value", self.output_value, 1000)

        _review_metadata(
            self.status,
            source_ids,
            self.reviewed_on,
            self.reviewed_by,
            self.review_due_on,
        )

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


class ClinicalRuleRegistry:
    def __init__(
        self,
        modules: ClinicalModuleRegistry,
        rules: tuple[ClinicalRuleDefinition, ...]
        | list[ClinicalRuleDefinition] = (),
    ) -> None:
        if not isinstance(modules, ClinicalModuleRegistry):
            raise TypeError("modules must be a ClinicalModuleRegistry")
        self._items: dict[str, ClinicalRuleDefinition] = {}
        self._modules = modules
        for rule in rules:
            self.register(rule)

    def register(self, rule: ClinicalRuleDefinition) -> ClinicalRuleDefinition:
        if not isinstance(rule, ClinicalRuleDefinition):
            raise TypeError("rule must be a ClinicalRuleDefinition")
        if rule.rule_id in self._items:
            _fail("rule_id", f"duplicate rule id: {rule.rule_id}")
        self._modules.require(rule.module_id)
        self._items[rule.rule_id] = rule
        return rule

    def require(self, rule_id: str) -> ClinicalRuleDefinition:
        try:
            return self._items[rule_id]
        except KeyError as exc:
            raise KnowledgeError(
                "clinical_rule_registry.unknown",
                f"unknown clinical rule: {rule_id}",
            ) from exc

    def all(self) -> tuple[ClinicalRuleDefinition, ...]:
        return tuple(self._items.values())

    def for_module(self, module_id_or_legacy_key: str) -> tuple[ClinicalRuleDefinition, ...]:
        module = self._modules.require(module_id_or_legacy_key)
        return tuple(
            rule for rule in self._items.values() if rule.module_id == module.module_id
        )

    def counts_by_status(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for rule in self._items.values():
            key = rule.status.value
            counts[key] = counts.get(key, 0) + 1
        return dict(sorted(counts.items()))


def _require_only(
    condition: ClinicalRuleCondition,
    *,
    require_value: bool = False,
    allow_values: bool = False,
    allow_threshold: bool = False,
    allow_pattern: bool = False,
) -> None:
    if require_value and condition.value is None:
        _fail("condition.value", "condition value is required")
    if not require_value and condition.value is not None:
        _fail("condition.value", "condition value is not allowed")
    if not allow_values and condition.values:
        _fail("condition.values", "condition values are not allowed")
    if not allow_threshold and condition.threshold is not None:
        _fail("condition.threshold", "condition threshold is not allowed")
    if not allow_pattern and condition.pattern is not None:
        _fail("condition.pattern", "condition pattern is not allowed")


def _review_metadata(
    status: ClinicalRuleStatus,
    source_ids: tuple[str, ...],
    reviewed_on: date | None,
    reviewed_by: str | None,
    review_due_on: date | None,
) -> None:
    if reviewed_on is not None:
        if not isinstance(reviewed_on, date):
            raise TypeError("reviewed_on must be a date or None")
        if reviewed_on > date.today():
            _fail("reviewed_on", "review date cannot be in the future")
    if reviewed_by is not None:
        _identifier("reviewed_by", reviewed_by)
    if review_due_on is not None:
        if not isinstance(review_due_on, date):
            raise TypeError("review_due_on must be a date or None")
        if reviewed_on is None or review_due_on <= reviewed_on:
            _fail("review_due_on", "review due date must follow review date")
    if status is ClinicalRuleStatus.VALIDATED and (
        not source_ids
        or reviewed_on is None
        or reviewed_by is None
        or review_due_on is None
        or review_due_on <= date.today()
    ):
        _fail(
            "validation",
            "validated rule requires sources, reviewer metadata, "
            "and a future review date",
        )


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
    field_name: str, values: tuple[str, ...] | list[str]
) -> tuple[str, ...]:
    if not isinstance(values, (tuple, list)):
        raise TypeError(f"{field_name} must be a tuple or list")
    result = tuple(values)
    for value in result:
        _text(field_name, value, 500)
    if len(result) != len(set(result)):
        _fail(field_name, f"{field_name} values must be unique")
    return result


def _identifier(field_name: str, value: object) -> None:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        _fail(field_name, f"{field_name} must be canonical")


def _text(field_name: str, value: object, maximum: int) -> None:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        _fail(field_name, f"{field_name} must contain 1 to {maximum} characters")


def _fail(field_name: str, message: str) -> None:
    raise KnowledgeError(f"clinical_rule.{field_name}", message)
