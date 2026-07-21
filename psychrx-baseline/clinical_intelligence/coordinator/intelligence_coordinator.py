"""Coordinator for Clinical Intelligence Platform."""

from __future__ import annotations

from clinical_intelligence.audit import IntelligenceAudit
from clinical_intelligence.context import ContextBroker
from clinical_intelligence.contracts import ContractManager, ContractValidator
from clinical_intelligence.explainability import ExplainabilityGateway, OutputValidator
from clinical_intelligence.governance import GovernanceGate, PermissionEngine
from clinical_intelligence.models import ClinicalIntelligenceCapability, ClinicalIntelligenceResult
from clinical_intelligence.registry import CapabilityRegistry, CapabilityValidator


class IntelligenceCoordinator:
    """Coordinates future intelligent capabilities without inference or decision making."""

    def __init__(self) -> None:
        self.registry = CapabilityRegistry()
        self.context = ContextBroker()
        self.contract_manager = ContractManager()
        self.contract_validator = ContractValidator()
        self.permission_engine = PermissionEngine()
        self.capability_validator = CapabilityValidator()
        self.governance = GovernanceGate()
        self.explainability = ExplainabilityGateway()
        self.output_validator = OutputValidator()
        self.audit = IntelligenceAudit()

    def evaluate_capability(self, capability: ClinicalIntelligenceCapability | None = None) -> ClinicalIntelligenceResult:
        active = self.registry.register(
            capability
            or ClinicalIntelligenceCapability(
                dependencies=(
                    "Clinical Operating Mind",
                    "Scientific Validation Framework",
                    "Knowledge Governance Platform",
                    "Clinical Quality Engine",
                )
            )
        )
        context = self.context.distribute()
        contract = self.contract_manager.create(active)
        contract_issues = self.contract_validator.validate(contract)
        permission = self.permission_engine.grant(active, ("Snapshot", "Timeline", "Knowledge", "Quality"))
        capability_issues = self.capability_validator.validate(active, contract, permission)
        governance = self.governance.evaluate((), permission)
        trace = f"trace:{active.capability_id}"
        explanations = self.explainability.explain(
            "structured_output",
            trace,
            ("Snapshot", "Timeline", "Quality"),
            ("no_ai_implementation", "no_clinical_decision"),
        )
        output_issues = self.output_validator.validate(
            trace,
            ("Snapshot", "Timeline"),
            (contract.capability_id,),
            "quality_validated",
        )
        self.audit.record("ClinicalIntelligenceCapabilityEvaluated")
        issues = contract_issues + capability_issues + output_issues
        return ClinicalIntelligenceResult(
            capability=active,
            context=context,
            contracts=(contract,),
            permissions=(permission,),
            outputs=("structured_output",) if not issues else (),
            explanations=explanations,
            quality_validation="valid" if not issues else "invalid",
            governance_decision=governance,
            audit=self.audit.snapshot(),
        )

