import unittest

from application.app_service import PsychRxAppService
from clinical_runtime import ClinicalRuntime


class ClinicalTimelineIntegrationTest(unittest.TestCase):
    def test_runtime_exposes_clinical_timeline_after_snapshot(self) -> None:
        result = ClinicalRuntime().execute()

        self.assertIn("clinical_timeline", result)
        self.assertEqual(result["clinical_timeline"]["statistics"]["snapshot_count"], 1)
        self.assertIn("Timeline", result["result"]["outputs"])
        self.assertEqual(result["prescription"], "not_available")

    def test_app_view_model_exposes_timeline_metadata(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.clinical_timeline_status.status, "available_read_only")
        self.assertTrue(view_model.clinical_timeline_status.read_only_mode)

    def test_workspace_contains_timeline_widget_without_prescription(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Clinical Timeline Engine Status Widget", payload)
        self.assertIn("ClinicalTimeline", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()
