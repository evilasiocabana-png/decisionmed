import unittest

from scientific_knowledge.catalogs import (
    create_empty_drug_catalog,
    create_guideline_source_catalog,
    create_package_registry_baseline,
)
from scientific_knowledge.editorial import EditorialPipeline, ScientificReviewerRegistry
from scientific_knowledge.models import (
    KnowledgePackage,
    ReviewerRecord,
    ScientificEntityContract,
)
from scientific_knowledge.packages import KnowledgePackageLoader
from scientific_knowledge.schema import create_official_schema
from scientific_knowledge.validation import (
    DrugValidationPipeline,
    PublicationGate,
    ScientificEntityContractValidator,
)


class OfficialScientificKnowledgeBaseTests(unittest.TestCase):
    def test_schema_defines_required_scientific_entities(self):
        schema = create_official_schema()

        self.assertIn("Drug", schema.supported_entities)
        self.assertIn("Guideline", schema.supported_entities)
        self.assertIn("trace_id", schema.required_contract_fields)
        self.assertTrue(schema.requires_scientific_validation)
        self.assertTrue(schema.requires_knowledge_governance)
        self.assertTrue(schema.read_only_mode)

    def test_entity_contract_requires_traceability_and_read_only_mode(self):
        contract = ScientificEntityContract(
            identifier="DRG-PLACEHOLDER",
            entity_type="Drug",
            semantic_id="SEM-DRG-PLACEHOLDER",
            scientific_id="SCI-DRG-PLACEHOLDER",
        )

        issues = ScientificEntityContractValidator().validate(contract)

        self.assertEqual((), issues)
        self.assertEqual("not_assigned", contract.traceability.evidence_level)
        self.assertEqual("draft", contract.editorial_review.editorial_status)
        self.assertTrue(contract.read_only_mode)

    def test_drug_validation_pipeline_blocks_published_package_without_approvals(self):
        package = KnowledgePackage(
            package_id="OSKB-DRUGS-DRAFT",
            package_type="drug",
            publication_status="published",
            entities=(
                ScientificEntityContract(
                    identifier="DRG-PLACEHOLDER",
                    entity_type="Drug",
                    semantic_id="SEM-DRG-PLACEHOLDER",
                    scientific_id="SCI-DRG-PLACEHOLDER",
                ),
            ),
        )

        issues = DrugValidationPipeline().validate_package(package)

        self.assertIn("drug_package_cannot_publish_without_external_approvals", issues)

    def test_publication_gate_requires_all_approvals(self):
        package = KnowledgePackage(package_id="OSKB-GUIDELINES-DRAFT", package_type="guideline")
        gate = PublicationGate()

        blocked = gate.evaluate(package, scientific_validation_approved=True)
        allowed = gate.evaluate(
            package,
            scientific_validation_approved=True,
            knowledge_governance_approved=True,
            editorial_approved=True,
            version_assigned=True,
        )

        self.assertFalse(blocked.publish_allowed)
        self.assertEqual("publication_requirements_incomplete", blocked.reason)
        self.assertTrue(allowed.publish_allowed)
        self.assertEqual("publication_allowed", allowed.reason)

    def test_package_loader_registers_only_when_dependencies_exist(self):
        loader = KnowledgePackageLoader()
        missing_dependency_package = KnowledgePackage(
            package_id="OSKB-PKG-1",
            package_type="guideline",
            dependencies=("MISSING",),
        )
        valid_package = KnowledgePackage(package_id="OSKB-PKG-2", package_type="guideline")

        missing_issues = loader.load(missing_dependency_package)
        valid_issues = loader.load(valid_package)

        self.assertEqual(("missing_dependency:MISSING",), missing_issues)
        self.assertEqual((), valid_issues)
        self.assertIsNone(loader.registry.get("OSKB-PKG-1"))
        self.assertIsNotNone(loader.registry.get("OSKB-PKG-2"))

    def test_editorial_pipeline_and_reviewer_registry_are_metadata_only(self):
        pipeline = EditorialPipeline()
        registry = ScientificReviewerRegistry()
        registry.register(ReviewerRecord(reviewer_id="REV-001", decision="not_assigned"))

        self.assertEqual("review", pipeline.next_stage("draft"))
        self.assertEqual("published", pipeline.next_stage("editorial_approval"))
        self.assertEqual(1, len(registry.list_reviewers()))

    def test_initial_catalogs_do_not_contain_drug_content(self):
        drug_catalog = create_empty_drug_catalog()
        guideline_catalog = create_guideline_source_catalog()
        registry = create_package_registry_baseline()

        self.assertEqual((), drug_catalog["entries"])
        self.assertFalse(drug_catalog["allows_clinical_content"])
        self.assertTrue(all(entry["status"] == "metadata_only" for entry in guideline_catalog))
        self.assertEqual(2, len(registry))


if __name__ == "__main__":
    unittest.main()

