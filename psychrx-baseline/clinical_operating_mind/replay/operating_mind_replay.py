"""Read-only deterministic replay for Clinical Operating Mind."""

from __future__ import annotations

from clinical_operating_mind.models import ClinicalOperatingMindState


class OperatingMindReplay:
    """Reconstructs the recorded state without recalculation."""

    def replay(self, state: ClinicalOperatingMindState) -> ClinicalOperatingMindState:
        return state

