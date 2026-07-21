import unittest
from datetime import date

from application.patient_population_context import PatientPopulationContextService


class PatientPopulationContextServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.service = PatientPopulationContextService()
        self.reference = date(2026, 7, 20)

    def test_calculates_age_without_frontend_trust(self) -> None:
        result = self.service.assess(
            birth_date="1980-07-21",
            sex_context="female",
            weight_kg="72.5",
            pregnancy_status="Nao aplicavel",
            lactation_status="Nao aplicavel",
            postpartum_status="Nao aplicavel",
            renal_status="Preservada",
            hepatic_status="Preservada",
            as_of=self.reference,
        )

        self.assertEqual(45, result.age_years)
        self.assertEqual("ADULT", result.age_band)
        self.assertEqual("female", result.sex_context)
        self.assertEqual("72.5", result.weight_kg)
        self.assertEqual((), result.blocking_warnings)

    def test_child_and_adolescent_require_population_review(self) -> None:
        child = self._assess(birth_date="2018-01-01")
        adolescent = self._assess(birth_date="2010-01-01")

        self.assertEqual("CHILD", child.age_band)
        self.assertEqual("ADOLESCENT", adolescent.age_band)
        self.assertTrue(child.blocking_warnings)
        self.assertTrue(adolescent.blocking_warnings)

    def test_older_adult_requires_population_review(self) -> None:
        result = self._assess(birth_date="1940-01-01")

        self.assertEqual("OLDER_ADULT", result.age_band)
        self.assertIn("Pessoa idosa", result.blocking_warnings[0])

    def test_missing_or_future_birth_date_is_unknown(self) -> None:
        missing = self._assess(birth_date="")
        future = self._assess(birth_date="2030-01-01")

        self.assertEqual("UNKNOWN", missing.age_band)
        self.assertEqual("UNKNOWN", future.age_band)
        self.assertIn("Idade: Nao avaliada", missing.blocking_warnings)

    def test_postpartum_context_requires_specific_review(self) -> None:
        result = self.service.assess(
            birth_date="1990-01-01",
            pregnancy_status="Negado",
            lactation_status="Negado",
            postpartum_status="Presente",
            renal_status="Preservada",
            hepatic_status="Preservada",
            as_of=self.reference,
        )

        self.assertIn("Periodo pos-parto", result.blocking_warnings[0])

    def test_unassessed_or_altered_organ_function_blocks_routine_flow(self) -> None:
        missing = self.service.assess(
            birth_date="1980-01-01",
            pregnancy_status="Nao aplicavel",
            lactation_status="Nao aplicavel",
            postpartum_status="Nao aplicavel",
            as_of=self.reference,
        )
        altered = self.service.assess(
            birth_date="1980-01-01",
            pregnancy_status="Nao aplicavel",
            lactation_status="Nao aplicavel",
            postpartum_status="Nao aplicavel",
            renal_status="Alterada",
            hepatic_status="Preservada",
            as_of=self.reference,
        )

        self.assertTrue(any("Funcao renal: Nao avaliada" in item for item in missing.blocking_warnings))
        self.assertTrue(any("Funcao renal alterada" in item for item in altered.blocking_warnings))

    def test_unassessed_perinatal_context_is_not_inferred_as_safe(self) -> None:
        result = self.service.assess(
            birth_date="1980-01-01",
            renal_status="Preservada",
            hepatic_status="Preservada",
            as_of=self.reference,
        )

        self.assertIn("Gestacao: Nao avaliada", result.blocking_warnings)
        self.assertIn("Lactacao: Nao avaliada", result.blocking_warnings)
        self.assertIn("Periodo pos-parto: Nao avaliada", result.blocking_warnings)

    def _assess(self, *, birth_date: str):
        return self.service.assess(
            birth_date=birth_date,
            pregnancy_status="Nao aplicavel",
            lactation_status="Nao aplicavel",
            postpartum_status="Nao aplicavel",
            renal_status="Preservada",
            hepatic_status="Preservada",
            as_of=self.reference,
        )


if __name__ == "__main__":
    unittest.main()
