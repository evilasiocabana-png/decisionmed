"""Compatibility checks with existing knowledge architecture."""

from scientific_knowledge.psychopharmacology.contracts import DrugPackageContract


class KnowledgeLayerIntegration:
    def can_consume(self, contract: DrugPackageContract) -> bool:
        return contract.validation_status == "validated" and contract.publication_status == "published"


class EvidenceRuntimeCompatibility:
    def recognizes_package(self, contract: DrugPackageContract) -> bool:
        return bool(contract.package_id and contract.drug_metadata)

    def executes_runtime(self) -> bool:
        return False


class OntologyCompatibility:
    required_mapping = ("Drug", "Mechanism", "Receptor", "Interaction", "Monitoring", "Evidence", "Guideline")

    def missing_mappings(self, contract: DrugPackageContract) -> tuple[str, ...]:
        return tuple(item for item in self.required_mapping if item not in contract.ontology_mapping)

