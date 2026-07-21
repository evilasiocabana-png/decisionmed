import unittest

from application.medication_population_evidence_table import (
    MedicationPopulationEvidenceTable,
)


class MedicationPopulationEvidenceTableTest(unittest.TestCase):
    def setUp(self) -> None:
        self.table = MedicationPopulationEvidenceTable()

    def test_returns_child_and_older_adult_evidence(self) -> None:
        child = self.table.for_medication("Sertralina", "CHILD")
        older = self.table.for_medication("Sertralina", "OLDER_ADULT")

        self.assertIsNotNone(child)
        self.assertIsNotNone(older)
        self.assertEqual("DM", child.source_abbreviation)
        self.assertFalse(child.therapeutic_runtime_eligible)
        self.assertIn("(DM)", child.display_line())
        self.assertIn("Faixa/informacao por idade:", child.display_line())
        self.assertIn(child.dosage_summary, child.display_line())

    def test_uses_alternate_official_source_when_dailymed_is_absent(self) -> None:
        bromazepam = self.table.for_medication("Bromazepam", "OLDER_ADULT")
        zopiclone = self.table.for_medication("Zopiclona", "ADOLESCENT")

        self.assertEqual("HC", bromazepam.source_abbreviation)
        self.assertEqual("UK-SMPC", zopiclone.source_abbreviation)
        self.assertTrue(bromazepam.source_url.startswith("https://pdf.hres.ca/"))

    def test_returns_one_row_per_medication_in_requested_band(self) -> None:
        rows = self.table.for_medications(
            ("Sertralina", "Sertralina", "Agomelatina"), "ADULT"
        )

        self.assertEqual(2, len(rows))
        self.assertEqual({"DM", "EMA"}, {row.source_abbreviation for row in rows})


if __name__ == "__main__":
    unittest.main()
