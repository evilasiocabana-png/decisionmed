"""Timeline navigator."""

from __future__ import annotations

from clinical_timeline.models import ClinicalTimeline, TimelineNode


class TimelineNavigator:
    """Read-only timeline navigation."""

    def first(self, timeline: ClinicalTimeline) -> TimelineNode | None:
        return timeline.snapshots[0] if timeline.snapshots else None

    def latest(self, timeline: ClinicalTimeline) -> TimelineNode | None:
        return timeline.snapshots[-1] if timeline.snapshots else None

    def previous(self, timeline: ClinicalTimeline, snapshot_id: str) -> TimelineNode | None:
        ids = [node.snapshot_id for node in timeline.snapshots]
        if snapshot_id in ids and ids.index(snapshot_id) > 0:
            return timeline.snapshots[ids.index(snapshot_id) - 1]
        return None

    def next(self, timeline: ClinicalTimeline, snapshot_id: str) -> TimelineNode | None:
        ids = [node.snapshot_id for node in timeline.snapshots]
        if snapshot_id in ids and ids.index(snapshot_id) < len(ids) - 1:
            return timeline.snapshots[ids.index(snapshot_id) + 1]
        return None

    def by_version(self, timeline: ClinicalTimeline, version: str) -> tuple[TimelineNode, ...]:
        return tuple(node for node in timeline.snapshots if node.version == version)

    def by_timestamp(self, timeline: ClinicalTimeline, timestamp: str) -> TimelineNode | None:
        return next((node for node in timeline.snapshots if node.timestamp == timestamp), None)
