"""Runtime adapter for Clinical Operating Mind."""

from __future__ import annotations

from typing import Mapping

from clinical_operating_mind.coordinator import ClinicalOperatingMindCoordinator
from clinical_operating_mind.models import OperatingMindResult


class RuntimeOperatingMindAdapter:
    """Connects runtime engine results to the Clinical Operating Mind."""

    def __init__(self, coordinator: ClinicalOperatingMindCoordinator | None = None) -> None:
        self._coordinator = coordinator or ClinicalOperatingMindCoordinator()

    def coordinate(
        self,
        safety_result: Mapping[str, object],
        evidence_result: Mapping[str, object],
        optimization_result: Mapping[str, object],
        explanation_result: Mapping[str, object],
        clinical_snapshot: Mapping[str, object],
        clinical_timeline: Mapping[str, object],
        clinical_navigation: Mapping[str, object],
    ) -> OperatingMindResult:
        return self._coordinator.coordinate(
            safety_result,
            evidence_result,
            optimization_result,
            explanation_result,
            clinical_snapshot,
            clinical_timeline,
            clinical_navigation,
        )

