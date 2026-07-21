"""Permission engine."""

from __future__ import annotations

from clinical_intelligence.models import ClinicalIntelligenceCapability, PermissionPolicy


class PermissionEngine:
    ALLOWED = ("Snapshot", "Timeline", "Evidence", "Knowledge", "Quality", "Simulation")

    def grant(self, capability: ClinicalIntelligenceCapability, requested: tuple[str, ...]) -> PermissionPolicy:
        granted = tuple(item for item in requested if item in self.ALLOWED)
        return PermissionPolicy(
            capability_id=capability.capability_id,
            requested=requested,
            granted=granted,
            default_access="read_only",
        )

