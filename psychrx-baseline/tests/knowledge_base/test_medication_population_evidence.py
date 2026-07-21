import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TABLE_PATH = (
    ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "medication_population_evidence.csv"
)


class MedicationPopulationEvidenceCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with TABLE_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_catalog_is_complete_for_all_medications_and_age_bands(self) -> None:
        medications = {row["medication_name"] for row in self.rows}
        bands = {row["age_band"] for row in self.rows}

        self.assertEqual(83, len(medications))
        self.assertEqual(332, len(self.rows))
        self.assertEqual(
            {"CHILD", "ADOLESCENT", "ADULT", "OLDER_ADULT"}, bands
        )
        self.assertTrue(
            all(
                sum(
                    row["medication_name"] == medication
                    and row["age_band"] == band
                    for row in self.rows
                )
                == 1
                for medication in medications
                for band in bands
            )
        )

    def test_every_row_has_official_source_and_population_summary(self) -> None:
        approved_hosts = (
            "dailymed.nlm.nih.gov",
            "ema.europa.eu",
            "medicines.org.uk",
            "pdf.hres.ca",
        )
        self.assertTrue(all(row["population_summary"] for row in self.rows))
        self.assertTrue(all(row["population_anchor"] for row in self.rows))
        self.assertTrue(all(row["source_title"] for row in self.rows))
        self.assertTrue(
            all(any(host in row["source_url"] for host in approved_hosts) for row in self.rows)
        )
        self.assertTrue(all(row["content_sha256"] for row in self.rows))

    def test_source_display_does_not_enable_therapeutic_runtime(self) -> None:
        self.assertTrue(all(row["display_eligible"] == "true" for row in self.rows))
        self.assertTrue(
            all(row["therapeutic_runtime_eligible"] == "false" for row in self.rows)
        )
        self.assertTrue(
            all("official" in row["scientific_review_status"] for row in self.rows)
        )

    def test_bounded_fallback_does_not_capture_packaging_or_excipients(self) -> None:
        fallback_text = " ".join(
            row["population_summary"]
            for row in self.rows
            if row["evidence_status"] == "official_population_text_located"
        ).upper()

        for packaging_term in (
            "MAGNESIUM STEARATE",
            "LACTOSE MONOHYDRATE",
            "TITANIUM DIOXIDE",
        ):
            self.assertNotIn(packaging_term, fallback_text)


if __name__ == "__main__":
    unittest.main()
