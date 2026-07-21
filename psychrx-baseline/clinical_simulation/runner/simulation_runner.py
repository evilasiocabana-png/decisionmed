"""Simulation runner."""

from __future__ import annotations

from clinical_simulation.models import SimulationBranch, SimulationOutcome, SimulationSandbox, SimulationScenario


class SimulationRunner:
    def run(self, sandbox: SimulationSandbox, scenario: SimulationScenario, branch: SimulationBranch) -> SimulationOutcome:
        if not sandbox.isolated:
            return SimulationOutcome(status="rejected", differences=("unsafe_sandbox",))
        return SimulationOutcome(status="completed", differences=(f"scenario:{scenario.scenario_id}", f"branch:{branch.branch_id}"))

