"""Simulation replay."""

from __future__ import annotations

from clinical_simulation.models import ClinicalSimulationResult


class SimulationReplay:
    def replay(self, result: ClinicalSimulationResult) -> ClinicalSimulationResult:
        return result

