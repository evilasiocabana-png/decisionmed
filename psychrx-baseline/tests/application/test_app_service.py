import unittest

from application.app_service import PsychRxAppService


class PsychRxAppServiceTest(unittest.TestCase):
    def test_app_view_model_exposes_safe_read_only_contract(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.status.product_name, "PsychRx")
        self.assertIn("NO PRESCRIPTION", view_model.status.safety_status)
        self.assertGreaterEqual(len(view_model.safety_guardrails), 4)
        self.assertGreaterEqual(len(view_model.clinical_workflow), 8)
        self.assertGreaterEqual(len(view_model.dashboard_panels), 4)
        self.assertGreaterEqual(len(view_model.clinical_experience_components), 8)
        self.assertGreaterEqual(len(view_model.consultation_regions), 4)

    def test_app_view_model_does_not_contain_prescribing_actions(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict()).lower()

        forbidden = ["dose recommendation", "prescribe now", "automatic prescription"]
        for term in forbidden:
            with self.subTest(term=term):
                self.assertNotIn(term, payload)

    def test_clinical_experience_components_have_safety_limits(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        names = {item.name for item in view_model.clinical_experience_components}

        self.assertIn("Guided Anamnesis", names)
        self.assertIn("Risk Widget", names)
        self.assertIn("Patient Friendly Mode", names)
        self.assertIn("Clinical Investigation Panel", names)
        self.assertIn("Objectives Widget", names)
        for component in view_model.clinical_experience_components:
            with self.subTest(component=component.name):
                self.assertTrue(component.safety_limit)

    def test_consultation_mvp_has_patient_first_and_strategy_locked(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        first_region = view_model.consultation_regions[0]
        payload = view_model.to_dict()

        self.assertEqual(first_region.name, "Paciente")
        self.assertIn("Patient Header", str(payload))
        self.assertIn("Current Medication", str(payload))
        self.assertIn("Strategy Panel", str(payload))
        self.assertIn("locked", str(payload))

    def test_clinical_investigation_panel_is_read_only_and_static(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Clinical Investigation Panel", payload)
        self.assertIn("read-only", payload)
        self.assertIn("ideacao suicida", payload.lower())
        self.assertIn("sintomas maniformes", payload.lower())
        self.assertIn("uso de substancias", payload.lower())
        self.assertIn("Guided Anamnesis", payload)
        self.assertIn("Perguntas Agora", payload)

    def test_objectives_widget_is_read_only_and_non_prescriptive(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Objectives Widget", payload)
        self.assertIn("Objetivos Terapeuticos", payload)
        self.assertIn("melhorar sono", payload.lower())
        self.assertIn("reduzir ansiedade", payload.lower())
        self.assertIn("nao sao recomendacoes", payload.lower())
        self.assertNotIn("iniciar medicamento", payload.lower())
        self.assertNotIn("ajustar dose agora", payload.lower())

    def test_risk_widget_is_conceptual_and_read_only(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Risk Panel", payload)
        self.assertIn("suicidio", payload.lower())
        self.assertIn("agressividade", payload.lower())
        self.assertIn("interacoes medicamentosas", payload.lower())
        self.assertIn("nao calcula risco real", payload.lower())
        self.assertNotIn("encaminhar agora", payload.lower())
        self.assertNotIn("risco calculado", payload.lower())


if __name__ == "__main__":
    unittest.main()
