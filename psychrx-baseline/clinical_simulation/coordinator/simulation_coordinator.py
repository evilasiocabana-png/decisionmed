"""Coordinator for Clinical Simulation Platform."""

from __future__ import annotations

from clinical_simulation.audit import SimulationAudit
from clinical_simulation.branch import BranchEngine
from clinical_simulation.comparison import OutcomeComparator
from clinical_simulation.models import ClinicalSimulationResult, SimulationScenario
from clinical_simulation.reports import SimulationReportEngine
from clinical_simulation.runner import SimulationRunner
from clinical_simulation.sandbox import SandboxValidator, SimulationSandboxEngine, TwinCloneEngine
from digital_clinical_twin import TwinCoordinator


class SimulationCoordinator:
    """Coordinates isolated simulations without modifying production objects."""

    def __init__(self) -> None:
        self.sandbox = SimulationSandboxEngine()
        self.clone_engine = TwinCloneEngine()
        self.branch = BranchEngine()
        self.runner = SimulationRunner()
        self.comparator = OutcomeComparator()
        self.reports = SimulationReportEngine()
        self.validator = SandboxValidator()
        self.audit = SimulationAudit()
        self.twin_source = TwinCoordinator()

    def simulate(self, scenario: SimulationScenario | None = None) -> ClinicalSimulationResult:
        active_scenario = scenario or SimulationScenario(status="validated", inputs=("structural_input",))
        sandbox = self.sandbox.create()
        sandbox_issues = self.validator.validate(sandbox)
        official_twin = self.twin_source.build_twin()
        clone = self.clone_engine.clone(official_twin)
        branch = self.branch.create(active_scenario, clone)
        outcome = self.runner.run(sandbox, active_scenario, branch)
        comparison = self.comparator.compare(clone, clone, (branch,))
        report = self.reports.generate(active_scenario, branch, comparison.comparison_id)
        self.audit.record("SimulationExecuted")
        return ClinicalSimulationResult(
            sandbox_id=sandbox.sandbox_id,
            twin_clone_id=clone.clone_id,
            scenario_id=active_scenario.scenario_id,
            execution_plan=("create_sandbox", "clone_twin", "create_branch", "run_scenario", "compare", "report"),
            simulation_branch=branch,
            simulation_outcome=outcome,
            comparison=comparison,
            limitations=("isolated_sandbox_only", "does_not_modify_official_twin", *sandbox_issues),
            metadata=(report.report_id,),
        )

