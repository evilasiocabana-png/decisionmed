"""Capability validator."""

from __future__ import annotations

from clinical_intelligence.models import ClinicalIntelligenceCapability, IntelligenceContract, PermissionPolicy


class CapabilityValidator:
    def validate(
        self,
        capability: ClinicalIntelligenceCapability,
        contract: IntelligenceContract | None,
        permission: PermissionPolicy | None,
    ) -> tuple[str, ...]:
        issues = []
        if contract is None:
            issues.append("missing_contract")
        if permission is None:
            issues.append("missing_permissions")
        if "Clinical Operating Mind" not in capability.dependencies:
            issues.append("missing_operating_mind_dependency")
        return tuple(issues)

