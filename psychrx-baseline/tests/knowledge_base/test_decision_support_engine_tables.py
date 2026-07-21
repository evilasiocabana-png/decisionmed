import csv
import re
import unittest
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET


ROOT = Path("knowledge_base/decision_support_engine")


class DecisionSupportEngineTablesTest(unittest.TestCase):
    def test_engine_table_folder_exists(self) -> None:
        self.assertTrue((ROOT / "README.md").is_file())
        self.assertTrue((ROOT / "docs" / "ENGINEERING_REVERSE_WORKFLOW.md").is_file())
        self.assertTrue((ROOT / "schemas" / "TABLE_SCHEMA.md").is_file())

    def test_motor_research_source_policy_registers_official_sources(self) -> None:
        policy = Path("docs/decision_support_engine/MOTOR_RESEARCH_SOURCE_POLICY.md")
        self.assertTrue(policy.is_file())
        text = policy.read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        for source in (
            "Stahl's Essential Psychopharmacology",
            "Stahl's Prescriber's Guide",
            "Goodman & Gilman's The Pharmacological Basis of Therapeutics",
            "American Psychiatric Association Guidelines",
            "NICE Guidelines",
            "FDA / DailyMed",
            "EMA",
            "ANVISA",
        ):
            self.assertIn(source, text)

        self.assertIn("PENDENTE_PESQUISAR", text)
        self.assertIn("MOTOR_RESEARCH_SOURCE_POLICY.md", readme)

    def test_medication_strategy_table_has_required_columns_and_rows(self) -> None:
        rows = self._read_csv(ROOT / "tables" / "medication_strategy_table.csv")

        self.assertGreaterEqual(len(rows), 6)
        self.assert_required_columns(
            rows,
            {
                "drug_id",
                "drug_name",
                "drug_class",
                "targets",
                "usual_adult_range",
                "source_id",
                "source_title",
                "source_section",
                "source_url",
                "cautions",
                "substitution_fit",
                "association_fit",
                "status",
            },
        )
        self.assertIn("Sertralina", {row["drug_name"] for row in rows})
        self.assertTrue(all(row["source_url"].startswith("https://") for row in rows))

    def test_decision_rules_reference_question_fields(self) -> None:
        questions = self._read_csv(ROOT / "tables" / "question_derivation_matrix.csv")
        rules = self._read_csv(ROOT / "tables" / "decision_rules.csv")
        question_ids = {row["field_id"] for row in questions}

        for rule in rules:
            required = {
                field.strip()
                for field in rule["required_fields"].split("|")
                if field.strip()
            }
            missing = required - question_ids - {"safety"}
            self.assertEqual(missing, set(), f"{rule['rule_id']} has missing fields")

    def test_safety_gate_questions_are_prioritized(self) -> None:
        rows = self._read_csv(ROOT / "tables" / "safety_gate_questions.csv")
        priorities = [int(row["priority"]) for row in rows]

        self.assertEqual(priorities, sorted(priorities))
        self.assertEqual(rows[0]["safety_field"], "suicide")

    def test_toxidrome_screening_matrix_is_source_anchored_and_non_prescriptive(self) -> None:
        rows = self._read_csv(ROOT / "tables" / "toxidrome_screening_matrix.csv")
        self.assertGreaterEqual(len(rows), 10)
        self.assert_required_columns(
            rows,
            {
                "signal_id",
                "ui_label",
                "pattern_hint",
                "motor_action",
                "source_id",
                "source_section",
                "source_url",
                "validation_status",
                "runtime_scope",
                "toxidrome_definition",
                "antidote_or_specific_measure",
                "emergency_boundary",
            },
        )
        self.assertTrue(
            all(
                row["runtime_scope"]
                in {"screening_only", "screening_and_countermeasure_display"}
                for row in rows
            )
        )
        self.assertTrue(all(row["source_id"] for row in rows))
        self.assertTrue(any("Naloxona" in row["antidote_or_specific_measure"] for row in rows))
        self.assertTrue(any("Atropina" in row["antidote_or_specific_measure"] for row in rows))
        self.assertTrue(any("fisostigmina" in row["antidote_or_specific_measure"].lower() for row in rows))
        self.assertTrue(any("pralidoxima" in row["antidote_or_specific_measure"].lower() for row in rows))
        self.assertTrue(
            all(
                row["emergency_boundary"].startswith("Nao ")
                or row["signal_id"] == "NONE"
                for row in rows
            )
        )

    def test_antidepressant_indication_matrix_table1_has_founder_headers(self) -> None:
        rows = self._read_csv(
            ROOT / "tables" / "antidepressant_indication_matrix_table1.csv"
        )
        expected = {
            "medicamento",
            "dose_referencia_linha",
            "TAG",
            "TAG_visual_status",
            "panico",
            "transtorno_de_estresse",
            "fobias",
            "fobia_social",
            "TOC",
            "depressao_melancolica",
            "depressao_ansiosa",
            "depressao_com_agitacao_agressiva",
            "depressao_atipica",
            "dor",
            "vicios",
            "tabagismo",
            "compulsao",
            "bulimia_anorexia",
            "TDPM",
            "ideacao_suicida",
        }

        self.assert_required_columns(rows, expected)
        self.assertIn("Sertralina", {row["medicamento"] for row in rows})
        self.assertIn("Venlafaxina", {row["medicamento"] for row in rows})
        by_medication = {row["medicamento"]: row for row in rows}
        self.assertEqual(by_medication["Desvenlafaxina"]["dose_referencia_linha"], "50-100")
        self.assertEqual(by_medication["Duloxetina"]["dose_referencia_linha"], "60-120")
        self.assertEqual(by_medication["Citalopram"]["dose_referencia_linha"], "20-40")
        self.assertEqual(by_medication["Escitalopram"]["dose_referencia_linha"], "10-20")
        self.assertEqual(by_medication["Bupropiona"]["dose_referencia_linha"], "150-300")
        self.assertEqual(
            by_medication["Desvenlafaxina"]["TAG_visual_status"],
            "visual_present_no_dose_transcribed",
        )
        self.assertEqual(
            by_medication["Bupropiona"]["TAG_visual_status"],
            "blank_or_not_indicated",
        )

    def test_antidepressant_priority_matrix_table1_has_legend_values(self) -> None:
        rows = self._read_csv(
            ROOT / "tables" / "antidepressant_priority_matrix_table1.csv"
        )
        allowed = {"muito_alta", "alta", "moderada", "baixa", "evitar", ""}
        expected = {
            "medicamento",
            "TAG",
            "panico",
            "transtorno_de_estresse",
            "fobias",
            "fobia_social",
            "TOC",
            "depressao_melancolica",
            "depressao_ansiosa",
            "depressao_com_agitacao_agressiva",
            "depressao_atipica",
            "dor",
            "vicios",
            "tabagismo",
            "compulsao",
            "bulimia_anorexia",
            "TDPM",
            "ideacao_suicida",
        }

        self.assert_required_columns(rows, expected)
        self.assertEqual(len(rows), 23)
        for row in rows:
            for key, value in row.items():
                if key != "medicamento":
                    self.assertIn(value, allowed, f"{row['medicamento']} {key}")

        by_medication = {row["medicamento"]: row for row in rows}
        self.assertEqual(by_medication["Venlafaxina"]["TAG"], "muito_alta")
        self.assertEqual(by_medication["Venlafaxina"]["panico"], "muito_alta")
        self.assertEqual(by_medication["Desvenlafaxina"]["panico"], "moderada")
        self.assertEqual(by_medication["Duloxetina"]["panico"], "moderada")
        self.assertEqual(by_medication["Doxepina"]["panico"], "muito_alta")
        self.assertEqual(by_medication["Duloxetina"]["TAG"], "alta")
        self.assertEqual(by_medication["Nortriptilina"]["TAG"], "moderada")
        self.assertEqual(by_medication["Maprotilina"]["TAG"], "alta")
        self.assertEqual(by_medication["Maprotilina"]["transtorno_de_estresse"], "alta")
        self.assertEqual(by_medication["Paroxetina"]["TAG"], "alta")
        self.assertEqual(by_medication["Venlafaxina"]["fobias"], "alta")
        self.assertEqual(by_medication["Duloxetina"]["fobias"], "baixa")
        self.assertEqual(by_medication["Maprotilina"]["fobias"], "baixa")
        self.assertEqual(by_medication["Vortioxetina"]["fobias"], "alta")
        self.assertEqual(by_medication["Fluoxetina"]["depressao_melancolica"], "moderada")
        self.assertEqual(by_medication["Sertralina"]["TOC"], "muito_alta")
        self.assertEqual(by_medication["Bupropiona"]["fobias"], "evitar")

    def test_antidepressant_first_choice_matrix_table1_marks_icon_cells(self) -> None:
        rows = self._read_csv(
            ROOT / "tables" / "antidepressant_first_choice_matrix_table1.csv"
        )
        allowed = {"primeira_escolha", ""}
        expected = {
            "medicamento",
            "TAG",
            "panico",
            "transtorno_de_estresse",
            "fobias",
            "fobia_social",
            "TOC",
            "depressao_melancolica",
            "depressao_ansiosa",
            "depressao_com_agitacao_agressiva",
            "depressao_atipica",
            "dor",
            "vicios",
            "tabagismo",
            "compulsao",
            "bulimia_anorexia",
            "TDPM",
            "ideacao_suicida",
        }

        self.assert_required_columns(rows, expected)
        self.assertEqual(len(rows), 23)
        for row in rows:
            for key, value in row.items():
                if key != "medicamento":
                    self.assertIn(value, allowed, f"{row['medicamento']} {key}")

        by_medication = {row["medicamento"]: row for row in rows}
        self.assertEqual(
            by_medication["Venlafaxina"]["depressao_melancolica"],
            "primeira_escolha",
        )
        self.assertEqual(
            by_medication["Escitalopram"]["transtorno_de_estresse"],
            "primeira_escolha",
        )
        self.assertEqual(by_medication["Duloxetina"]["dor"], "primeira_escolha")
        self.assertEqual(by_medication["Bupropiona"]["tabagismo"], "primeira_escolha")

    def test_pharmacological_decision_matrix_supports_profile_ranking(self) -> None:
        rows = self._read_csv(ROOT / "tables" / "pharmacological_decision_matrix.csv")
        expected = {
            "drug_id",
            "drug_name",
            "drug_class",
            "therapeutic_targets",
            "fit_energy",
            "fit_anxiety",
            "fit_sleep",
            "fit_pain",
            "fit_weight_neutral",
            "fit_libido",
            "fit_mood_stabilization",
            "fit_psychosis",
            "fit_impulsivity",
            "cautions",
            "preferred_contexts",
            "source_tabs",
            "status",
        }

        self.assertGreaterEqual(len(rows), 12)
        self.assert_required_columns(rows, expected)
        by_medication = {row["drug_name"]: row for row in rows}
        self.assertEqual(by_medication["Duloxetina"]["fit_pain"], "5")
        self.assertEqual(by_medication["Bupropiona XL"]["fit_energy"], "5")
        self.assertEqual(by_medication["Mirtazapina"]["fit_sleep"], "5")
        self.assertEqual(by_medication["Quetiapina"]["fit_sleep"], "5")
        self.assertEqual(by_medication["Lamotrigina"]["fit_mood_stabilization"], "4")

    def test_medication_explanation_profile_backlog_is_not_runtime_active(self) -> None:
        matrix_rows = self._read_csv(ROOT / "tables" / "pharmacological_decision_matrix.csv")
        rows = self._read_csv(
            ROOT / "tables" / "medication_explanation_profile_backlog.csv"
        )
        expected = {
            "medication_id",
            "medication_name",
            "drug_class",
            "dose_band",
            "dominant_effect",
            "pharmacological_target",
            "receptor_or_mechanism",
            "anxiety_score",
            "sleep_score",
            "mood_score",
            "energy_score",
            "cognition_score",
            "sedation_risk",
            "weight_gain_risk",
            "extrapyramidal_risk",
            "explanation_for_motor",
            "current_source_status",
            "source_required",
            "source_reference",
            "integration_status",
            "drug_class_source",
            "dose_band_source",
            "dominant_effect_source",
            "pharmacological_target_source",
            "receptor_or_mechanism_source",
            "anxiety_score_source",
            "sleep_score_source",
            "mood_score_source",
            "energy_score_source",
            "cognition_score_source",
            "sedation_risk_source",
            "weight_gain_risk_source",
            "extrapyramidal_risk_source",
            "source_legend",
        }

        self.assert_required_columns(rows, expected)
        matrix_medications = {row["drug_name"] for row in matrix_rows}
        backlog_medications = {row["medication_name"] for row in rows}
        self.assertEqual(backlog_medications, matrix_medications)
        self.assertGreaterEqual(len(rows), len(matrix_medications))
        self.assertTrue(
            all(
                row["current_source_status"]
                in {
                    "pending_source_validation",
                    "partial_from_motor_matrix",
                    "source_located_pending_review",
                    "source_reference_mapped_pending_formal_review",
                    "official_label_located_pending_formal_review",
                    "official_label_located_context_mismatch_review_required",
                }
                for row in rows
            )
        )
        self.assertTrue(all(row["integration_status"] == "backlog_only" for row in rows))
        self.assertTrue(all(row["dose_band"] for row in rows))
        self.assertFalse(any(row["dose_band"] == "PENDENTE_PESQUISAR" for row in rows))
        pending_source_statuses = {
            "source_located_pending_review",
            "source_reference_mapped_pending_formal_review",
            "official_label_located_pending_formal_review",
            "official_label_located_context_mismatch_review_required",
        }
        self.assertTrue(all(row["current_source_status"] in pending_source_statuses for row in rows))
        self.assertTrue(all(row["source_reference"] for row in rows))
        self.assertTrue(any(row["sedation_risk"] == "nao cadastrado" for row in rows))
        self.assertEqual(len(rows), len(matrix_medications))
        self.assertTrue(
            any(
                "25" in row["dose_band"] and "100 mg/dia" in row["dose_band"]
                for row in rows
                if row["medication_name"] == "Quetiapina"
            )
        )
        self.assertTrue(
            any(
                "15 mg/dia" in row["dose_band"]
                for row in rows
                if row["medication_name"] == "Mirtazapina"
            )
        )
        source_pairs = {
            "drug_class": "drug_class_source",
            "pharmacological_target": "pharmacological_target_source",
            "anxiety_score": "anxiety_score_source",
            "sleep_score": "sleep_score_source",
            "mood_score": "mood_score_source",
            "energy_score": "energy_score_source",
        }
        for row in rows:
            self.assertIn("DM=DailyMed/FDA", row["source_legend"])
            for value_field, source_field in source_pairs.items():
                self.assertNotEqual(row[value_field], "")
                self.assertNotEqual(row[source_field], "")

    def test_unified_workbook_contains_dose_profile_sheet_for_all_medications(self) -> None:
        workbook = ROOT / "tables" / "Tabela_Motor_Unificada_audit_evilasio.xlsx"
        rows = self._read_csv(
            ROOT / "tables" / "medication_explanation_profile_backlog.csv"
        )

        with ZipFile(workbook) as archive:
            workbook_xml = ET.fromstring(archive.read("xl/workbook.xml"))
            namespace = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
            sheet_names = [
                sheet.attrib["name"]
                for sheet in workbook_xml.findall(".//a:sheet", namespace)
            ]

        self.assertIn("Dose - Efeito", sheet_names)
        self.assertIn("Regras Perfil Dose", sheet_names)
        self.assertIn("Motor 2 - Estrategia", sheet_names)
        self.assertEqual(len(rows), 83)
        self.assertTrue({"Alprazolam", "Buspirona", "Paliperidona"}.issubset({row["medication_name"] for row in rows}))

    def test_medication_disease_use_matrix_covers_all_motor_medications(self) -> None:
        matrix_rows = self._read_csv(ROOT / "tables" / "pharmacological_decision_matrix.csv")
        rows = self._read_csv(ROOT / "tables" / "medication_disease_use_matrix.csv")
        expected = {
            "medication_name",
            "disease_or_context",
            "role",
            "status",
            "phase",
            "notes",
            "source_reference",
            "review_status",
        }

        self.assert_required_columns(rows, expected)
        self.assertEqual(
            {row["medication_name"] for row in rows},
            {row["drug_name"] for row in matrix_rows},
        )
        self.assertGreaterEqual(len(rows), 200)
        self.assertTrue(
            any(
                row["medication_name"] == "Quetiapina"
                and row["disease_or_context"] == "Transtorno bipolar - episodio depressivo"
                for row in rows
            )
        )
        self.assertTrue(
            any(
                row["medication_name"] == "Clozapina"
                and row["disease_or_context"] == "Esquizofrenia resistente"
                and row["role"] == "tratamento_esquizofrenia_resistente"
                for row in rows
            )
        )

    def test_medication_source_legend_documents_abbreviations(self) -> None:
        rows = self._read_csv(ROOT / "tables" / "medication_source_legend.csv")
        codes = {row["code"] for row in rows}

        self.assertTrue({"TM", "DM", "ST-E", "ST-PG", "GG", "APA", "NICE", "EMA", "ANVISA", "HC"}.issubset(codes))
        self.assertTrue({"Maudsley", "CANMAT/ISBD", "WFSBP", "BNF", "Cochrane", "PubMed"}.issubset(codes))
        self.assertIn("PENDENTE_PESQUISAR", codes)

    def test_motor_display_fields_show_source_abbreviations_when_sourced(self) -> None:
        marker = re.compile(
            r"\((?:DM|HC|ST-E|ST-PG|GG|TM|T\d|APA|NICE|EMA|ANVISA|"
            r"CANMAT|ISBD|WFSBP|BNF|Maudsley|Cochrane|PubMed|PENDENTE)[^)]*\)"
        )
        placeholders = {
            "",
            "nao cadastrado",
            "não cadastrado",
            "pendente pesquisar",
            "PENDENTE_PESQUISAR",
        }

        profile_rows = self._read_csv(
            ROOT / "tables" / "medication_explanation_profile_backlog.csv"
        )
        for row in profile_rows:
            for field, source_field in {
                "dose_band": "dose_band_source",
                "dominant_effect": "dominant_effect_source",
                "pharmacological_target": "pharmacological_target_source",
                "receptor_or_mechanism": "receptor_or_mechanism_source",
            }.items():
                value = row[field].strip()
                if value in placeholders or not row[source_field].strip():
                    continue
                self.assertRegex(value, marker, f"{row['medication_name']} {field}")

        motor2_rows = self._read_csv(ROOT / "tables" / "motor2_strategy_matrix.csv")
        for row in motor2_rows:
            for field, source_field in {
                "dose_effect_band": "dose_effect_source",
                "dominant_effect": "dose_effect_source",
                "mechanism_or_target": "dose_effect_source",
                "condition_range": "range_source",
            }.items():
                value = row[field].strip()
                if value in placeholders or not row[source_field].strip():
                    continue
                self.assertRegex(value, marker, f"{row['medication_name']} {field}")

    def test_official_source_registry_covers_motor_medications_without_runtime_claims(self) -> None:
        matrix_rows = self._read_csv(ROOT / "tables" / "pharmacological_decision_matrix.csv")
        rows = self._read_csv(ROOT / "tables" / "medication_official_source_registry.csv")
        expected = {
            "medication_name",
            "official_query",
            "source_system",
            "source_status",
            "setid",
            "title",
            "published_date",
            "spl_version",
            "label_url",
            "service_url",
            "query_url",
            "source_use",
            "review_status",
            "notes",
        }

        self.assert_required_columns(rows, expected)
        self.assertEqual(
            {row["medication_name"] for row in rows},
            {row["drug_name"] for row in matrix_rows},
        )
        self.assertGreaterEqual(
            sum(
                row["source_status"]
                in {
                    "official_label_located_pending_formal_review",
                    "official_label_located_context_mismatch_review_required",
                }
                for row in rows
            ),
            70,
        )
        self.assertTrue(
            all(
                row["review_status"]
                in {
                    "source_locator_only_no_clinical_claim_extracted",
                    "source_locator_context_mismatch_no_clinical_claim_extracted",
                    "official_source_not_found_in_dailymed",
                }
                for row in rows
            )
        )
        self.assertTrue(all(row["query_url"].startswith("https://dailymed.nlm.nih.gov") for row in rows))
        self.assertTrue(
            any(
                row["medication_name"] == "Amissulprida"
                and row["source_status"] == "official_label_located_context_mismatch_review_required"
                for row in rows
            )
        )

    def test_medication_explanation_pending_audit_covers_all_motor_medications(self) -> None:
        matrix_rows = self._read_csv(ROOT / "tables" / "pharmacological_decision_matrix.csv")
        audit_rows = self._read_csv(
            ROOT / "tables" / "medication_explanation_pending_audit.csv"
        )
        expected = {
            "medication_id",
            "medication_name",
            "drug_class",
            "backlog_rows",
            "known_fields",
            "pending_fields",
            "not_registered_fields",
            "source_reference",
            "source_status",
            "next_research_need",
        }

        self.assert_required_columns(audit_rows, expected)
        self.assertEqual(
            {row["medication_name"] for row in audit_rows},
            {row["drug_name"] for row in matrix_rows},
        )
        self.assertTrue(all(row["pending_fields"] for row in audit_rows))
        self.assertTrue(any(row["not_registered_fields"] for row in audit_rows))
        self.assertIn(
            "dominant_effect",
            {field for row in audit_rows for field in row["pending_fields"].split(" | ")},
        )
        self.assertIn(
            "sedation_risk",
            {field for row in audit_rows for field in row["not_registered_fields"].split(" | ")},
        )

    def assert_required_columns(self, rows, columns: set[str]) -> None:
        self.assertTrue(rows)
        self.assertTrue(columns.issubset(rows[0].keys()))

    def _read_csv(self, path: Path) -> list[dict[str, str]]:
        self.assertTrue(path.is_file(), f"Missing {path}")
        with path.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
