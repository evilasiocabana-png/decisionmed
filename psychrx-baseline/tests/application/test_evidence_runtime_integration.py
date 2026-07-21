import unittest

from application.app_service import PsychRxAppService
from clinical_runtime import ClinicalRuntime


class EvidenceRuntimeIntegrationTest(unittest.TestCase):
    def test_runtime_exposes_evidence_result_after_safety(self) -> None:
        result = ClinicalRuntime().execute()

        self.assertEqual(result["evidence_result"]["status"], "completed_read_only")
        self.assertEqual(result["evidence_result"]["snapshot"]["selected_count"], 0)
        self.assertIn("Safety", result["result"]["outputs"])
        self.assertIn("Evidence", result["result"]["outputs"])
        self.assertEqual(result["clinical_decision"], "not_implemented")
        self.assertEqual(result["prescription"], "not_available")

    def test_app_view_model_exposes_evidence_runtime_metadata(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.evidence_runtime_status.runtime_status, "completed_read_only")
        self.assertEqual(view_model.evidence_runtime_status.selected_count, 0)
        self.assertTrue(view_model.evidence_runtime_status.read_only_mode)

    def test_workspace_contains_evidence_runtime_widget_without_recommendations(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Evidence Runtime Status Widget", payload)
        self.assertIn("EvidenceResult", payload)
        self.assertIn("Strategy Widget", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()
