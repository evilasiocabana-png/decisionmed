"""Deterministic read-only quality replay."""

from __future__ import annotations

from clinical_quality.models import ClinicalQualityResult


class QualityReplay:
    def replay(self, result: ClinicalQualityResult) -> ClinicalQualityResult:
        return result

