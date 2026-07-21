"""Branch engine."""

from __future__ import annotations

from clinical_simulation.models import SimulationBranch, SimulationScenario, TwinClone


class BranchEngine:
    def create(self, scenario: SimulationScenario, clone: TwinClone) -> SimulationBranch:
        return SimulationBranch(
            scenario_id=scenario.scenario_id,
            parent_clone_id=clone.clone_id,
            immutable_history=("branch_created",),
        )

