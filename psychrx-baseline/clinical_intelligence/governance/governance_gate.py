"""Governance gate."""

from __future__ import annotations

from clinical_intelligence.models import GovernanceDecision, PermissionPolicy


class GovernanceGate:
    FORBIDDEN = (
        "modify_production_state",
        "bypass_safety",
        "bypass_scientific_validation",
        "bypass_knowledge_governance",
        "bypass_quality_engine",
        "autonomous_clinical_decision",
        "prescription",
    )

    def evaluate(self, requested_actions: tuple[str, ...], permission: PermissionPolicy) -> GovernanceDecision:
        for action in requested_actions:
            if action in self.FORBIDDEN:
                return GovernanceDecision("rejected", f"forbidden_action:{action}", False)
        if permission.default_access != "read_only":
            return GovernanceDecision("rejected", "non_read_only_permission", False)
        return GovernanceDecision("approved_read_only", "governance_constraints_satisfied", True)

