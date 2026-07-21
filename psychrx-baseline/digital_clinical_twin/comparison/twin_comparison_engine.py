"""Twin comparison engine."""

from __future__ import annotations

from digital_clinical_twin.models import DigitalClinicalTwin


class TwinComparisonEngine:
    def compare(self, left: DigitalClinicalTwin, right: DigitalClinicalTwin) -> tuple[str, ...]:
        differences = []
        if left.current_state != right.current_state:
            differences.append("state_differences")
        if left.snapshot_history != right.snapshot_history:
            differences.append("timeline_differences")
        if left.quality_history != right.quality_history:
            differences.append("quality_differences")
        if left.knowledge_versions != right.knowledge_versions:
            differences.append("knowledge_differences")
        return tuple(differences) or ("no_structural_difference",)

