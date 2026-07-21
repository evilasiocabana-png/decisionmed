"""Clinical Timeline coordinator."""

from __future__ import annotations

from clinical_timeline.audit import TimelineAudit, TimelineAuditEntry
from clinical_timeline.builder import TimelineBuilder
from clinical_timeline.models import ClinicalTimeline
from clinical_timeline.transition import TransitionEngine
from clinical_timeline.validator import TimelineValidation, TimelineValidator


class TimelineCoordinator:
    """Coordinates timeline creation without mutating snapshots."""

    def __init__(self) -> None:
        self.builder = TimelineBuilder()
        self.transition_engine = TransitionEngine()
        self.validator = TimelineValidator()
        self.audit = TimelineAudit()

    def execute(self, snapshots: tuple[dict[str, object], ...]) -> tuple[ClinicalTimeline, TimelineValidation]:
        timeline = self.builder.build(snapshots)
        transitions = self.transition_engine.detect(timeline.snapshots)
        timeline = ClinicalTimeline(
            timeline_id=timeline.timeline_id,
            patient_id=timeline.patient_id,
            snapshots=timeline.snapshots,
            transitions=transitions,
            events=timeline.events,
            metadata=timeline.metadata,
            statistics=timeline.statistics.__class__(
                snapshot_count=len(timeline.snapshots),
                transition_count=len(transitions),
                event_count=len(timeline.events),
            ),
            current_snapshot=timeline.current_snapshot,
            version=timeline.version,
            trace_id=timeline.trace_id,
        )
        validation = self.validator.validate(timeline)
        self.audit.record(TimelineAuditEntry(event="ClinicalTimelineCreated", timeline_id=timeline.timeline_id, trace_id=timeline.trace_id))
        return timeline, validation
