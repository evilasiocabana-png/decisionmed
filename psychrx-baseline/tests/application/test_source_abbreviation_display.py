import unittest

from application.medication_disease_use_table import MedicationDiseaseUseTable


class SourceAbbreviationDisplayTest(unittest.TestCase):
    def test_official_label_match_uses_regulatory_abbreviation(self) -> None:
        uses = MedicationDiseaseUseTable().all_uses_for("Sertralina")
        depression = next(
            item for item in uses if item.disease_or_context == "Transtorno depressivo maior"
        )

        self.assertEqual("DM", depression.source_abbreviation)
        self.assertTrue(depression.display_line().endswith("(DM)"))

    def test_pending_mapping_does_not_look_officially_validated(self) -> None:
        uses = MedicationDiseaseUseTable().all_uses_for("Agomelatina")
        depression = next(
            item for item in uses if item.disease_or_context == "Transtorno depressivo maior"
        )

        self.assertEqual("NICE/PENDENTE", depression.source_abbreviation)
        self.assertTrue(depression.display_line().endswith("(NICE/PENDENTE)"))

    def test_missing_support_remains_explicit(self) -> None:
        uses = MedicationDiseaseUseTable().all_uses_for("Sertralina")
        anxiety = next(
            item
            for item in uses
            if item.disease_or_context == "Transtorno de ansiedade generalizada"
        )

        self.assertEqual("PENDENTE", anxiety.source_abbreviation)
        self.assertTrue(anxiety.display_line().endswith("(PENDENTE)"))


if __name__ == "__main__":
    unittest.main()
