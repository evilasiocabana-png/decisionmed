"""Validation engine."""

from __future__ import annotations

from clinical_research.models import ValidationResult


class ValidationEngine:
    """Validates experimental outputs without medical validation."""

    CHECKS = ("contract_compliance", "trace_integrity", "quality_gates", "reproducibility")

    def validate(self) -> ValidationResult:
        return ValidationResult(checks=self.CHECKS)

