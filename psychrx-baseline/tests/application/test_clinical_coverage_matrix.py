import unittest

from application.clinical_coverage_matrix import ClinicalCoverageMatrix, EXPECTED_COUNTS


class ClinicalCoverageMatrixTest(unittest.TestCase):
    def setUp(self) -> None:
        self.matrix = ClinicalCoverageMatrix()

    def test_all_51_topics_reconcile_to_expected_classes(self) -> None:
        self.assertEqual(51, len(self.matrix.topics()))
        self.assertEqual(EXPECTED_COUNTS, self.matrix.summary())
        self.assertEqual((), self.matrix.validation_issues())

    def test_explicit_ui_context_is_normalized_without_diagnosis_inference(self) -> None:
        result = self.matrix.match("Transtorno bipolar - episodio depressivo")

        self.assertIsNotNone(result.topic)
        self.assertEqual("BIPOLAR_DISORDER", result.topic.canonical_context)
        self.assertEqual("covered", result.topic.coverage_class)

    def test_unmapped_context_remains_explicitly_outside_matrix(self) -> None:
        result = self.matrix.match("Outro contexto ja conhecido / nao cadastrado")

        self.assertIsNone(result.topic)
        self.assertIn("fora da matriz", result.display_line())

    def test_contextual_topics_never_claim_treatment_scope(self) -> None:
        contextual = [item for item in self.matrix.topics() if item.coverage_class == "contextual_only"]

        self.assertTrue(all(item.runtime_scope == "context_only" for item in contextual))
        self.assertTrue(all(item.priority == "no_expansion" for item in contextual))


if __name__ == "__main__":
    unittest.main()
