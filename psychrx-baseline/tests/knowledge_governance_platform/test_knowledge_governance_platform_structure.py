import unittest
from pathlib import Path

from knowledge_governance_platform import (
    CompatibilityAnalyzer,
    DependencyAnalyzer,
    EntityDefinition,
    GovernanceCoordinator,
    GovernanceReplay,
    MigrationPlanner,
    OntologyLifecycle,
    OntologyValidator,
    RelationshipDefinition,
    SemanticConflictDetector,
    SemanticValidator,
    SemanticVersionManager,
    TaxonomyManager,
)


class KnowledgeGovernancePlatformStructureTest(unittest.TestCase):
    def test_package_structure_exists(self) -> None:
        for dirname in [
            "coordinator",
            "ontology",
            "registry",
            "relationships",
            "taxonomy",
            "validation",
            "dependencies",
            "versioning",
            "audit",
            "models",
        ]:
            with self.subTest(dirname=dirname):
                expected = Path("knowledge_governance_platform") / dirname
                if dirname == "relationships":
                    expected = Path("knowledge_governance_platform") / "registry"
                self.assertTrue(expected.is_dir())

    def test_ontology_and_semantic_validation_detect_issues(self) -> None:
        patient = EntityDefinition("Patient", "Patient", aliases=("person",))
        duplicate = EntityDefinition("Patient2", "Patient", aliases=("person",))
        taxonomy = TaxonomyManager().build(("Clinical",))

        ontology_issues = OntologyValidator().validate((patient, duplicate))
        semantic_issues = SemanticValidator().validate((patient,), (), taxonomy)
        conflicts = SemanticConflictDetector().detect((patient, duplicate))

        self.assertIn("duplicate_entity:Patient", ontology_issues)
        self.assertEqual(semantic_issues, ())
        self.assertIn("ambiguous_mapping:person", conflicts)
        self.assertTrue(OntologyLifecycle().can_transition("draft", "proposed"))

    def test_dependencies_versioning_and_migration_are_structural(self) -> None:
        patient = EntityDefinition("Patient", "Patient")
        rel = RelationshipDefinition("REL", "Patient", "Missing", "has_missing")
        graph = DependencyAnalyzer().analyze((patient,), (rel,))
        current = SemanticVersionManager().create(0, 1, 0)
        target = SemanticVersionManager().create(0, 2, 0)
        incompatible = SemanticVersionManager().create(1, 0, 0)

        self.assertIn("broken_reference:Missing", graph.issues)
        self.assertEqual(CompatibilityAnalyzer().compatible(current, target), (True, "compatible"))
        self.assertEqual(CompatibilityAnalyzer().compatible(current, incompatible), (False, "major_version_mismatch"))
        self.assertIn("automatic_migration:not_allowed", MigrationPlanner().plan(("Patient",)))

    def test_governance_coordinator_and_replay_are_read_only(self) -> None:
        result = GovernanceCoordinator().validate_structure()
        replayed = GovernanceReplay().replay(result)
        payload = str(result.to_dict()).lower()

        self.assertEqual(result.publication_decision, "semantic_validation_passed")
        self.assertEqual(len(result.entity_registry), 2)
        self.assertEqual(len(result.relationship_registry), 1)
        self.assertEqual(result.dependency_graph.issues, ())
        self.assertTrue(result.read_only_mode)
        self.assertEqual(replayed, result)
        self.assertNotIn("prescrever", payload)
        self.assertNotIn("dose recomendada", payload)


if __name__ == "__main__":
    unittest.main()

