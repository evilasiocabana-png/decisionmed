"""Runtime adapter for Clinical Quality & Error Reduction Engine."""

from __future__ import annotations

from collections.abc import Mapping

from clinical_quality.coordinator import QualityCoordinator
from clinical_quality.models import ClinicalQualityResult


class RuntimeQualityAdapter:
    def __init__(self, coordinator: QualityCoordinator | None = None) -> None:
        self._coordinator = coordinator or QualityCoordinator()

    def evaluate(self, runtime_output: Mapping[str, object]) -> ClinicalQualityResult:
        return self._coordinator.evaluate(runtime_output)

