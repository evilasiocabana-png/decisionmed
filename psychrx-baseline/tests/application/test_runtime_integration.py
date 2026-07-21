import unittest

from application.app_service import PsychRxAppService


class RuntimeApplicationIntegrationTest(unittest.TestCase):
    def test_app_view_model_exposes_runtime_metadata(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.runtime_status.runtime_status, "completed_read_only")
        self.assertEqual(view_model.runtime_status.session_status, "open")
        self.assertTrue(view_model.runtime_status.read_only_mode)

    def test_workspace_contains_runtime_status_widget(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Runtime Status Widget", payload)
        self.assertIn("Runtime coordena execucao", payload)
        self.assertIn("completed_read_only", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()
