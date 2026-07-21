"""Transition engine."""

from __future__ import annotations

from clinical_timeline.models import TimelineNode, TimelineTransition


class TransitionEngine:
    """Detects structural transitions between timeline nodes."""

    def detect(self, nodes: tuple[TimelineNode, ...]) -> tuple[TimelineTransition, ...]:
        transitions = []
        for left, right in zip(nodes, nodes[1:]):
            change_type = "modified" if left.snapshot != right.snapshot else "unchanged"
            transitions.append(
                TimelineTransition(
                    from_snapshot=left.snapshot_id,
                    to_snapshot=right.snapshot_id,
                    change_type=change_type,
                    summary=f"Transition {change_type} between immutable snapshots.",
                )
            )
        return tuple(transitions)
