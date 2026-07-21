"""Coordinator for Knowledge Governance Platform."""

from __future__ import annotations

from knowledge_governance_platform.audit import GovernanceAudit
from knowledge_governance_platform.dependencies import DependencyAnalyzer
from knowledge_governance_platform.models import (
    EntityDefinition,
    KnowledgeGovernanceResult,
    OntologyDefinition,
    RelationshipDefinition,
)
from knowledge_governance_platform.ontology import OntologyRegistry, OntologyValidator
from knowledge_governance_platform.registry import EntityRegistry, RelationshipRegistry
from knowledge_governance_platform.taxonomy import TaxonomyManager
from knowledge_governance_platform.validation import SemanticConflictDetector, SemanticValidator
from knowledge_governance_platform.versioning import SemanticVersionManager


class GovernanceCoordinator:
    """Coordinates semantic governance without medical logic or Runtime access."""

    def __init__(self) -> None:
        self.ontology = OntologyRegistry()
        self.entities = EntityRegistry()
        self.relationships = RelationshipRegistry()
        self.taxonomy = TaxonomyManager()
        self.ontology_validator = OntologyValidator()
        self.semantic_validator = SemanticValidator()
        self.conflicts = SemanticConflictDetector()
        self.dependencies = DependencyAnalyzer()
        self.versioning = SemanticVersionManager()
        self.audit = GovernanceAudit()

    def validate_structure(self) -> KnowledgeGovernanceResult:
        ontology = self.ontology.register(OntologyDefinition(status="approved"))
        patient = self.entities.register(EntityDefinition("Patient", "Patient", aliases=("Paciente",), status="approved"))
        symptom = self.entities.register(EntityDefinition("Symptom", "Symptom", aliases=("Sintoma",), status="approved"))
        relationship = self.relationships.register(
            RelationshipDefinition("REL-Patient-Symptom", "Patient", "Symptom", "has_symptom", traceability="structural")
        )
        taxonomy = self.taxonomy.build(("Patient", "Clinical Finding", "Knowledge Object"))
        entities = self.entities.all()
        relationships = self.relationships.all()
        semantic_issues = (
            self.ontology_validator.validate(entities)
            + self.semantic_validator.validate(entities, relationships, taxonomy)
            + self.conflicts.detect(entities)
        )
        graph = self.dependencies.analyze(entities, relationships)
        self.audit.record("KnowledgeGovernanceValidated")
        return KnowledgeGovernanceResult(
            ontology_version=ontology.version.value(),
            entity_registry=entities,
            relationship_registry=relationships,
            taxonomy_version=taxonomy.version.value(),
            dependency_graph=graph,
            semantic_validation=semantic_issues + graph.issues,
            version_status="compatible",
            publication_decision="semantic_validation_passed" if not semantic_issues and not graph.issues else "hold",
            audit=self.audit.snapshot(),
        )

