"""Validation for metadata-only drug packages."""

from scientific_knowledge.psychopharmacology.contracts import DrugPackageContract, DrugTemplate


class DrugTemplateValidator:
    """Validate that a drug template has required metadata and no content."""

    def validate(self, template: DrugTemplate) -> tuple[str, ...]:
        issues: list[str] = []
        metadata = template.metadata
        if not metadata.identifier:
            issues.append("identifier_required")
        if not metadata.generic_name:
            issues.append("generic_name_required")
        if not metadata.semantic_id:
            issues.append("semantic_id_required")
        if not metadata.knowledge_id:
            issues.append("knowledge_id_required")
        if not metadata.read_only_mode:
            issues.append("drug_metadata_must_be_read_only")
        if template.populated_sections:
            issues.append("scientific_content_not_allowed_in_a02")
        if template.allows_therapeutic_rule:
            issues.append("therapeutic_rules_forbidden")
        if template.allows_prescription:
            issues.append("prescription_forbidden")
        return tuple(issues)


class DrugPackageContractValidator:
    """Validate package-level metadata without approving publication."""

    def validate(self, contract: DrugPackageContract) -> tuple[str, ...]:
        issues: list[str] = []
        if not contract.package_name:
            issues.append("package_name_required")
        if not contract.drug_metadata:
            issues.append("drug_metadata_required")
        if contract.publication_status == "published":
            issues.append("publication_forbidden_without_gate")
        if contract.validation_status == "validated":
            issues.append("validation_cannot_be_self_assigned")
        if not contract.read_only_mode:
            issues.append("package_must_be_read_only")
        return tuple(issues)

