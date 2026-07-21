"""Output validator."""

from __future__ import annotations


class OutputValidator:
    def validate(self, trace: str, references: tuple[str, ...], contracts: tuple[str, ...], quality_status: str) -> tuple[str, ...]:
        issues = []
        if not trace:
            issues.append("missing_trace")
        if not references:
            issues.append("missing_references")
        if not contracts:
            issues.append("missing_contracts")
        if not quality_status:
            issues.append("missing_quality_status")
        return tuple(issues)

