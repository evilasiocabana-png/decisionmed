"""Timeline validation."""

from __future__ import annotations

from dataclasses import dataclass, field

from clinical_timeline.models import ClinicalTimeline


@dataclass(frozen=True)
class TimelineValidation:
    ordering_errors: tuple[str, ...] = field(default_factory=tuple)
    duplicate_snapshots: tuple[str, ...] = field(default_factory=tuple)
    broken_lineage: tuple[str, ...] = field(default_factory=tuple)
    missing_versions: tuple[str, ...] = field(default_factory=tuple)
    missing_traces: tuple[str, ...] = field(default_factory=tuple)

    @property
    def valid(self) -> bool:
        return not (
            self.ordering_errors
            or self.duplicate_snapshots
            or self.broken_lineage
            or self.missing_versions
            or self.missing_traces
        )


class TimelineValidator:
    """Checks structural timeline integrity."""

    def validate(self, timeline: ClinicalTimeline) -> TimelineValidation:
        ids = [node.snapshot_id for node in timeline.snapshots]
        duplicates = tuple(sorted({item for item in ids if ids.count(item) > 1}))
        missing_versions = tuple(node.snapshot_id for node in timeline.snapshots if not node.version)
        missing_traces = tuple(node.snapshot_id for node in timeline.snapshots if not node.trace_id)
        return TimelineValidation(
            duplicate_snapshots=duplicates,
            missing_versions=missing_versions,
            missing_traces=missing_traces,
        )
