"""Read-only intelligence replay."""

from __future__ import annotations

from clinical_intelligence.models import ClinicalIntelligenceResult


class IntelligenceReplay:
    def replay(self, result: ClinicalIntelligenceResult) -> ClinicalIntelligenceResult:
        return result

