"""Timeline exporters."""

from __future__ import annotations

from clinical_timeline.models import ClinicalTimeline


class TimelineExporter:
    def internal_json(self, timeline: ClinicalTimeline) -> dict[str, object]:
        return timeline.to_dict()

    def developer_json(self, timeline: ClinicalTimeline) -> dict[str, object]:
        return {"timeline": timeline.to_dict(), "developer": True}

    def audit_json(self, timeline: ClinicalTimeline) -> dict[str, object]:
        return {"timeline_id": timeline.timeline_id, "trace_id": timeline.trace_id}

    def future_interoperability_placeholder(self) -> dict[str, str]:
        return {"status": "future_interoperability_placeholder"}
