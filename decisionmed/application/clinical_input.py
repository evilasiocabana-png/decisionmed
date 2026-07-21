"""Structural validation for governed form payloads; no clinical interpretation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import math
import re

from decisionmed.knowledge import (
    ClinicalFieldDefinition,
    ClinicalFieldValueType,
    SpecialtyFormSchemaRegistry,
)


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")


@dataclass(frozen=True, slots=True)
class ClinicalInputIssue:
    field_key: str
    code: str


@dataclass(frozen=True, slots=True)
class ClinicalInputValidation:
    schema_id: str
    workflow_id: str
    step_key: str
    schema_version: str
    schema_status: str
    accepted_field_count: int
    issues: tuple[ClinicalInputIssue, ...]

    @property
    def structurally_valid(self) -> bool:
        return not self.issues

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


class ClinicalInputStructureValidator:
    """Check payload shape for QA without retaining values or making decisions."""

    def __init__(self, schemas: SpecialtyFormSchemaRegistry) -> None:
        if not isinstance(schemas, SpecialtyFormSchemaRegistry):
            raise TypeError("schemas must be a SpecialtyFormSchemaRegistry")
        self._schemas = schemas

    def validate(
        self,
        specialty_key: str,
        workflow_id: str,
        step_key: str,
        values: Mapping[str, object],
    ) -> ClinicalInputValidation:
        if not isinstance(values, Mapping):
            raise TypeError("values must be a mapping")
        schema = self._schemas.require(specialty_key, workflow_id, step_key)
        payload = dict(values)
        fields = {field.field_key: field for field in schema.fields}
        issues: list[ClinicalInputIssue] = []
        accepted = 0

        for key in payload:
            if not isinstance(key, str):
                issues.append(ClinicalInputIssue("_payload", "invalid_field_key"))
            elif key not in fields:
                safe_key = key if _IDENTIFIER.fullmatch(key) else "_unknown"
                issues.append(ClinicalInputIssue(safe_key, "unknown_field"))

        for field in schema.fields:
            if field.field_key not in payload:
                if field.required:
                    issues.append(ClinicalInputIssue(field.field_key, "required"))
                continue
            if _value_is_valid(field, payload[field.field_key]):
                accepted += 1
            else:
                issues.append(ClinicalInputIssue(field.field_key, "invalid_value"))

        return ClinicalInputValidation(
            schema_id=schema.schema_id,
            workflow_id=schema.workflow_id,
            step_key=schema.step_key,
            schema_version=schema.version,
            schema_status=schema.status.value,
            accepted_field_count=accepted,
            issues=tuple(sorted(issues, key=lambda item: (item.field_key, item.code))),
        )


def _value_is_valid(field: ClinicalFieldDefinition, value: object) -> bool:
    if field.value_type is ClinicalFieldValueType.BOOLEAN:
        return isinstance(value, bool)
    if field.value_type is ClinicalFieldValueType.INTEGER:
        return isinstance(value, int) and not isinstance(value, bool)
    if field.value_type is ClinicalFieldValueType.DECIMAL:
        if isinstance(value, bool):
            return False
        if isinstance(value, int):
            return True
        return isinstance(value, float) and math.isfinite(value)
    if field.value_type is ClinicalFieldValueType.TEXT:
        return isinstance(value, str) and bool(value.strip()) and len(value) <= 2000
    if field.value_type is ClinicalFieldValueType.CODED_CHOICE:
        return isinstance(value, str) and value in field.allowed_values
    return False
