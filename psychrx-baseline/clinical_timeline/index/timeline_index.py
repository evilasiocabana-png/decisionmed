"""In-memory timeline index."""

from __future__ import annotations

from dataclasses import dataclass, field

from clinical_timeline.models import ClinicalTimeline


@dataclass
class TimelineIndex:
    timelines: list[ClinicalTimeline] = field(default_factory=list)

    def add(self, timeline: ClinicalTimeline) -> None:
        self.timelines.append(timeline)

    def lookup(self, timeline_id: str) -> ClinicalTimeline | None:
        return next((item for item in self.timelines if item.timeline_id == timeline_id), None)

    def history(self) -> tuple[ClinicalTimeline, ...]:
        return tuple(self.timelines)

    def by_version(self, version: str) -> tuple[ClinicalTimeline, ...]:
        return tuple(item for item in self.timelines if item.version == version)

    def by_date(self, date_prefix: str) -> tuple[ClinicalTimeline, ...]:
        return tuple(item for item in self.timelines if item.metadata.creation_date.startswith(date_prefix))
