"""Simulation report engine."""

from __future__ import annotations

from clinical_simulation.models import SimulationBranch, SimulationReport, SimulationScenario


class SimulationReportEngine:
    def generate(self, scenario: SimulationScenario, branch: SimulationBranch, trace: str) -> SimulationReport:
        return SimulationReport(
            scenario=scenario.scenario_id,
            changes=("simulated_branch_created",),
            branch_summary=branch.branch_id,
            trace=trace,
        )

