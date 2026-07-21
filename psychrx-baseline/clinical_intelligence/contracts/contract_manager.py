"""Intelligence contract manager."""

from __future__ import annotations

from clinical_intelligence.models import ClinicalIntelligenceCapability, IntelligenceContract


class ContractManager:
    def create(self, capability: ClinicalIntelligenceCapability) -> IntelligenceContract:
        return IntelligenceContract(
            capability_id=capability.capability_id,
            inputs=("Snapshot", "Timeline", "Operating Mind", "Quality Result", "Knowledge Version"),
            outputs=("structured_output", "explanation", "trace"),
            immutable=True,
            trace_required=True,
            quality_requirements=("quality_status", "contract_compliance"),
        )

