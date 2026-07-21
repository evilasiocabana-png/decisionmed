import unittest
from pathlib import Path


class KnowledgeLibraryStructureTest(unittest.TestCase):
    def test_official_knowledge_library_structure_exists(self) -> None:
        required_dirs = [
            "guidelines",
            "drug_models",
            "evidence_sources",
            "contraindications",
            "interactions",
            "adverse_effects",
            "monitoring",
            "references",
            "validation",
            "registry",
        ]

        for dirname in required_dirs:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("knowledge_library") / dirname).is_dir())

    def test_registry_and_metadata_templates_exist(self) -> None:
        required_files = [
            "registry/KNOWLEDGE_REGISTRY.md",
            "registry/ID_FORMAT.md",
            "validation/METADATA_STANDARD.md",
            "validation/EMPTY_METADATA_TEMPLATE.md",
            "validation/VALIDATION_STATUS.md",
        ]

        for filename in required_files:
            with self.subTest(filename=filename):
                self.assertTrue((Path("knowledge_library") / filename).is_file())

    def test_guideline_drug_evidence_and_safety_schemas_exist(self) -> None:
        required_files = [
            "guidelines/GUIDELINE_SCHEMA.md",
            "guidelines/GUIDELINE_TEMPLATE.md",
            "guidelines/GUIDELINE_SOURCE_CATALOG.md",
            "guidelines/GUIDELINE_IMPORT_PROTOCOL.md",
            "guidelines/GUIDELINE_VALIDATION_TEMPLATE.md",
            "drug_models/DRUG_KNOWLEDGE_SCHEMA.md",
            "drug_models/DRUG_TEMPLATE.md",
            "drug_models/DRUG_CLASS_CATALOG.md",
            "drug_models/DRUG_EVIDENCE_LINK_MODEL.md",
            "drug_models/DRUG_KNOWLEDGE_VALIDATION_TEMPLATE.md",
            "evidence_sources/EVIDENCE_SOURCE_SCHEMA.md",
            "evidence_sources/EVIDENCE_HIERARCHY_MODEL.md",
            "evidence_sources/EVIDENCE_CONFLICT_MODEL.md",
            "evidence_sources/EVIDENCE_TRACEABILITY_TEMPLATE.md",
            "contraindications/CONTRAINDICATION_SCHEMA.md",
            "interactions/INTERACTION_SCHEMA.md",
            "adverse_effects/ADVERSE_EFFECT_SCHEMA.md",
            "monitoring/MONITORING_KNOWLEDGE_SCHEMA.md",
        ]

        for filename in required_files:
            with self.subTest(filename=filename):
                self.assertTrue((Path("knowledge_library") / filename).is_file())

    def test_draft_example_is_fictitious_and_not_validated(self) -> None:
        content = (
            Path("knowledge_library") / "registry" / "DRAFT_KNOWLEDGE_EXAMPLE.md"
        ).read_text(encoding="utf-8")

        self.assertIn("DRG-EXAMPLE-000", content)
        self.assertIn("GLD-EXAMPLE-000", content)
        self.assertIn("EVD-EXAMPLE-000", content)
        self.assertIn("validation_status: draft", content)
        self.assertIn("Fictitious", content)
        self.assertNotIn("validation_status: validated", content)

    def test_program_09_does_not_create_real_clinical_content(self) -> None:
        combined = []
        for path in Path("knowledge_library").rglob("*.md"):
            combined.append(path.read_text(encoding="utf-8").lower())
        payload = "\n".join(combined)

        forbidden_terms = [
            "dose recommendation",
            "prescribe",
            "start medication",
            "clinical decision approved",
            "validation_status: validated",
        ]
        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, payload)


if __name__ == "__main__":
    unittest.main()
