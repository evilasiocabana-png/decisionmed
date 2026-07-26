"""Governed identities for DecisionMEd clinical reasoning modules.

This layer catalogs terminology and relationships. It does not execute clinical
rules, diagnose, recommend care, or authorize clinical runtime use.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
import re
import unicodedata

from .models import KnowledgeError


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class ClinicalEntityType(str, Enum):
    MANIFESTATION = "manifestation"
    CLINICAL_PRESENTATION = "clinical_presentation"
    INITIAL_SYNDROME = "initial_syndrome"
    STANDARDIZED_SYNDROME = "standardized_syndrome"
    DIAGNOSIS = "diagnosis"
    RISK_CONDITION = "risk_condition"
    CLINICAL_CONTEXT = "clinical_context"


class ClinicalModuleStatus(str, Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    VALIDATED = "validated"
    RETIRED = "retired"


class TerminologyStatus(str, Enum):
    CANDIDATE = "candidate"
    REVIEWED = "reviewed"
    OFFICIAL = "official"


class ClinicalContentStatus(str, Enum):
    SKELETON = "skeleton"
    PARTIAL = "partial"
    COMPLETE = "complete"


@dataclass(frozen=True, slots=True)
class TerminologyCode:
    system: str
    code: str
    display: str
    version: str | None = None

    def __post_init__(self) -> None:
        _text("system", self.system, 100)
        _text("code", self.code, 200)
        _text("display", self.display, 500)
        if self.version is not None:
            _text("version", self.version, 100)


@dataclass(frozen=True, slots=True)
class ClinicalModuleDefinition:
    module_id: str
    version: str
    official_name: str
    display_name: str
    entity_type: ClinicalEntityType
    primary_specialty: str
    synonyms: tuple[str, ...] = ()
    abbreviations: tuple[str, ...] = ()
    related_specialties: tuple[str, ...] = ()
    parent_module_id: str | None = None
    related_module_ids: tuple[str, ...] = ()
    terminology_codes: tuple[TerminologyCode, ...] = ()
    populations: tuple[str, ...] = ()
    care_settings: tuple[str, ...] = ()
    source_ids: tuple[str, ...] = ()
    legacy_keys: tuple[str, ...] = ()
    terminology_status: TerminologyStatus = TerminologyStatus.CANDIDATE
    content_status: ClinicalContentStatus = ClinicalContentStatus.SKELETON
    status: ClinicalModuleStatus = ClinicalModuleStatus.DRAFT
    reviewed_on: date | None = None
    reviewed_by: str | None = None
    review_due_on: date | None = None

    def __post_init__(self) -> None:
        _identifier("module_id", self.module_id)
        if not isinstance(self.version, str) or not _VERSION.fullmatch(self.version):
            _fail("version", "version must use semantic versioning")
        _text("official_name", self.official_name, 500)
        _text("display_name", self.display_name, 500)
        if not isinstance(self.entity_type, ClinicalEntityType):
            raise TypeError("entity_type must be a ClinicalEntityType")
        _identifier("primary_specialty", self.primary_specialty)
        if not isinstance(self.terminology_status, TerminologyStatus):
            raise TypeError("terminology_status must be a TerminologyStatus")
        if not isinstance(self.content_status, ClinicalContentStatus):
            raise TypeError("content_status must be a ClinicalContentStatus")
        if not isinstance(self.status, ClinicalModuleStatus):
            raise TypeError("status must be a ClinicalModuleStatus")

        for field_name, values, identifiers in (
            ("synonyms", self.synonyms, False),
            ("abbreviations", self.abbreviations, False),
            ("related_specialties", self.related_specialties, True),
            ("related_module_ids", self.related_module_ids, True),
            ("populations", self.populations, False),
            ("care_settings", self.care_settings, False),
            ("source_ids", self.source_ids, True),
            ("legacy_keys", self.legacy_keys, True),
        ):
            normalized = _unique_tuple(field_name, values, identifiers)
            object.__setattr__(self, field_name, normalized)

        codes = tuple(self.terminology_codes)
        if any(not isinstance(value, TerminologyCode) for value in codes):
            raise TypeError("terminology_codes must contain TerminologyCode values")
        if len({(value.system, value.code) for value in codes}) != len(codes):
            _fail("terminology_codes", "terminology codes must be unique")
        object.__setattr__(self, "terminology_codes", codes)

        if self.parent_module_id is not None:
            _identifier("parent_module_id", self.parent_module_id)
            if self.parent_module_id == self.module_id:
                _fail("parent_module_id", "a module cannot be its own parent")
        if self.module_id in self.related_module_ids:
            _fail("related_module_ids", "a module cannot relate to itself")
        if self.primary_specialty in self.related_specialties:
            _fail(
                "related_specialties",
                "primary specialty must not be repeated as related",
            )

        _review_metadata(
            self.status,
            self.terminology_status,
            self.content_status,
            self.source_ids,
            self.reviewed_on,
            self.reviewed_by,
            self.review_due_on,
        )

    @property
    def clinical_execution_allowed(self) -> bool:
        """Catalog identity alone never authorizes clinical execution."""

        return False


class ClinicalModuleRegistry:
    """Deterministic registry with identity, alias, and relationship checks."""

    def __init__(
        self, modules: tuple[ClinicalModuleDefinition, ...] | list[ClinicalModuleDefinition] = ()
    ) -> None:
        self._items: dict[str, ClinicalModuleDefinition] = {}
        self._names: dict[str, str] = {}
        self._legacy_keys: dict[str, str] = {}
        for module in modules:
            self.register(module)
        self.validate_relationships()

    def register(self, module: ClinicalModuleDefinition) -> ClinicalModuleDefinition:
        if not isinstance(module, ClinicalModuleDefinition):
            raise TypeError("module must be a ClinicalModuleDefinition")
        if module.module_id in self._items:
            _fail("module_id", f"duplicate module id: {module.module_id}")
        normalized_name = _normalized_name(module.official_name)
        if normalized_name in self._names:
            _fail(
                "official_name",
                "duplicate official name: "
                f"{module.official_name} ({self._names[normalized_name]})",
            )
        for legacy_key in module.legacy_keys:
            if legacy_key in self._legacy_keys:
                _fail("legacy_keys", f"duplicate legacy key: {legacy_key}")
        self._items[module.module_id] = module
        self._names[normalized_name] = module.module_id
        for legacy_key in module.legacy_keys:
            self._legacy_keys[legacy_key] = module.module_id
        return module

    def validate_relationships(self) -> None:
        for module in self._items.values():
            references = (
                (() if module.parent_module_id is None else (module.parent_module_id,))
                + module.related_module_ids
            )
            missing = tuple(
                module_id for module_id in references if module_id not in self._items
            )
            if missing:
                _fail(
                    "relationships",
                    f"{module.module_id} references missing modules: {', '.join(missing)}",
                )

    def require(self, module_id_or_legacy_key: str) -> ClinicalModuleDefinition:
        module_id = self._legacy_keys.get(module_id_or_legacy_key, module_id_or_legacy_key)
        try:
            return self._items[module_id]
        except KeyError as exc:
            raise KnowledgeError(
                "clinical_module_registry.unknown",
                f"unknown clinical module: {module_id_or_legacy_key}",
            ) from exc

    def all(self) -> tuple[ClinicalModuleDefinition, ...]:
        return tuple(self._items.values())

    def by_specialty(self, specialty_key: str) -> tuple[ClinicalModuleDefinition, ...]:
        return tuple(
            module
            for module in self._items.values()
            if module.primary_specialty == specialty_key
        )

    def counts_by_specialty(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for module in self._items.values():
            counts[module.primary_specialty] = counts.get(module.primary_specialty, 0) + 1
        return dict(sorted(counts.items()))

    def counts_by_entity_type(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for module in self._items.values():
            key = module.entity_type.value
            counts[key] = counts.get(key, 0) + 1
        return dict(sorted(counts.items()))

    def counts_by_status(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for module in self._items.values():
            key = module.status.value
            counts[key] = counts.get(key, 0) + 1
        return dict(sorted(counts.items()))


def _review_metadata(
    status: ClinicalModuleStatus,
    terminology_status: TerminologyStatus,
    content_status: ClinicalContentStatus,
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
    if status is ClinicalModuleStatus.VALIDATED:
        if (
            terminology_status is not TerminologyStatus.OFFICIAL
            or content_status is not ClinicalContentStatus.COMPLETE
            or not source_ids
            or reviewed_on is None
            or reviewed_by is None
            or review_due_on is None
            or review_due_on <= date.today()
        ):
            _fail(
                "validation",
                "validated module requires official terminology, complete content, "
                "sources, reviewer metadata, and a future review date",
            )


def _unique_tuple(
    field_name: str, values: tuple[str, ...], identifiers: bool
) -> tuple[str, ...]:
    if not isinstance(values, (tuple, list)):
        raise TypeError(f"{field_name} must be a tuple or list")
    result = tuple(values)
    for value in result:
        if identifiers:
            _identifier(field_name, value)
        else:
            _text(field_name, value, 500)
    if len(set(result)) != len(result):
        _fail(field_name, f"{field_name} values must be unique")
    return result


def _normalized_name(value: str) -> str:
    return "".join(
        character
        for character in unicodedata.normalize("NFD", value.casefold())
        if unicodedata.category(character) != "Mn"
    ).strip()


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
    raise KnowledgeError(f"clinical_module.{field_name}", message)
