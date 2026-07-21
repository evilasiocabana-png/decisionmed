import unittest

from application.app_service import PsychRxAppService
from clinical_runtime import ClinicalRuntime


class KnowledgeGovernancePlatformIntegrationTest(unittest.TestCase):
    def test_knowledge_governance_is_not_in_runtime_pipeline(self) -> None:
        result = ClinicalRuntime().execute()

        self.assertNotIn("knowledge_governance_platform", result)
        self.assertNotIn("Knowledge Governance", result["result"]["outputs"])
        self.assertEqual(result["prescription"], "not_available")

    def test_app_view_model_exposes_knowledge_governance_read_only(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.knowledge_governance_status.status, "available_read_only")
        self.assertFalse(view_model.knowledge_governance_status.runtime_connected)
        self.assertEqual(view_model.knowledge_governance_status.publication_decision, "semantic_validation_passed")
        self.assertEqual(view_model.knowledge_governance_status.entity_count, 2)
        self.assertTrue(view_model.knowledge_governance_status.read_only_mode)

    def test_workspace_contains_knowledge_governance_widget_without_prescription(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Knowledge Governance Platform Status Widget", payload)
        self.assertIn("KnowledgeGovernanceResult", payload)
        self.assertIn("Runtime integration: forbidden", payload)
        self.assertIn("Scientific Validation alone: insufficient", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()

