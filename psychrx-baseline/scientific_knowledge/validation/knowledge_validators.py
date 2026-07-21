"""Structural validators for scientific knowledge metadata."""

from scientific_knowledge.models import KnowledgePackage, PublicationGateResult, ScientificEntityContract


class ScientificEntityContractValidator:
    """Validate that a scientific entity is traceable and governed."""

    def validate(self, contract: ScientificEntityContract) -> tuple[str, ...]:
        issues: list[str] = []
        if not contract.identifier:
            issues.append("identifier_required")
        if not contract.semantic_id:
            issues.append("semantic_id_required")
        if not contract.scientific_id:
            issues.append("scientific_id_required")
        if not contract.traceability.trace_id:
            issues.append("trace_id_required")
        if contract.editorial_review.editorial_status not in {
            "draft",
            "review",
            "scientific_review",
            "editorial_approval",
            "published",
            "deprecated",
        }:
            issues.append("invalid_editorial_status")
        if not contract.read_only_mode:
            issues.append("contract_must_be_read_only")
        return tuple(issues)


class DrugValidationPipeline:
    """Validate drug package structure without validating drug content."""

    def __init__(self, validator: ScientificEntityContractValidator | None = None) -> None:
        self._validator = validator or ScientificEntityContractValidator()

    def validate_package(self, package: KnowledgePackage) -> tuple[str, ...]:
        issues: list[str] = []
        if package.package_type != "drug":
            issues.append("package_type_must_be_drug")
        if package.publication_status == "published":
            issues.append("drug_package_cannot_publish_without_external_approvals")
        for entity in package.entities:
            issues.extend(self._validator.validate(entity))
            if entity.entity_type != "Drug":
                issues.append("drug_package_contains_non_drug_entity")
        return tuple(issues)


class PublicationGate:
    """Require all governance approvals before publication."""

    def evaluate(
        self,
        package: KnowledgePackage,
        *,
        scientific_validation_approved: bool = False,
        knowledge_governance_approved: bool = False,
        editorial_approved: bool = False,
        version_assigned: bool = False,
    ) -> PublicationGateResult:
        allowed = all(
            (
                scientific_validation_approved,
                knowledge_governance_approved,
                editorial_approved,
                version_assigned,
            )
        )
        reason = "publication_allowed" if allowed else "publication_requirements_incomplete"
        return PublicationGateResult(
            package_id=package.package_id,
            scientific_validation_approved=scientific_validation_approved,
            knowledge_governance_approved=knowledge_governance_approved,
            editorial_approved=editorial_approved,
            version_assigned=version_assigned,
            publish_allowed=allowed,
            reason=reason,
        )

