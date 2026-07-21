"""Twin stability analyzer."""

from __future__ import annotations

from digital_clinical_twin.models import DigitalClinicalTwin


class TwinStabilityAnalyzer:
    """Evaluates structural stability, not clinical scoring."""

    def analyze(self, twin: DigitalClinicalTwin) -> tuple[str, ...]:
        return (
            f"snapshot_continuity:{bool(twin.snapshot_history)}",
            f"knowledge_consistency:{bool(twin.knowledge_versions)}",
            f"trace_continuity:{bool(twin.trace_id)}",
            f"quality_evolution:{bool(twin.quality_history)}",
            f"operating_mind_consistency:{bool(twin.current_state.operating_mind_reference)}",
        )

