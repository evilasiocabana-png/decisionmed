import unittest

from application.clinical_decision_support_service import ClinicalDecisionSupportService


def safety_payload(**overrides):
    values = {
        "suicide": "Negado",
        "aggression": "Negado",
        "mania_or_hypomania": "Negado",
        "substances": "Negado",
        "delirium": "Negado",
        "intoxication": "Negado",
        "withdrawal": "Negado",
        "allergies": "Negado",
        "severe_adverse_reaction": "Negado",
        "interactions": "Negado",
        "qt_risk": "Negado",
        "pregnancy_or_lactation": "Nao aplicavel",
        "metabolic_risk": "Negado",
        "acute_toxicity": "Negado",
        "adherence": "Boa",
        "adverse_effects": "Ausentes",
    }
    values.update(overrides)
    return values


class PolypharmacyRegimenAxisTest(unittest.TestCase):
    def test_regimen_axis_is_visible_even_when_safety_blocks_strategy(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "diagnostic_context": "TEPT / F43.1",
                "clinical_presentation": "Revisao medicamentosa",
                "symptoms": (
                    "Irritabilidade",
                    "Impulsividade",
                    "Ideacao suicida",
                ),
                "impairment_domains": ("Trabalho", "Familia", "Financeiro"),
                "impairment_severity": "Grave",
                "stability": "Instavel",
                "current_medications": (
                    {"name": "Unialtrex", "dose_value": "50", "dose_unit": "mg", "frequency": "1x/dia"},
                    {"name": "Trazodona", "dose_value": "50", "dose_unit": "mg", "frequency": "noite"},
                    {"name": "Fluoxetina", "dose_value": "20", "dose_unit": "mg", "frequency": "1x/dia"},
                    {"name": "Rivotril", "dose_value": "0.25", "dose_unit": "mg", "frequency": "1x/dia"},
                    {"name": "Lexotan", "dose_value": "6", "dose_unit": "mg", "frequency": "1x/dia"},
                ),
                "safety": safety_payload(suicide="Presente", substances="Presente"),
            }
        )

        rationale = " ".join(response.clinical_rationale)

        self.assertEqual(response.status, "blocked")
        self.assertIn("Regime atual por eixos", rationale)
        self.assertIn("Unialtrex 50 mg 1x/dia -> substancias/craving", rationale)
        self.assertIn("Trazodona 50 mg noite -> sono/sedacao", rationale)
        self.assertIn("Fluoxetina 20 mg 1x/dia -> humor/ansiedade/TEPT", rationale)
        self.assertIn("Rivotril 0.25 mg 1x/dia -> ansiedade/resgate", rationale)
        self.assertIn("Lexotan 6 mg 1x/dia -> ansiedade/resgate", rationale)

    def test_motor_reports_uncovered_clinical_axis_from_recipe(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "diagnostic_context": "TEPT / F43.1",
                "clinical_presentation": "Revisao medicamentosa",
                "symptoms": ("Humor deprimido", "Ansiedade", "Insonia inicial"),
                "clinical_axes": ("humor/TEPT", "sono/sedacao", "ansiedade/resgate"),
                "impairment_domains": ("Trabalho",),
                "impairment_severity": "Importante",
                "stability": "Resposta parcial",
                "pharmacological_profile": (
                    "Eixo humor/TEPT",
                    "Eixo sono/sedacao",
                    "Eixo ansiedade/resgate",
                ),
                "current_medications": (
                    {
                        "name": "Fluoxetina",
                        "dose_value": "20",
                        "dose_unit": "mg",
                        "frequency": "1x/dia",
                        "duration": "8 semanas",
                        "adherence": "Boa",
                        "response": "Resposta parcial",
                        "tolerability": "Boa",
                    },
                ),
                "safety": safety_payload(),
            }
        )

        rationale = " ".join(response.clinical_rationale)

        self.assertEqual(response.status, "unresolved")
        self.assertIn("Eixos clinicos a cobrir: humor/TEPT, sono/sedacao, ansiedade/resgate", rationale)
        self.assertIn("Eixos cobertos pela receita: humor/TEPT, ansiedade/resgate", rationale)
        self.assertIn("Eixos sem cobertura clara: sono/sedacao", rationale)
        self.assertTrue(response.excluded_medications)


if __name__ == "__main__":
    unittest.main()
