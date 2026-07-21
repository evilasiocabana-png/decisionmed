"""Current state resolver."""

from __future__ import annotations

from clinical_timeline.models import ClinicalTimeline, TimelineNode


class CurrentStateResolver:
    """Returns latest valid snapshot node."""

    def resolve(self, timeline: ClinicalTimeline) -> TimelineNode | None:
        return timeline.snapshots[-1] if timeline.snapshots else None
