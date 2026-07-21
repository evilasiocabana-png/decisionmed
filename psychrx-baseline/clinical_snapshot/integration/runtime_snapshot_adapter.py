"""Runtime adapter for Clinical Snapshot Engine."""

from __future__ import annotations

from clinical_snapshot.coordinator import SnapshotCoordinator
from clinical_snapshot.models import ClinicalSnapshot


class RuntimeSnapshotAdapter:
    def __init__(self, coordinator: SnapshotCoordinator | None = None) -> None:
        self._coordinator = coordinator or SnapshotCoordinator()

    def build(
        self,
        runtime_result: dict[str, object],
        safety_result: dict[str, object],
        evidence_result: dict[str, object],
        optimization_result: dict[str, object],
        explanation_result: dict[str, object],
    ) -> ClinicalSnapshot:
        snapshot, _ = self._coordinator.execute(
            runtime_result,
            safety_result,
            evidence_result,
            optimization_result,
            explanation_result,
        )
        return snapshot
