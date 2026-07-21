"""Timeline replay."""

from __future__ import annotations

from clinical_timeline.models import ClinicalTimeline


class TimelineReplay:
    """Returns stored timeline without recalculation."""

    def __init__(self, timeline: ClinicalTimeline) -> None:
        self._timeline = timeline

    def replay(self) -> ClinicalTimeline:
        return self._timeline
