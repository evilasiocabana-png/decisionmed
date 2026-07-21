"""Contract validator."""

from __future__ import annotations

from clinical_intelligence.models import IntelligenceContract


class ContractValidator:
    def validate(self, contract: IntelligenceContract) -> tuple[str, ...]:
        issues = []
        if not contract.inputs:
            issues.append("missing_inputs")
        if not contract.outputs:
            issues.append("missing_outputs")
        if not contract.immutable:
            issues.append("mutable_contract")
        if not contract.trace_required:
            issues.append("trace_not_required")
        return tuple(issues)

