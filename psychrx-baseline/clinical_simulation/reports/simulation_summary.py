"""Simulation summary."""

from __future__ import annotations

from clinical_simulation.models import SimulationComparison, SimulationScenario


class SimulationSummary:
    def generate(self, scenario: SimulationScenario, comparison: SimulationComparison) -> tuple[str, ...]:
        return (
            f"executed_scenario:{scenario.scenario_id}",
            f"main_differences:{len(comparison.branch_differences)}",
            "quality_comparison:structural",
            f"trace_references:{comparison.comparison_id}",
        )

