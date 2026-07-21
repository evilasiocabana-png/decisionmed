"""Capability registry."""

from __future__ import annotations

from clinical_intelligence.models import ClinicalIntelligenceCapability


class CapabilityRegistry:
    def __init__(self) -> None:
        self._capabilities: dict[str, ClinicalIntelligenceCapability] = {}

    def register(self, capability: ClinicalIntelligenceCapability) -> ClinicalIntelligenceCapability:
        self._capabilities[capability.capability_id] = capability
        return capability

    def all(self) -> tuple[ClinicalIntelligenceCapability, ...]:
        return tuple(self._capabilities.values())

