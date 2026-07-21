"""Twin compatibility validator."""

from __future__ import annotations

from digital_clinical_twin.models import DigitalClinicalTwin


class TwinCompatibility:
    def validate(self, twin: DigitalClinicalTwin) -> tuple[str, ...]:
        issues = []
        if not twin.knowledge_versions:
            issues.append("knowledge_incompatible")
        if not twin.timeline_reference:
            issues.append("timeline_incompatible")
        if not twin.snapshot_history:
            issues.append("snapshot_incompatible")
        if not twin.quality_history:
            issues.append("quality_engine_incompatible")
        return tuple(issues)

