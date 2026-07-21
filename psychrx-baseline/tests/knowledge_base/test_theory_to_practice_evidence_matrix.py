from __future__ import annotations

import csv
import unittest
from pathlib import Path


TABLE_DIR = (
    Path(__file__).resolve().parents[2]
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
)


class TheoryToPracticeEvidenceMatrixTests(unittest.TestCase):
    @staticmethod
    def _rows(name: str) -> list[dict[str, str]]:
        with (TABLE_DIR / name).open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_theory_matrix_separates_didactic_and_official_sources(self) -> None:
        rows = self._rows("theory_to_practice_matrix.csv")

        self.assertGreaterEqual(len(rows), 15)
        self.assertTrue(all(row["didactic_source"] for row in rows))
        self.assertTrue(all(row["official_source_url"] for row in rows))
        self.assertTrue(all(row["runtime_eligible"] == "false" for row in rows))
        self.assertTrue(any(row["theoretical_topic"] == "Ensaio antidepressivo adequado" for row in rows))

    def test_official_claim_matrix_covers_all_motor_medications(self) -> None:
        claims = self._rows("medication_official_claims.csv")
        gaps = self._rows("medication_evidence_gap_matrix.csv")

        self.assertEqual(len(claims), 83)
        self.assertEqual(
            {row["medication_name"] for row in claims},
            {row["medication_name"] for row in gaps},
        )
        self.assertTrue(all(row["runtime_eligible"] == "false" for row in claims))
        self.assertGreaterEqual(
            sum(row["extraction_status"] == "official_claim_anchors_extracted" for row in claims),
            70,
        )
        amisulpride = next(row for row in claims if row["medication_name"] == "Amissulprida")
        self.assertEqual(
            amisulpride["extraction_status"],
            "official_source_context_mismatch_rejected",
        )
        self.assertFalse(amisulpride["dosage_excerpt"])
        self.assertFalse(amisulpride["mechanism_excerpt"])

    def test_disease_use_review_preserves_every_original_relationship(self) -> None:
        original = self._rows("medication_disease_use_matrix.csv")
        review = self._rows("medication_disease_use_evidence_review.csv")

        self.assertEqual(len(review), len(original))
        self.assertTrue(all(row["evidence_review_status"] for row in review))
        self.assertTrue(all(row["runtime_eligible"] == "false" for row in review))

    def test_motor2_gap_review_classifies_every_row_without_inventing_ranges(self) -> None:
        motor2 = self._rows("motor2_strategy_matrix.csv")
        review = self._rows("motor2_gap_resolution_matrix.csv")

        self.assertEqual(len(review), len(motor2))
        self.assertTrue(all(row["range_resolution_status"] for row in review))
        self.assertTrue(all(row["mechanism_resolution_status"] for row in review))
        self.assertTrue(all(row["runtime_eligible"] == "false" for row in review))
        no_relationship = [
            row
            for row in review
            if row["range_resolution_status"]
            == "no_supported_relationship_registered_do_not_invent_range"
        ]
        self.assertTrue(no_relationship)
        self.assertTrue(all(not row["official_dosage_candidate"] for row in no_relationship))


if __name__ == "__main__":
    unittest.main()
