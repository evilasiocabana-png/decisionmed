"""Build ordered timelines from immutable snapshots."""

from __future__ import annotations

from clinical_timeline.models import ClinicalTimeline, TimelineMetadata, TimelineNode, TimelineStatistics


class TimelineBuilder:
    """Creates ordered timeline nodes without mutating snapshots."""

    def build(self, snapshots: tuple[dict[str, object], ...]) -> ClinicalTimeline:
        ordered = tuple(sorted(snapshots, key=lambda item: str(item.get("timestamp", ""))))
        nodes = tuple(
            TimelineNode(
                snapshot_id=str(snapshot.get("snapshot_id", "")),
                timestamp=str(snapshot.get("timestamp", "")),
                version=self._version_label(snapshot),
                trace_id=str(snapshot.get("trace_id", "")),
                snapshot=snapshot,
            )
            for snapshot in ordered
        )
        return ClinicalTimeline(
            snapshots=nodes,
            metadata=TimelineMetadata(snapshot_count=len(nodes)),
            statistics=TimelineStatistics(snapshot_count=len(nodes)),
            current_snapshot=nodes[-1].snapshot_id if nodes else "",
        )

    def _version_label(self, snapshot: dict[str, object]) -> str:
        version = snapshot.get("version", {})
        if isinstance(version, dict):
            return f"{version.get('major', 0)}.{version.get('minor', 0)}.{version.get('patch', 0)}"
        return "0.0.0"
