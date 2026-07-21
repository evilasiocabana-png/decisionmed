import unittest

from scientific_knowledge.psychopharmacology.audit import DrugAuditEvent, DrugAuditLog, DrugReplaySupport
from scientific_knowledge.psychopharmacology.catalog import (
    create_initial_ssri_catalog,
    create_initial_ssri_registry,
    create_ssri_package_contract,
)
from scientific_knowledge.psychopharmacology.contracts import DrugMetadata, DrugPackageContract, DrugTemplate
from scientific_knowledge.psychopharmacology.editorial import (
    DrugEditorialWorkflow,
    DrugPublicationChecklist,
    DrugPublicationGate,
)
from scientific_knowledge.psychopharmacology.integration import (
    EvidenceRuntimeCompatibility,
    KnowledgeLayerIntegration,
    OntologyCompatibility,
)
from scientific_knowledge.psychopharmacology.references import (
    EvidenceAttachment,
    ReferenceEntry,
    ReferenceRegistry,
    ReferenceValidator,
)
from scientific_knowledge.psychopharmacology.validation import (
    DrugPackageContractValidator,
    DrugTemplateValidator,
)


class PsychopharmacologyLibraryPopulationTests(unittest.TestCase):
    def test_initial_ssri_registry_contains_metadata_only(self):
        registry = create_initial_ssri_registry()
        names = tuple(item.generic_name for item in registry)

        self.assertEqual(6, len(registry))
        self.assertEqual(
            ("Fluoxetine", "Sertraline", "Paroxetine", "Citalopram", "Escitalopram", "Fluvoxamine"),
            names,
        )
        self.assertTrue(all(item.publication_status == "not_populated" for item in registry))
        self.assertTrue(all(item.validation_status == "not_validated" for item in registry))

    def test_ssri_catalog_is_ready_but_contains_no_scientific_content(self):
        catalog = create_initial_ssri_catalog()

        self.assertEqual("registered_not_populated", catalog["status"])
        self.assertTrue(catalog["ready_for_scientific_population"])
        self.assertFalse(catalog["contains_scientific_content"])

    def test_drug_template_validator_rejects_populated_sections_in_a02(self):
        valid = DrugTemplate(
            metadata=DrugMetadata(
                identifier="DRG-SSRI-001",
                generic_name="Fluoxetine",
                semantic_id="SEM-DRG-SSRI-FLUOXETINE",
                knowledge_id="KNW-DRG-SSRI-001",
            )
        )
        invalid = DrugTemplate(
            metadata=valid.metadata,
            populated_sections=("mechanism",),
        )

        self.assertEqual((), DrugTemplateValidator().validate(valid))
        self.assertIn("scientific_content_not_allowed_in_a02", DrugTemplateValidator().validate(invalid))
        self.assertFalse(valid.allows_prescription)
        self.assertFalse(valid.allows_therapeutic_rule)

    def test_drug_package_contract_validator_blocks_self_publication(self):
        contract = create_ssri_package_contract()
        published = DrugPackageContract(
            package_name="SSRIs Package",
            drug_metadata=contract.drug_metadata,
            validation_status="validated",
            publication_status="published",
        )

        self.assertEqual((), DrugPackageContractValidator().validate(contract))
        issues = DrugPackageContractValidator().validate(published)
        self.assertIn("publication_forbidden_without_gate", issues)
        self.assertIn("validation_cannot_be_self_assigned", issues)

    def test_reference_registry_and_validator_detect_invalid_or_duplicate_references(self):
        validator = ReferenceValidator()
        invalid = ReferenceEntry(reference_type="Unknown")
        valid_a = ReferenceEntry(reference_type="PMID", pmid="123")
        valid_b = ReferenceEntry(reference_type="PMID", pmid="123")
        registry = ReferenceRegistry()
        registry.register(valid_a)
        registry.register(valid_b)

        self.assertIn("invalid_reference_type", validator.validate(invalid))
        self.assertIn("missing_identifier", validator.validate(invalid))
        self.assertEqual((), validator.validate(valid_a))
        self.assertEqual((valid_b.reference_id,), registry.find_duplicates())

    def test_evidence_attachment_does_not_interpret_evidence(self):
        attachment = EvidenceAttachment(
            evidence_id="EVD-001",
            target_field="mechanism",
            target_entity_id="DRG-SSRI-001",
        )

        self.assertEqual("none", attachment.interpretation)
        self.assertTrue(attachment.trace_id)

    def test_editorial_workflow_and_publication_gate(self):
        workflow = DrugEditorialWorkflow()
        gate = DrugPublicationGate()
        incomplete = DrugPublicationChecklist(scientific_validation=True)
        complete = DrugPublicationChecklist(
            scientific_validation=True,
            knowledge_governance=True,
            editorial_approval=True,
            version_assignment=True,
            trace_validation=True,
        )

        self.assertEqual("Scientific Review", workflow.next_stage("Draft"))
        self.assertEqual("publication_rejected_incomplete_package", gate.evaluate(incomplete))
        self.assertEqual("publication_allowed", gate.evaluate(complete))

    def test_integration_requires_validated_published_package(self):
        contract = create_ssri_package_contract()
        knowledge = KnowledgeLayerIntegration()
        evidence = EvidenceRuntimeCompatibility()
        ontology = OntologyCompatibility()

        self.assertFalse(knowledge.can_consume(contract))
        self.assertTrue(evidence.recognizes_package(contract))
        self.assertFalse(evidence.executes_runtime())
        self.assertEqual((), ontology.missing_mappings(contract))

    def test_audit_and_replay_are_read_only(self):
        log = DrugAuditLog()
        event = DrugAuditEvent(package_id="OSKB-SSRI-PACKAGE-0.1", event_type="registration")
        log.record(event)
        replay = DrugReplaySupport().replay(log.list_events())

        self.assertTrue(event.read_only_mode)
        self.assertEqual(1, len(replay))
        self.assertIn("registration", replay[0])


if __name__ == "__main__":
    unittest.main()

