"""Evolution engine."""

from __future__ import annotations

from digital_clinical_twin.models import DigitalClinicalTwin


class EvolutionEngine:
    """Tracks structural evolution without interpretation."""

    def track(self, twin: DigitalClinicalTwin) -> tuple[str, ...]:
        return (
            f"context_evolution:{len(twin.snapshot_history)}",
            f"hypothesis_evolution:{len(twin.state_transitions)}",
            f"safety_evolution:{len(twin.quality_history)}",
            f"evidence_evolution:{len(twin.knowledge_versions)}",
            "quality_evolution:structural",
        )

