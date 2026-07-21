"""Coordinator for the Clinical Operating Mind."""

from __future__ import annotations

from typing import Mapping

from clinical_operating_mind.audit import OperatingMindAuditLog, OperatingMindTraceBuilder
from clinical_operating_mind.contracts import EngineContractRegistry
from clinical_operating_mind.governance import GovernanceRuleRegistry, SafetyGovernanceGate
from clinical_operating_mind.lifecycle import LifecycleDefinition
from clinical_operating_mind.models import ClinicalOperatingMindState, OperatingMindAudit, OperatingMindResult
from clinical_operating_mind.transitions import TransitionValidator


class ClinicalOperatingMindCoordinator:
    """Coordinates engine outputs without mutating them or deciding clinically."""

    def __init__(self) -> None:
        self.lifecycle_definition = LifecycleDefinition()
        self.contract_registry = EngineContractRegistry()
        self.transition_validator = TransitionValidator()
        self.governance = GovernanceRuleRegistry()
        self.safety_gate = SafetyGovernanceGate()
        self.audit = OperatingMindAuditLog()
        self.trace_builder = OperatingMindTraceBuilder()

    def coordinate(
        self,
        safety_result: Mapping[str, object],
        evidence_result: Mapping[str, object],
        optimization_result: Mapping[str, object],
        explanation_result: Mapping[str, object],
        clinical_snapshot: Mapping[str, object],
        clinical_timeline: Mapping[str, object],
        clinical_navigation: Mapping[str, object],
    ) -> OperatingMindResult:
        lifecycle = self.lifecycle_definition.build()
        completed = tuple(phase.name for phase in lifecycle.phases)
        transition_errors = self.transition_validator.validate_completed(completed)
        safety_allowed, blocking_reason = self.safety_gate.evaluate(safety_result)
        trace = self.trace_builder.build(
            safety_result,
            evidence_result,
            optimization_result,
            explanation_result,
            clinical_snapshot,
            clinical_timeline,
            clinical_navigation,
        )
        status = "navigation_ready" if safety_allowed and not transition_errors else "blocked"
        audit_entry = OperatingMindAudit(
            event="OperatingMindCoordinated",
            phase="Navigation Update",
            validation_result="valid" if not transition_errors else "invalid",
            trace_id=trace.trace_id,
        )
        self.audit.record(audit_entry)
        state = ClinicalOperatingMindState(
            status=status,
            current_phase="Navigation Update",
            completed_phases=completed,
            lifecycle=lifecycle,
            contracts=self.contract_registry.operating_contracts(),
            audit=self.audit.snapshot(),
            trace=trace,
            governance_warnings=(),
            blocking_reason=blocking_reason,
            read_only_mode=True,
        )
        output_errors = self.governance.validate_output(str(state.to_dict()))
        validation_errors = transition_errors + output_errors
        return OperatingMindResult(
            state=state,
            validation_errors=validation_errors,
            blocked=not safety_allowed or bool(validation_errors),
        )

