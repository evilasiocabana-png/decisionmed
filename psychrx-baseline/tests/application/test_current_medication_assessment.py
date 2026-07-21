import unittest

from application.clinical_decision_support_contract import CurrentMedicationPayload
from application.current_medication_assessment import (
    CurrentMedicationAssessmentService,
)


class CurrentMedicationAssessmentTest(unittest.TestCase):
    def test_assessment_calculates_core_status_fields(self) -> None:
        assessment = CurrentMedicationAssessmentService().assess(
            CurrentMedicationPayload(
                name="Sertralina",
                dose_value="50",
                dose_unit="mg",
                frequency="1x/dia",
                duration="4 semanas",
                adherence="Boa",
                response="Resposta parcial",
                tolerability="Boa",
            )
        )

        self.assertEqual(assessment.current_dose_status, "within_registered_range")
        self.assertEqual(assessment.duration_status, "duration_possibly_sufficient")
        self.assertEqual(assessment.response_status, "partial_response")
        self.assertEqual(assessment.tolerability_status, "good_tolerability")
        self.assertEqual(
            assessment.optimization_possible,
            "indeterminate",
        )
        self.assertIn("Avaliacao da medicacao atual", assessment.summary())

    def test_missing_or_unknown_dose_is_indeterminate(self) -> None:
        assessment = CurrentMedicationAssessmentService().assess(
            CurrentMedicationPayload(
                name="Medicamento fora da tabela",
                dose_value="",
                dose_unit="mg",
                frequency="",
                duration="",
                adherence="",
                response="",
                tolerability="",
            )
        )

        self.assertEqual(assessment.current_dose_status, "dose_indeterminate")
        self.assertEqual(assessment.duration_status, "duration_indeterminate")
        self.assertEqual(assessment.response_status, "response_indeterminate")
        self.assertIn("dose_value", assessment.missing_fields)

    def test_assessment_detects_below_and_above_registered_range(self) -> None:
        service = CurrentMedicationAssessmentService()

        below = service.assess(
            CurrentMedicationPayload(
                name="Sertralina",
                dose_value="10",
                dose_unit="mg",
                frequency="1x/dia",
            )
        )
        above = service.assess(
            CurrentMedicationPayload(
                name="Sertralina",
                dose_value="300",
                dose_unit="mg",
                frequency="1x/dia",
            )
        )

        self.assertEqual(below.current_dose_status, "below_registered_range")
        self.assertEqual(above.current_dose_status, "above_registered_range")

    def test_assessment_detects_insufficient_adherence_and_intolerance(self) -> None:
        assessment = CurrentMedicationAssessmentService().assess(
            CurrentMedicationPayload(
                name="Sertralina",
                dose_value="50",
                dose_unit="mg",
                frequency="1x/dia",
                duration="4 semanas",
                adherence="Ruim",
                response="Resposta parcial",
                tolerability="Ruim / efeitos relevantes",
            )
        )

        self.assertEqual(assessment.adherence_status, "insufficient_adherence")
        self.assertEqual(assessment.tolerability_status, "poor_tolerability")
        self.assertEqual(assessment.optimization_possible, "not_favored")


if __name__ == "__main__":
    unittest.main()
