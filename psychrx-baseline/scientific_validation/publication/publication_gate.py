"""Publication gate for validated knowledge."""

from __future__ import annotations

from scientific_validation.models import EditorialDecision, PublicationDecision, QualityAssessment


class PublicationGate:
    """Allows knowledge publication only after validation requirements."""

    def decide(
        self,
        quality: QualityAssessment,
        editorial: EditorialDecision,
        trace_valid: bool,
        version: str,
    ) -> PublicationDecision:
        if quality.status != "evaluated":
            return PublicationDecision("hold", version, "quality_evaluation_required", False)
        if editorial.state != "approved":
            return PublicationDecision("hold", version, "editorial_approval_required", False)
        if not trace_valid:
            return PublicationDecision("hold", version, "trace_validation_required", False)
        if not version:
            return PublicationDecision("hold", version, "version_assignment_required", False)
        return PublicationDecision("publish", version, "validated_for_knowledge_layer", True)

