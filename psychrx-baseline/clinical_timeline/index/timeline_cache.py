"""Timeline cache abstraction."""

from __future__ import annotations

from dataclasses import dataclass, field

from clinical_timeline.models import ClinicalTimeline


@dataclass
class TimelineCache:
    items: dict[str, ClinicalTimeline] = field(default_factory=dict)

    def key(self, timeline: ClinicalTimeline) -> str:
        return f"{timeline.timeline_id}:{timeline.version}"

    def put(self, timeline: ClinicalTimeline) -> None:
        self.items[self.key(timeline)] = timeline

    def get(self, timeline_id: str, version: str) -> ClinicalTimeline | None:
        return self.items.get(f"{timeline_id}:{version}")
