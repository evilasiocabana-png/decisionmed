"""Simulation sandbox engine."""

from __future__ import annotations

from clinical_simulation.models import SimulationSandbox


class SimulationSandboxEngine:
    def create(self) -> SimulationSandbox:
        return SimulationSandbox()

