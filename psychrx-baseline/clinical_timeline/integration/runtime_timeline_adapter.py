"""Runtime adapter for Clinical Timeline Engine."""

from __future__ import annotations

from clinical_timeline.coordinator import TimelineCoordinator
from clinical_timeline.models import ClinicalTimeline


class RuntimeTimelineAdapter:
    def __init__(self, coordinator: TimelineCoordinator | None = None) -> None:
        self._coordinator = coordinator or TimelineCoordinator()

    def build(self, snapshots: tuple[dict[str, object], ...]) -> ClinicalTimeline:
        timeline, _ = self._coordinator.execute(snapshots)
        return timeline
