"""Scenario validator."""

from __future__ import annotations

from clinical_simulation.models import SimulationScenario, SimulationSandbox, TwinClone


class ScenarioValidator:
    def validate(self, scenario: SimulationScenario, sandbox: SimulationSandbox, clone: TwinClone) -> tuple[str, ...]:
        issues = []
        if not scenario.inputs:
            issues.append("missing_scenario_inputs")
        if not sandbox.isolated:
            issues.append("sandbox_incompatible")
        if clone.shared_mutable_state:
            issues.append("clone_has_shared_mutable_state")
        return tuple(issues)

