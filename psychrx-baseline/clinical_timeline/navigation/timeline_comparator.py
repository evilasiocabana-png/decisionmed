"""Timeline comparator."""

from __future__ import annotations

from clinical_timeline.models import TimelineNode, TimelineTransition


class TimelineComparator:
    """Compares two snapshot nodes structurally."""

    def compare(self, left: TimelineNode, right: TimelineNode) -> TimelineTransition:
        return TimelineTransition(
            from_snapshot=left.snapshot_id,
            to_snapshot=right.snapshot_id,
            change_type="modified" if left.snapshot != right.snapshot else "unchanged",
            summary="Structured comparison only. No clinical interpretation.",
        )
