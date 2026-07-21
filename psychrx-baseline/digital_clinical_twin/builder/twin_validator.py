"""Twin validator."""

from __future__ import annotations

from digital_clinical_twin.models import DigitalClinicalTwin


class TwinValidator:
    def validate(self, twin: DigitalClinicalTwin) -> tuple[str, ...]:
        issues = []
        if not twin.timeline_reference:
            issues.append("missing_timeline_reference")
        if not twin.snapshot_history:
            issues.append("missing_snapshot_history")
        if not twin.trace_id:
            issues.append("missing_trace")
        if not twin.knowledge_versions:
            issues.append("missing_knowledge_version")
        return tuple(issues)

