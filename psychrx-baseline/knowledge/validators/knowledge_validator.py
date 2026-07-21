"""Structural validation for knowledge objects."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from knowledge.core.knowledge_object import KnowledgeObject
from knowledge.core.status import KnowledgeStatus


class ValidationSeverity(StrEnum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class ValidationIssue:
    field: str
    message: str
    severity: ValidationSeverity = ValidationSeverity.ERROR


@dataclass(frozen=True)
class ValidationResult:
    issues: tuple[ValidationIssue, ...] = ()

    @property
    def is_valid(self) -> bool:
        return all(issue.severity != ValidationSeverity.ERROR for issue in self.issues)


class KnowledgeValidator:
    """Validate structural requirements before knowledge enters the platform."""

    def validate(self, knowledge_object: KnowledgeObject) -> ValidationResult:
        issues: list[ValidationIssue] = []

        if not knowledge_object.identifier.strip():
            issues.append(ValidationIssue("identifier", "identifier is required"))
        if not knowledge_object.name.strip():
            issues.append(ValidationIssue("name", "name is required"))
        if not knowledge_object.origin.strip():
            issues.append(ValidationIssue("origin", "origin is required"))
        if knowledge_object.status == KnowledgeStatus.VALIDATED and not knowledge_object.references:
            issues.append(
                ValidationIssue(
                    "references",
                    "validated knowledge requires at least one traceable reference",
                )
            )

        return ValidationResult(tuple(issues))
