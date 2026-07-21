import unittest

from application.app_service import PsychRxAppService
from application.kernel_adapter import ApplicationKernelAdapter


class KernelIntegrationTest(unittest.TestCase):
    def test_kernel_adapter_returns_structural_result(self) -> None:
        result = ApplicationKernelAdapter().get_kernel_result()

        self.assertEqual(result.status, "read_only_structural")
        self.assertIn("Strategies blocked", result.blocked_reason)

    def test_app_view_model_exposes_kernel_metadata(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.kernel_status.kernel_status, "read_only_structural")
        self.assertTrue(view_model.kernel_status.read_only_mode)
        self.assertIn(
            "Safety Engine",
            view_model.kernel_status.future_integrations,
        )

    def test_workspace_keeps_strategy_blocked_by_kernel_result(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Kernel Status Widget", payload)
        self.assertIn("Evidence Graph Runtime", payload)
        self.assertIn("Therapeutic Optimization Runtime", payload)
        self.assertIn("Strategy Widget", payload)
        self.assertNotIn("Prescrever", payload)
        self.assertNotIn("Dose recomendada", payload)


if __name__ == "__main__":
    unittest.main()
