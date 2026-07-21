"""Outcome comparator."""

from __future__ import annotations

from clinical_simulation.models import SimulationBranch, SimulationComparison, TwinClone


class OutcomeComparator:
    def compare(self, original: TwinClone, simulated: TwinClone, branches: tuple[SimulationBranch, ...]) -> SimulationComparison:
        differences = []
        if original.clone_id != simulated.clone_id:
            differences.append("clone_difference")
        differences.extend(f"branch:{branch.branch_id}" for branch in branches)
        return SimulationComparison(
            original_twin=original.source_twin_id,
            simulated_twin=simulated.source_twin_id,
            branch_differences=tuple(differences),
        )

