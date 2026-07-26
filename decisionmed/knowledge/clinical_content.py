"""Governed content records for clinical reasoning modules.

Draft content may be displayed for prototyping and review, but this contract
never authorizes automated diagnosis, prescription, or treatment.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import re

from .clinical_modules import (
    ClinicalContentStatus,
    ClinicalModuleRegistry,
    ClinicalModuleStatus,
)
from .models import KnowledgeError


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


@dataclass(frozen=True, slots=True)
class ClinicalDiscriminator:
    question_id: str
    text: str
    options: tuple[str, ...]
    rationale: str | None = None
    detail_on_positive: bool = False
    detail_required: bool = False
    source_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _identifier("question_id", self.question_id)
        _text("text", self.text, 1000)
        options = _unique_texts("options", self.options, required=True)
        object.__setattr__(self, "options", options)
        if self.rationale is not None:
            _text("rationale", self.rationale, 1000)
        if not isinstance(self.detail_on_positive, bool):
            raise TypeError("detail_on_positive must be boolean")
        if not isinstance(self.detail_required, bool):
            raise TypeError("detail_required must be boolean")
        object.__setattr__(
            self,
            "source_ids",
            _unique_identifiers("source_ids", self.source_ids),
        )


@dataclass(frozen=True, slots=True)
class ClinicalComplementaryExam:
    exam_id: str
    name: str
    clinical_question: str
    when: str
    limitations: str | None = None
    source_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _identifier("exam_id", self.exam_id)
        _text("name", self.name, 500)
        _text("clinical_question", self.clinical_question, 2000)
        _text("when", self.when, 2000)
        if self.limitations is not None:
            _text("limitations", self.limitations, 2000)
        object.__setattr__(
            self,
            "source_ids",
            _unique_identifiers("source_ids", self.source_ids),
        )


@dataclass(frozen=True, slots=True)
class ClinicalModuleContent:
    module_id: str
    version: str
    definition: str | None
    boundaries: str | None
    anchor_values: tuple[str, ...]
    required_manifestations: tuple[str, ...]
    frequent_manifestations: tuple[str, ...]
    atypical_manifestations: tuple[str, ...]
    contrary_findings: tuple[str, ...]
    risk_factors: tuple[str, ...]
    red_flags: tuple[str, ...]
    stop_conditions: tuple[str, ...]
    likely_hypotheses: tuple[str, ...]
    cannot_miss_hypotheses: tuple[str, ...]
    mimics: tuple[str, ...]
    discriminators: tuple[ClinicalDiscriminator, ...]
    physical_examination: tuple[str, ...]
    complementary_exams: tuple[ClinicalComplementaryExam, ...]
    diagnostic_criteria: tuple[str, ...]
    post_exam_reassessment: tuple[str, ...]
    safety_conduct: tuple[str, ...]
    initial_treatment: tuple[str, ...]
    definitive_treatment: tuple[str, ...]
    destination_return_followup: tuple[str, ...]
    source_ids: tuple[str, ...]
    content_status: ClinicalContentStatus
    status: ClinicalModuleStatus
    reviewed_on: date | None = None
    reviewed_by: str | None = None
    review_due_on: date | None = None

    def __post_init__(self) -> None:
        _identifier("module_id", self.module_id)
        if not isinstance(self.version, str) or not _VERSION.fullmatch(self.version):
            _fail("version", "version must use semantic versioning")
        if self.definition is not None:
            _text("definition", self.definition, 4000)
        if self.boundaries is not None:
            _text("boundaries", self.boundaries, 4000)
        if not isinstance(self.content_status, ClinicalContentStatus):
            raise TypeError("content_status must be a ClinicalContentStatus")
        if not isinstance(self.status, ClinicalModuleStatus):
            raise TypeError("status must be a ClinicalModuleStatus")

        for field_name in (
            "anchor_values",
            "required_manifestations",
            "frequent_manifestations",
            "atypical_manifestations",
            "contrary_findings",
            "risk_factors",
            "red_flags",
            "stop_conditions",
            "likely_hypotheses",
            "cannot_miss_hypotheses",
            "mimics",
            "physical_examination",
            "diagnostic_criteria",
            "post_exam_reassessment",
            "safety_conduct",
            "initial_treatment",
            "definitive_treatment",
            "destination_return_followup",
        ):
            object.__setattr__(
                self,
                field_name,
                _unique_texts(field_name, getattr(self, field_name)),
            )
        object.__setattr__(
            self,
            "source_ids",
            _unique_identifiers("source_ids", self.source_ids),
        )

        discriminators = tuple(self.discriminators)
        if any(
            not isinstance(item, ClinicalDiscriminator)
            for item in discriminators
        ):
            raise TypeError(
                "discriminators must contain ClinicalDiscriminator values"
            )
        if len({item.question_id for item in discriminators}) != len(
            discriminators
        ):
            _fail("discriminators", "question ids must be unique")
        object.__setattr__(self, "discriminators", discriminators)

        exams = tuple(self.complementary_exams)
        if any(
            not isinstance(item, ClinicalComplementaryExam) for item in exams
        ):
            raise TypeError(
                "complementary_exams must contain ClinicalComplementaryExam values"
            )
        if len({item.exam_id for item in exams}) != len(exams):
            _fail("complementary_exams", "exam ids must be unique")
        object.__setattr__(self, "complementary_exams", exams)

        _validate_review(self)
        if self.content_status is ClinicalContentStatus.COMPLETE:
            required_sections = {
                "definition": self.definition,
                "boundaries": self.boundaries,
                "anchor_values": self.anchor_values,
                "red_flags": self.red_flags,
                "stop_conditions": self.stop_conditions,
                "likely_hypotheses": self.likely_hypotheses,
                "cannot_miss_hypotheses": self.cannot_miss_hypotheses,
                "mimics": self.mimics,
                "discriminators": self.discriminators,
                "physical_examination": self.physical_examination,
                "complementary_exams": self.complementary_exams,
                "post_exam_reassessment": self.post_exam_reassessment,
                "safety_conduct": self.safety_conduct,
                "destination_return_followup": self.destination_return_followup,
            }
            missing = tuple(
                name for name, value in required_sections.items() if not value
            )
            if missing:
                _fail(
                    "completeness",
                    f"complete content is missing: {', '.join(missing)}",
                )

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


class ClinicalModuleContentRegistry:
    def __init__(
        self,
        modules: ClinicalModuleRegistry,
        contents: tuple[ClinicalModuleContent, ...]
        | list[ClinicalModuleContent] = (),
    ) -> None:
        if not isinstance(modules, ClinicalModuleRegistry):
            raise TypeError("modules must be a ClinicalModuleRegistry")
        self._modules = modules
        self._items: dict[str, ClinicalModuleContent] = {}
        for content in contents:
            self.register(content)

    def register(self, content: ClinicalModuleContent) -> ClinicalModuleContent:
        if not isinstance(content, ClinicalModuleContent):
            raise TypeError("content must be ClinicalModuleContent")
        if content.module_id in self._items:
            _fail("module_id", f"duplicate content: {content.module_id}")
        self._modules.require(content.module_id)
        self._items[content.module_id] = content
        return content

    def require(self, module_id_or_legacy_key: str) -> ClinicalModuleContent:
        module = self._modules.require(module_id_or_legacy_key)
        try:
            return self._items[module.module_id]
        except KeyError as exc:
            raise KnowledgeError(
                "clinical_content_registry.unknown",
                f"unknown clinical module content: {module_id_or_legacy_key}",
            ) from exc

    def all(self) -> tuple[ClinicalModuleContent, ...]:
        return tuple(self._items.values())

    def counts_by_content_status(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for content in self._items.values():
            key = content.content_status.value
            counts[key] = counts.get(key, 0) + 1
        return dict(sorted(counts.items()))


def _validate_review(content: ClinicalModuleContent) -> None:
    if content.reviewed_on is not None:
        if not isinstance(content.reviewed_on, date):
            raise TypeError("reviewed_on must be a date or None")
        if content.reviewed_on > date.today():
            _fail("reviewed_on", "review date cannot be in the future")
    if content.reviewed_by is not None:
        _identifier("reviewed_by", content.reviewed_by)
    if content.review_due_on is not None:
        if not isinstance(content.review_due_on, date):
            raise TypeError("review_due_on must be a date or None")
        if (
            content.reviewed_on is None
            or content.review_due_on <= content.reviewed_on
        ):
            _fail("review_due_on", "review due date must follow review date")
    if content.status is ClinicalModuleStatus.VALIDATED and (
        content.content_status is not ClinicalContentStatus.COMPLETE
        or not content.source_ids
        or content.reviewed_on is None
        or content.reviewed_by is None
        or content.review_due_on is None
        or content.review_due_on <= date.today()
    ):
        _fail(
            "validation",
            "validated content requires complete sections, sources, reviewer "
            "metadata, and a future review date",
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
        _text(field_name, value, 4000)
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
    raise KnowledgeError(f"clinical_content.{field_name}", message)
