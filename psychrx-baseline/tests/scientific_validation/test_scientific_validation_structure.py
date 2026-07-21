import unittest
from pathlib import Path

from scientific_validation import (
    ConflictResolutionEngine,
    EditorialReviewEngine,
    EvidenceQualityEvaluator,
    EvidenceSummaryGenerator,
    GuidelineRegistry,
    HierarchyEngine,
    KnowledgeVersionManager,
    PublicationGate,
    ScientificEvidence,
    ScientificSource,
    SourceLifecycle,
    SourceMetadataFactory,
    SourceRegistry,
    ValidationCoordinator,
)
from scientific_validation.audit import ScientificReplay


class ScientificValidationStructureTest(unittest.TestCase):
    def test_package_structure_exists(self) -> None:
        for dirname in [
            "coordinator",
            "sources",
            "quality",
            "governance",
            "editorial",
            "publication",
            "audit",
            "models",
        ]:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("scientific_validation") / dirname).is_dir())

    def test_source_registry_metadata_and_lifecycle(self) -> None:
        source = SourceMetadataFactory().create(
            title="Guideline candidate",
            authors=("Reviewer",),
            organization="Scientific body",
            publication_year=2026,
            doi="10.0000/example",
            language="en",
            country="US",
        )
        registry = SourceRegistry()
        registry.register(source)

        self.assertEqual(registry.all()[0].title, "Guideline candidate")
        self.assertTrue(SourceLifecycle().can_transition("candidate", "validated"))
        self.assertFalse(SourceLifecycle().can_transition("candidate", "active"))

    def test_quality_hierarchy_guidelines_conflicts_and_editorial_are_structural(self) -> None:
        evidence = ScientificEvidence(study_design="systematic_review", references=("SRC-1",))
        assessment = EvidenceQualityEvaluator().evaluate(evidence)
        summary = EvidenceSummaryGenerator().generate(assessment, evidence.references)
        conflict = ConflictResolutionEngine().register_conflict("guideline-a", "guideline-b", "version_mismatch")
        editorial = EditorialReviewEngine().decide(("reviewer",), "rationale", approved=True)

        self.assertEqual(assessment.status, "evaluated")
        self.assertIn("Clinical Guidelines", HierarchyEngine().hierarchy())
        self.assertIn("recommendations:none", summary)
        self.assertEqual(conflict, "conflict:guideline-a:guideline-b:version_mismatch")
        self.assertEqual(editorial.state, "approved")
        self.assertEqual(GuidelineRegistry().all(), ())

    def test_publication_gate_versioning_and_validation_result(self) -> None:
        coordinator = ValidationCoordinator()
        result = coordinator.validate_candidate(
            candidate="knowledge-candidate",
            source=ScientificSource(title="Validated source"),
            evidence=ScientificEvidence(study_design="meta_analysis", references=("SRC-1",)),
        )
        replayed = ScientificReplay().replay(result)
        payload = str(result.to_dict()).lower()

        self.assertEqual(result.publication_decision.outcome, "publish")
        self.assertTrue(result.publication_decision.publish_allowed)
        self.assertEqual(result.knowledge_version, "0.1.0")
        self.assertTrue(KnowledgeVersionManager().compatible("0.1.0", "0.2.0"))
        self.assertEqual(PublicationGate().decide(result.quality_assessment, result.editorial_review, True, "").outcome, "hold")
        self.assertEqual(replayed, result)
        self.assertNotIn("prescrever", payload)
        self.assertNotIn("dose recomendada", payload)


if __name__ == "__main__":
    unittest.main()

