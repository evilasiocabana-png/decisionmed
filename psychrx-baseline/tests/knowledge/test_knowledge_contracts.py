import unittest

from knowledge.core.status import KnowledgeStatus
from knowledge.loaders.knowledge_loader import KnowledgeLoader
from knowledge.models.evidence import EvidenceModel, EvidenceQuality
from knowledge.models.guideline import GuidelineModel
from knowledge.repositories.knowledge_repository import KnowledgeRepository
from knowledge.versioning.version import KnowledgeVersion


class KnowledgeContractTest(unittest.TestCase):
    def test_repository_contract_is_runtime_free(self) -> None:
        self.assertTrue(hasattr(KnowledgeRepository, "add"))
        self.assertTrue(hasattr(KnowledgeRepository, "get"))
        self.assertTrue(hasattr(KnowledgeRepository, "list"))
        self.assertTrue(hasattr(KnowledgeRepository, "find_by_status"))

    def test_loader_contract_does_not_load_content_by_itself(self) -> None:
        self.assertTrue(hasattr(KnowledgeLoader, "load"))

    def test_guideline_model_accepts_empty_schema_shape(self) -> None:
        guideline = GuidelineModel(
            identifier="guideline.schema",
            name="Guideline Schema",
            version=KnowledgeVersion(0, 1, 0),
            origin="schema",
            status=KnowledgeStatus.DRAFT,
        )

        self.assertEqual(guideline.sections, ())
        self.assertEqual(guideline.recommendations, ())

    def test_evidence_model_accepts_empty_schema_shape(self) -> None:
        evidence = EvidenceModel(
            identifier="evidence.schema",
            name="Evidence Schema",
            version=KnowledgeVersion(0, 1, 0),
            origin="schema",
        )

        self.assertEqual(evidence.quality, EvidenceQuality.UNRATED)
        self.assertEqual(evidence.limitations, ())


if __name__ == "__main__":
    unittest.main()
