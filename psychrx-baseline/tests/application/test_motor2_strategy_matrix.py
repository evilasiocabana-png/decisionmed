import unittest

from application.motor2_strategy_matrix import Motor2StrategyMatrix


class Motor2StrategyMatrixTest(unittest.TestCase):
    def test_motor2_matrix_contains_dose_effect_crossing(self) -> None:
        matrix = Motor2StrategyMatrix()

        rows = matrix.rows_for("Amissulprida")

        self.assertTrue(rows)
        self.assertTrue(any("50-300" in row.dose_effect_band for row in rows))
        self.assertTrue(any(row.mechanism_or_target for row in rows))
        self.assertFalse(
            any(
                "revisar alvo residual" in row.strategy_if_within_range_partial_response.lower()
                for row in matrix.rows()
            )
        )

    def test_missing_condition_range_uses_dose_effect_when_available(self) -> None:
        assessment = Motor2StrategyMatrix().assess(
            medication_name="Amissulprida",
            current_dose="50 mg",
            clinical_text="sintomas negativos depressivos baixa energia",
            response_state="Resposta parcial",
        )

        if assessment.row and not assessment.row.has_condition_range():
            self.assertEqual(assessment.suggested_action, "optimize_current")
            self.assertEqual(assessment.dose_status, "within_dose_effect_range")
            self.assertIn("faixa por dose-efeito", assessment.strategy_text)

    def test_current_dose_inside_condition_range_is_not_increase(self) -> None:
        assessment = Motor2StrategyMatrix().assess(
            medication_name="Agomelatina",
            current_dose="50 mg",
            clinical_text="depressao com agitacao agressividade",
            response_state="Resposta parcial",
        )

        self.assertEqual(assessment.dose_status, "within_registered_range")
        self.assertEqual(assessment.suggested_action, "optimize_current")
        self.assertNotEqual(assessment.suggested_action, "increase_dose")
        self.assertIn("confirmar quais sintomas ou prejuizos permanecem", assessment.strategy_text)
        self.assertNotIn("Revisar alvo residual", assessment.strategy_text)

    def test_trazodone_insomnia_uses_registered_sleep_range(self) -> None:
        assessment = Motor2StrategyMatrix().assess(
            medication_name="Trazodona",
            current_dose="50 mg",
            clinical_text="insonia sono sedacao",
            response_state="Resposta parcial",
        )

        self.assertIsNotNone(assessment.row)
        self.assertEqual(assessment.dose_status, "within_registered_range")
        self.assertIn("25-100", assessment.row.condition_range)
        self.assertIn("DM/ST-E/GG", assessment.row.condition_range)
        self.assertNotIn("nao cadastrada", assessment.strategy_text)

    def test_qualitative_dose_effect_text_is_not_reported_as_empty_range(self) -> None:
        matrix = Motor2StrategyMatrix()
        rows = matrix.rows_for("Midazolam")
        self.assertTrue(rows)
        row = rows[0]

        if row.has_dose_effect_text() and not row.has_dose_effect_range():
            assessment = matrix.assess(
                medication_name="Midazolam",
                current_dose="5 mg",
                clinical_text="sedacao procedural urgencia",
                response_state="Resposta parcial",
            )

            self.assertEqual(assessment.dose_status, "qualitative_dose_effect_range")
            self.assertIn("dose-efeito contextual", assessment.strategy_text)

    def test_priority_real_case_medications_have_sourced_rows(self) -> None:
        matrix = Motor2StrategyMatrix()

        expected_sources = {
            "Quetiapina": "DM",
            "Divalproato": "DM",
            "Clonazepam": "DM",
            "Bromazepam": "HC",
        }

        for medication, source in expected_sources.items():
            sourced = [
                row
                for row in matrix.rows_for(medication)
                if row.has_condition_range() and row.range_source == source
            ]
            self.assertTrue(sourced, f"{medication} lacks sourced Motor 2 range")
            self.assertTrue(
                any(f"({source})" in row.condition_range for row in sourced),
                f"{medication} range does not show abbreviated source",
            )
            self.assertTrue(
                any(source in row.dose_effect_source for row in matrix.rows_for(medication)),
                f"{medication} dose-effect source missing {source}",
            )

    def test_robot_axis_preferred_candidates_have_comparable_range(self) -> None:
        matrix = Motor2StrategyMatrix()
        preferred = {
            "humor/TEPT": ["Fluoxetina", "Sertralina", "Escitalopram", "Venlafaxina", "Duloxetina"],
            "sono/sedacao": ["Trazodona", "Mirtazapina", "Quetiapina", "Zolpidem"],
            "ansiedade/resgate": ["Clonazepam", "Bromazepam", "Diazepam", "Alprazolam", "Lorazepam"],
            "impulsividade/irritabilidade": ["Divalproato", "Carbamazepina", "Quetiapina", "Risperidona"],
            "compulsividade/TOC": ["Fluvoxamina", "Sertralina", "Fluoxetina", "Clomipramina"],
            "substancias/craving": ["Naltrexona", "Acamprosato", "Buprenorfina", "Bupropiona"],
            "dor/sintomas somaticos": ["Duloxetina", "Amitriptilina", "Nortriptilina", "Venlafaxina"],
            "energia/cognicao": ["Bupropiona", "Venlafaxina", "Desvenlafaxina", "Metilfenidato IR", "Metilfenidato LP"],
            "libido/funcao sexual": ["Bupropiona", "Agomelatina", "Vortioxetina"],
            "peso/metabolico": ["Bupropiona", "Agomelatina", "Fluoxetina"],
            "estabilizacao do humor": ["Litio", "Lamotrigina", "Divalproato", "Carbamazepina"],
            "psicose/organizacao do pensamento": ["Quetiapina", "Risperidona", "Olanzapina", "Aripiprazol", "Haloperidol"],
        }

        for axis, medications in preferred.items():
            for medication in medications:
                rows = matrix.rows_for(medication)
                self.assertTrue(rows, f"{axis} candidate {medication} is missing")
                self.assertTrue(
                    any(
                        row.has_condition_range() or row.has_dose_effect_range()
                        for row in rows
                    ),
                    f"{axis} candidate {medication} has no comparable range",
                )


if __name__ == "__main__":
    unittest.main()
