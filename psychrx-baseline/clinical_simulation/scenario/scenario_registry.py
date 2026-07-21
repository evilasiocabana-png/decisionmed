"""Scenario registry."""

from __future__ import annotations

from clinical_simulation.models import SimulationScenario


class ScenarioRegistry:
    def __init__(self) -> None:
        self._scenarios: dict[str, SimulationScenario] = {}

    def register(self, scenario: SimulationScenario) -> SimulationScenario:
        self._scenarios[scenario.scenario_id] = scenario
        return scenario

    def all(self) -> tuple[SimulationScenario, ...]:
        return tuple(self._scenarios.values())

