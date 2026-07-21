import unittest

from application.clinical_safety_assessment import ClinicalSafetyAssessmentService


def closed_safety():
    return {
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


class ClinicalSafetyAssessmentServiceTest(unittest.TestCase):
    def test_missing_value_is_not_interpreted_as_denied(self) -> None:
        safety = closed_safety()
        safety.pop("suicide")

        result = ClinicalSafetyAssessmentService().assess(
            safety, has_current_medication=True
        )

        self.assertFalse(result.closed)
        self.assertIn("suicide", result.missing_or_unknown)
        self.assertIn("Suicidio: Nao avaliado", result.warnings)

    def test_all_essential_domains_must_be_explicit(self) -> None:
        result = ClinicalSafetyAssessmentService().assess(
            closed_safety(), has_current_medication=True
        )

        self.assertTrue(result.closed)
        self.assertEqual((), result.warnings)

    def test_present_risk_blocks_even_when_other_domains_are_closed(self) -> None:
        safety = closed_safety()
        safety["qt_risk"] = "Presente"

        result = ClinicalSafetyAssessmentService().assess(
            safety, has_current_medication=True
        )

        self.assertFalse(result.closed)
        self.assertIn("qt_risk", result.present_risks)
        self.assertIn("Risco de QT: Presente", result.warnings)

    def test_high_value_contexts_are_explicit_essential_safety_domains(self) -> None:
        for field in ("aggression", "delirium", "intoxication", "withdrawal", "allergies", "severe_adverse_reaction"):
            with self.subTest(field=field):
                safety = closed_safety()
                safety.pop(field)
                result = ClinicalSafetyAssessmentService().assess(
                    safety, has_current_medication=False
                )
                self.assertIn(field, result.missing_or_unknown)

    def test_medication_fields_are_not_applicable_without_current_medication(self) -> None:
        safety = closed_safety()
        safety.pop("adherence")
        safety.pop("adverse_effects")

        result = ClinicalSafetyAssessmentService().assess(
            safety, has_current_medication=False
        )

        self.assertTrue(result.closed)
        self.assertIn(("adherence", "not_applicable"), result.normalized_states)


if __name__ == "__main__":
    unittest.main()
