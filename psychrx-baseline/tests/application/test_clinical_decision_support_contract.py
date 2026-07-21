import json
import unittest

from application.clinical_decision_support_contract import (
    ActionEvidencePayload,
    ClinicalDecisionSupportRequest,
    ClinicalDecisionSupportResponse,
    CurrentMedicationPayload,
    EvidenceCitationPayload,
    MedicationActionExplanationPayload,
    MedicationOptionPayload,
    PharmacologicalTargetPayload,
    empty_decision_support_response,
)
from application.clinical_decision_support_service import ClinicalDecisionSupportService
from application.specialized_gpt_decision_support_adapter import (
    SpecializedGPTDecisionSupportAdapter,
)


def safety_payload(**overrides):
    values = {
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
    values.update(overrides)
    return values


class ClinicalDecisionSupportContractTest(unittest.TestCase):
    def test_request_is_json_safe_and_contains_consultation_context(self) -> None:
        request = ClinicalDecisionSupportRequest(
            patient_label="Paciente teste",
            birth_date="1980-01-01",
            pregnancy_status="Nao aplicavel",
            lactation_status="Nao aplicavel",
            postpartum_status="Nao aplicavel",
            sex_context="female",
            weight_kg="72.5",
            renal_status="Preservada",
            hepatic_status="Preservada",
            clinical_context_ids=("CANNABIS_CONTEXT",),
            diagnostic_context="Depressao em acompanhamento",
            current_state="Melhora parcial, ainda sintomatico",
            symptoms=("Humor deprimido", "Insonia terminal"),
            impairment_domains=("Sono", "Trabalho"),
            current_medications=(
                CurrentMedicationPayload(
                    name="Sertralina",
                    dose_value="50",
                    dose_unit="mg",
                    frequency="1x/dia",
                ),
            ),
        )

        encoded = json.dumps(request.to_dict(), ensure_ascii=False)

        self.assertIn("Paciente teste", encoded)
        self.assertIn("Sertralina", encoded)
        self.assertIn("Sono", encoded)
        self.assertIn("1980-01-01", encoded)
        self.assertIn("postpartum_status", encoded)
        self.assertIn("CANNABIS_CONTEXT", encoded)
        self.assertIn("72.5", encoded)
        self.assertIn("clinical", request.clinician_question.lower())

    def test_response_requires_traceable_or_unresolved_action_evidence(self) -> None:
        response = ClinicalDecisionSupportResponse(
            summary="Considerar otimizacao apos revisao medica.",
            recommended_action="optimize_current",
            clinical_rationale=("Resposta parcial com prejuizo em sono.",),
            action_evidence=(
                ActionEvidencePayload(
                    action="optimize_current",
                    rationale="Acao sem fonte e sem pendencia.",
                ),
            ),
            status="ready_for_clinician_review",
        )

        self.assertIn(
            "action_evidence_untraceable:optimize_current",
            response.validate_for_display(),
        )

    def test_incomplete_per_medication_explanation_is_rejected(self) -> None:
        response = ClinicalDecisionSupportResponse(
            summary="Comparacao por medicamento.",
            recommended_action="optimize_current",
            clinical_rationale=("Resposta parcial.",),
            action_evidence=(
                ActionEvidencePayload(
                    action="optimize_current",
                    rationale="Regra estrutural.",
                    unresolved_reason="scientific_grade_pending",
                ),
            ),
            medication_action_explanations=(
                MedicationActionExplanationPayload(
                    medication_name="Sertralina",
                    maintain_reason="",
                    increase_reason="Dose em revisao.",
                    substitute_reason="Resposta em revisao.",
                    associate_reason="Eixo em revisao.",
                    evidence_level="Pendente.",
                ),
            ),
        )

        self.assertIn(
            "medication_action_explanation_incomplete:Sertralina",
            response.validate_for_display(),
        )

    def test_traceable_response_passes_structural_validation(self) -> None:
        citation = EvidenceCitationPayload(
            source_id="G001",
            title="Clinical guideline",
            organization="Example Organization",
            section="Treatment response",
            excerpt_anchor="G001-S2-P4",
        )
        response = ClinicalDecisionSupportResponse(
            summary="Conselho pronto para revisao medica.",
            recommended_action="substitute",
            clinical_rationale=("Sem resposta apesar de tratamento informado.",),
            impairment_targets=("Trabalho",),
            pharmacological_targets=(
                PharmacologicalTargetPayload(
                    impairment_domain="Trabalho",
                    symptom_target="Fadiga e anedonia",
                    pharmacological_target="Alvo humor / energia",
                    therapeutic_dose_target="Depende do medicamento escolhido.",
                    dose_source=citation,
                ),
            ),
            substitution_options=(
                MedicationOptionPayload(
                    name="Candidato definido pelo GPT especializado",
                    role="substitution_candidate",
                    reason="Perfil alinhado ao sintoma atual explicitamente informado.",
                    evidence=(citation,),
                ),
            ),
            action_evidence=(
                ActionEvidencePayload(
                    action="substitute",
                    rationale="Falha/intolerancia exige alternativa rastreavel.",
                    citations=(citation,),
                ),
            ),
            status="ready_for_clinician_review",
        )

        self.assertEqual(response.validate_for_display(), ())
        self.assertIn("substitution_candidate", json.dumps(response.to_dict()))
        self.assertIn("prescricao final", response.prescription_boundary.lower())

    def test_empty_response_is_safe_and_unresolved(self) -> None:
        response = empty_decision_support_response()

        self.assertEqual(response.status, "unresolved")
        self.assertEqual(response.recommended_action, "insufficient_information")
        self.assertEqual(response.validate_for_display(), ())

    def test_service_builds_structured_response_for_ui(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "symptoms": ["Humor deprimido", "Fadiga"],
                "impairment_domains": ["Trabalho"],
                "stability": "Sem resposta",
                "current_medications": [{"name": "Sertralina"}],
                "safety": safety_payload(),
            }
        )

        self.assertEqual(response.recommended_action, "substitute")
        self.assertEqual(response.status, "unresolved")
        self.assertEqual(response.scientific_readiness, "structural_only_scientific_review_pending")
        self.assertTrue(response.evidence_governance_summary)
        self.assertTrue(response.monitoring_governance_summary)
        self.assertTrue(response.population_evidence_summary)
        self.assertIn("Sertralina | ADULT", response.population_evidence_summary[0])
        self.assertTrue(
            any(
                name in response.substitution_options[0].name
                for name in {"Venlafaxina XR", "Duloxetina", "Bupropiona XL"}
            )
        )
        self.assertIn(
            "matriz farmacologica local",
            " ".join(response.clinical_rationale).lower(),
        )
        self.assertEqual(response.validate_for_display(), ())

    def test_service_suggests_initial_candidate_when_no_current_medication(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "clinical_presentation": "Primeira consulta",
                "symptoms": ["Humor deprimido", "Fadiga"],
                "impairment_domains": ["Trabalho", "Energia"],
                "pharmacological_profile": [
                    "baixa sedacao diurna",
                    "Humor deprimido: alvo predominante",
                ],
                "current_medications": [],
                "safety": safety_payload(),
            }
        )

        self.assertEqual(response.recommended_action, "select_candidate")
        self.assertEqual(response.status, "unresolved")
        self.assertTrue(response.substitution_options)
        self.assertEqual(response.substitution_options[0].role, "initiation_candidate")
        self.assertIn("sem medicacao atual", response.summary)
        self.assertEqual(response.validate_for_display(), ())

    def test_service_can_use_specialized_adapter_when_explicitly_enabled(self) -> None:
        class FakeAdapter:
            def request(self, payload):
                return ClinicalDecisionSupportResponse(
                    summary="Resposta do GPT especializado.",
                    recommended_action="optimize_current",
                    clinical_rationale=("Resposta parcial com prejuizo residual.",),
                    action_evidence=(
                        ActionEvidencePayload(
                            action="optimize_current",
                            rationale="Fonte pendente no teste.",
                            unresolved_reason="test_adapter",
                        ),
                    ),
                    status="unresolved",
                )

        response = ClinicalDecisionSupportService(
            specialized_adapter=FakeAdapter(),
            use_specialized_adapter=True,
        ).build_response({"stability": "Parcial"})

        self.assertEqual(response.summary, "Resposta do GPT especializado.")
        self.assertEqual(response.recommended_action, "optimize_current")

    def test_service_uses_local_rule_table_by_default_even_when_adapter_exists(self) -> None:
        class FailingAdapter:
            def request(self, payload):
                raise AssertionError("adapter should not be called by default")

        response = ClinicalDecisionSupportService(
            specialized_adapter=FailingAdapter(),
        ).build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "symptoms": ["Ansiedade", "Insonia terminal"],
                "impairment_domains": ["Sono", "Trabalho"],
                "impairment_severity": "Importante",
                "stability": "Parcial",
                "current_medications": [
                    {
                        "name": "Sertralina",
                        "dose_value": "50",
                        "dose_unit": "mg",
                        "frequency": "1x/dia",
                        "duration": "4 semanas",
                        "adherence": "Boa",
                        "response": "Resposta parcial",
                        "tolerability": "Boa",
                    }
                ],
                "safety": safety_payload(),
            }
        )

        self.assertEqual(response.recommended_action, "optimize_current")
        self.assertEqual(response.status, "unresolved")
        self.assertIn("sono", response.pharmacological_targets[0].pharmacological_target)
        self.assertIn("Sertralina", response.summary)
        self.assertIn(
            "Avaliacao da medicacao atual",
            " ".join(response.clinical_rationale),
        )
        self.assertIn(
            "dentro da faixa cadastrada",
            " ".join(response.clinical_rationale),
        )
        self.assertIn(
            "Alvo residual ainda nao confirmado longitudinalmente. "
            "Sintomas atuais a verificar como persistentes: Ansiedade, Insonia terminal.",
            response.clinical_rationale,
        )
        self.assertEqual(response.association_options[0].name, "Mirtazapina")
        self.assertEqual(response.validate_for_display(), ())

    def test_partial_response_without_symptoms_declares_residual_target_undefined(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "symptoms": [],
                "impairment_domains": ["Trabalho"],
                "stability": "Resposta parcial",
                "current_medications": [
                    {
                        "name": "Sertralina",
                        "dose_value": "50",
                        "dose_unit": "mg",
                        "frequency": "1x/dia",
                        "duration": "4 semanas",
                        "adherence": "Boa",
                        "response": "Resposta parcial",
                        "tolerability": "Boa",
                    }
                ],
                "safety": safety_payload(),
            }
        )

        rationale = " ".join(response.clinical_rationale)
        self.assertIn("Alvo residual nao definido", rationale)
        self.assertIn("registrar quais sintomas ou prejuizos persistem", rationale)
        self.assertNotIn("tratar alvo residual", rationale.lower())

    def test_each_current_medication_gets_four_reasons_and_evidence_level(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "diagnostic_context": "Transtorno de estresse",
                "clinical_presentation": "Seguimento",
                "symptoms": ["Ansiedade", "Humor deprimido"],
                "impairment_domains": ["Trabalho"],
                "clinical_axes": ["humor/TEPT", "ansiedade/resgate"],
                "stability": "Sem resposta",
                "current_medications": [
                    {
                        "name": "Sertralina",
                        "dose_value": "50",
                        "dose_unit": "mg",
                        "frequency": "1x/dia",
                        "duration": "8 semanas",
                        "adherence": "Boa",
                        "response": "Sem resposta",
                        "tolerability": "Boa",
                        "reason_for_use": "humor/TEPT",
                    },
                    {
                        "name": "Diazepam",
                        "dose_value": "5",
                        "dose_unit": "mg",
                        "frequency": "1x/dia",
                        "duration": "8 semanas",
                        "adherence": "Boa",
                        "response": "Boa resposta",
                        "tolerability": "Boa",
                        "reason_for_use": "ansiedade/resgate",
                    },
                ],
                "safety": safety_payload(),
            }
        )

        by_name = {
            item.medication_name: item
            for item in response.medication_action_explanations
        }
        self.assertEqual(set(by_name), {"Sertralina", "Diazepam"})
        self.assertIn("Favorecida para discussao medica", by_name["Sertralina"].substitute_reason)
        self.assertIsNotNone(by_name["Sertralina"].substitution_candidate)
        self.assertNotEqual(
            by_name["Sertralina"].substitution_candidate.name,
            "Sertralina",
        )
        self.assertTrue(
            by_name["Sertralina"]
            .substitution_candidate
            .has_evidence_or_unresolved_reason()
        )
        self.assertTrue(by_name["Sertralina"].substitution_candidate.dose_guidance)
        self.assertIn("mg", by_name["Sertralina"].substitution_candidate.dose_guidance)
        self.assertIn("once daily", by_name["Sertralina"].substitution_candidate.dose_guidance)
        self.assertIn("Favorecida", by_name["Diazepam"].maintain_reason)
        for item in by_name.values():
            self.assertTrue(item.maintain_reason)
            self.assertTrue(item.increase_reason)
            self.assertTrue(item.substitute_reason)
            self.assertTrue(item.associate_reason)
            self.assertTrue(item.evidence_level)
        self.assertEqual(response.validate_for_display(), ())

    def test_local_table_returns_dose_target_for_current_medication(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "symptoms": ["Humor deprimido", "Fadiga"],
                "impairment_domains": ["Trabalho"],
                "impairment_severity": "Importante",
                "stability": "Parcial",
                "current_medications": [{"name": "Sertralina"}],
                "safety": safety_payload(),
            }
        )

        target = response.pharmacological_targets[0]
        self.assertIn("Sertralina / depressao ansiosa", target.therapeutic_dose_target)
        self.assertIn("100-200", target.therapeutic_dose_target)
        self.assertIsNotNone(target.dose_source)
        self.assertTrue(target.dose_source.source_id.startswith("PSYCHRX-ABA1-DOSE-"))
        self.assertIn("Dose - efeito", target.dose_dependent_profile)
        self.assertIsNotNone(target.dose_profile_source)
        self.assertIn("Sertralina", target.dose_dependent_profile)
        self.assertTrue(response.disease_use_summary)
        self.assertTrue(
            any(
                "Transtorno depressivo maior" in item or "Quadro depressivo" in item
                for item in response.disease_use_summary
            )
        )

    def test_local_table_marks_dose_range_as_not_registered_when_absent_from_aba1(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "clinical_presentation": "Primeira consulta",
                "symptoms": ["Humor deprimido", "Fadiga"],
                "impairment_domains": ["Trabalho"],
                "pharmacological_profile": ["baixa sedacao diurna"],
                "current_medications": [],
                "safety": safety_payload(),
            }
        )

        target = response.pharmacological_targets[0]
        self.assertTrue(target.therapeutic_dose_target)
        self.assertIsNotNone(target.dose_source)
        self.assertTrue(response.phenotype_summary)

    def test_depressive_phenotype_without_closed_diagnosis_uses_conservative_filter(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "diagnostic_context": "Nao informado / em investigacao",
                "clinical_presentation": "Primeira consulta",
                "symptoms": ["Humor deprimido", "Fadiga"],
                "impairment_domains": ["Trabalho"],
                "pharmacological_profile": ["baixa sedacao diurna"],
                "current_medications": [],
                "safety": safety_payload(),
            }
        )

        self.assertEqual(response.recommended_action, "select_candidate")
        self.assertEqual(response.strategy_code, "INITIAL_MONOTHERAPY")
        self.assertIn("DEPRESSIVE_SYNDROME", " ".join(response.phenotype_summary))
        self.assertTrue(response.substitution_options)
        self.assertTrue(response.eligibility_summary)
        self.assertTrue(
            all("Quadro depressivo" in line for line in response.disease_use_summary[:1])
        )
        self.assertIn("fenotipo/quadro clinico", response.summary)
        self.assertEqual(response.validate_for_display(), ())

    def test_bipolar_or_maniform_context_blocks_antidepressant_monotherapy(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "diagnostic_context": "Transtorno bipolar em acompanhamento",
                "clinical_presentation": "Primeira consulta",
                "symptoms": ["Humor elevado", "Impulsividade"],
                "observed_signs": ["Humor elevado +++"],
                "impairment_domains": ["Estabilizacao"],
                "pharmacological_profile": ["Humor elevado: alvo predominante"],
                "current_medications": [],
                "safety": safety_payload(),
            }
        )

        names = " ".join(option.name for option in response.substitution_options)

        self.assertEqual(response.recommended_action, "select_candidate")
        self.assertIn("MANIFORM_SYNDROME", " ".join(response.phenotype_summary))
        self.assertNotIn("Fluoxetina", names)
        self.assertNotIn("Sertralina", names)
        self.assertTrue(
            all(
                option.drug_class not in {"SSRI", "SNRI", "NDRI", "NaSSA", "SARI"}
                for option in response.substitution_options
            )
        )

    def test_augmentation_only_candidate_does_not_appear_as_simple_substitution(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "diagnostic_context": "Depressao em acompanhamento",
                "clinical_presentation": "Seguimento",
                "symptoms": ["Humor deprimido", "Insonia inicial"],
                "impairment_domains": ["Sono"],
                "pharmacological_profile": ["boa acao sobre sono"],
                "stability": "Sem resposta",
                "current_medications": [{"name": "Fluoxetina"}],
                "safety": safety_payload(),
            }
        )

        substitutions = " ".join(option.name for option in response.substitution_options)
        excluded = " ".join(response.excluded_medications)

        self.assertEqual(response.strategy_code, "SWITCH_MONOTHERAPY")
        self.assertNotIn("Quetiapina", substitutions)
        self.assertIn("Quetiapina", excluded)
        self.assertIn("papel terapeutico incompativel", excluded)

    def test_local_table_returns_named_substitution_candidates(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "symptoms": ["Humor deprimido", "Fadiga"],
                "impairment_domains": ["Trabalho"],
                "impairment_severity": "Importante",
                "stability": "Sem resposta",
                "current_medications": [{"name": "Sertralina"}],
                "safety": safety_payload(),
            }
        )

        names = " ".join(option.name for option in response.substitution_options)
        self.assertIn("Venlafaxina XR", names)
        self.assertIn("Duloxetina", names)
        self.assertTrue(all(option.evidence for option in response.substitution_options))

    def test_service_ranks_medications_from_pharmacological_profile(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "clinical_presentation": "Somatica",
                "symptoms": ["Dor", "Ansiedade", "Fadiga"],
                "impairment_domains": ["Trabalho", "Sono"],
                "pharmacological_profile": [
                    "acao em sintomas somaticos",
                    "melhorar ansiedade",
                    "aumentar energia",
                    "nao ganhar peso",
                ],
                "comorbidities": ["Obesidade"],
                "safety": safety_payload(),
            }
        )

        names = " ".join(option.name for option in response.substitution_options)

        self.assertEqual(response.status, "unresolved")
        self.assertIn("Duloxetina", names)
        self.assertIn("pontuacao", response.substitution_options[0].name)
        self.assertIn("energia", response.substitution_options[0].reason)
        self.assertIn("matriz farmacologica", " ".join(response.clinical_rationale).lower())
        self.assertTrue(response.action_evidence[0].citations)
        self.assertEqual(response.validate_for_display(), ())

    def test_service_reports_risk_consequence_without_runtime_prescription(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "clinical_presentation": "Ansiosa",
                "symptoms": ["Ansiedade"],
                "impairment_domains": ["Trabalho"],
                "stability": "Parcial",
                "comorbidities": ["QT prolongado", "Fitoterapicos e suplementos"],
                "current_medications": [
                    {
                        "name": "Sertralina",
                        "dose_value": "50",
                        "dose_unit": "mg",
                        "frequency": "1x/dia",
                        "duration": "4 semanas",
                        "adherence": "Boa",
                        "response": "Resposta parcial",
                        "tolerability": "Boa",
                    }
                ],
                "safety": safety_payload(),
            }
        )

        rationale = " ".join(response.clinical_rationale)
        self.assertIn("QT prolongado -> consequencia operacional: BLOQUEAR_OPCAO", rationale)
        self.assertIn("Fitoterapicos e suplementos -> consequencia operacional: INFORMAR", rationale)
        self.assertTrue(any("QT prolongado" in item for item in response.safety_warnings))
        self.assertIn("medico permanece responsavel", response.prescription_boundary)

    def test_service_blocks_strategy_when_safety_is_not_closed(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "symptoms": ["Ansiedade"],
                "impairment_domains": ["Trabalho"],
                "stability": "Parcial",
                "current_medications": [{"name": "Sertralina"}],
                "safety": safety_payload(suicide="Nao avaliado"),
            }
        )

        self.assertEqual(response.status, "blocked")
        self.assertEqual(response.recommended_action, "investigate_before_change")
        self.assertIn("Suicidio", response.safety_warnings[0])
        self.assertEqual(len(response.medication_action_explanations), 1)
        blocked_explanation = response.medication_action_explanations[0]
        self.assertIn("prioridade de seguranca", blocked_explanation.maintain_reason)
        self.assertIn("Safety First", blocked_explanation.evidence_level)
        self.assertEqual(response.validate_for_display(), ())

    def test_special_age_band_returns_official_population_evidence_without_unlocking(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "2017-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "symptoms": ["Ansiedade"],
                "impairment_domains": ["Escola"],
                "stability": "Parcial",
                "current_medications": [{"name": "Sertralina"}],
                "safety": safety_payload(),
            }
        )

        self.assertEqual("blocked", response.status)
        self.assertTrue(response.population_evidence_summary)
        self.assertIn("Sertralina | CHILD", response.population_evidence_summary[0])
        self.assertIn("Faixa/informacao por idade:", response.population_evidence_summary[0])
        self.assertIn("(DM)", response.population_evidence_summary[0])
        self.assertIn("revisao especifica", " ".join(response.safety_warnings).lower())

    def test_blocking_clinical_context_is_applied_by_runtime(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "clinical_context_ids": ["DELIRIUM_CONCERN"],
                "symptoms": ["Humor deprimido"],
                "impairment_domains": ["Trabalho"],
                "stability": "Sem resposta",
                "safety": safety_payload(),
            }
        )

        self.assertEqual("blocked", response.status)
        self.assertIn("Delirium em avaliacao", response.safety_warnings[0])
        self.assertIn("Delirium em avaliacao", response.clinical_context_summary[0])

    def test_explicit_diagnostic_context_gets_coverage_metadata_only(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "diagnostic_context": "Transtorno bipolar - episodio depressivo",
                "symptoms": ["Humor deprimido"],
                "impairment_domains": ["Trabalho"],
                "stability": "Sem resposta",
                "safety": safety_payload(),
            }
        )

        self.assertIn("BIPOLAR_DISORDER", response.coverage_summary[0])
        self.assertIn("classe covered", response.coverage_summary[0])

    def test_service_prioritizes_urgent_assessment_for_acute_toxicity_signals(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "symptoms": ["Agitacao"],
                "observed_signs": ["Febre", "Clonus"],
                "impairment_domains": ["Seguranca aguda"],
                "stability": "Instavel",
                "current_medications": [{"name": "Sertralina"}],
                "safety": safety_payload(
                    acute_toxicity="Presente",
                    toxidrome_signals=["Febre ou hipertermia com agitacao", "Clonus"],
                ),
            }
        )

        self.assertEqual(response.status, "blocked")
        self.assertEqual(response.recommended_action, "investigate_before_change")
        self.assertIn("avaliacao medica urgente", response.summary)
        self.assertTrue(any("toxicidade/intoxicacao aguda" in item for item in response.safety_warnings))
        self.assertNotIn("antidoto", response.summary.lower())

    def test_specialized_adapter_parses_response_payload(self) -> None:
        adapter = SpecializedGPTDecisionSupportAdapter(api_key="")
        parsed = adapter._response_from_dict(
            {
                "summary": "Conselho do GPT.",
                "recommended_action": "substitute",
                "clinical_rationale": ["Sem resposta com prejuizo funcional."],
                "impairment_targets": ["Trabalho"],
                "pharmacological_targets": [
                    {
                        "impairment_domain": "Trabalho",
                        "symptom_target": "Anedonia",
                        "pharmacological_target": "humor / energia",
                        "therapeutic_dose_target": "Pendente de fonte.",
                        "unresolved_reason": "fonte pendente",
                    }
                ],
                "substitution_options": [
                    {
                        "name": "Candidato pendente",
                        "role": "substitution_candidate",
                        "reason": "Aguardando fonte.",
                        "dose_guidance": "10 mg 1x/dia",
                        "unresolved_reason": "fonte pendente",
                    }
                ],
                "association_options": [],
                "action_evidence": [
                    {
                        "action": "substitute",
                        "rationale": "Aguardando evidencia rastreavel.",
                        "unresolved_reason": "fonte pendente",
                    }
                ],
                "medication_action_explanations": [
                    {
                        "medication_name": "Sertralina",
                        "maintain_reason": "Nao favorecida sem resposta.",
                        "increase_reason": "Dose ja em faixa.",
                        "substitute_reason": "Favorecida para discussao.",
                        "associate_reason": "Nao favorecida antes da revisao.",
                        "evidence_level": "Forca comparativa nao classificada (DM).",
                        "substitution_candidate": {
                            "name": "Venlafaxina XR",
                            "role": "substitution_candidate",
                            "reason": "Candidato rastreavel.",
                            "drug_class": "SNRI",
                            "pharmacological_target": "humor / energia",
                            "unresolved_reason": "candidate_source_pending",
                        },
                    }
                ],
                "status": "unresolved",
            }
        )

        self.assertEqual(parsed.summary, "Conselho do GPT.")
        self.assertEqual(parsed.substitution_options[0].dose_guidance, "10 mg 1x/dia")
        self.assertEqual(
            parsed.medication_action_explanations[0].medication_name,
            "Sertralina",
        )
        self.assertEqual(
            parsed.medication_action_explanations[0].substitution_candidate.name,
            "Venlafaxina XR",
        )
        self.assertEqual(
            parsed.medication_action_explanations[0].substitution_candidate.drug_class,
            "SNRI",
        )
        self.assertEqual(parsed.validate_for_display(), ())

    def test_specialized_adapter_uses_psiquiatria_gpt_identity(self) -> None:
        adapter = SpecializedGPTDecisionSupportAdapter(api_key="")
        prompt = adapter._system_prompt()

        self.assertIn("Psiquiatria", prompt)
        self.assertIn("g-6a35c1c8f6208191a7c2c64201451179-psiquiatria", prompt)
        self.assertIn("suporte a decisao psicofarmacologica", prompt)

    def test_specialized_adapter_diagnostic_status_explains_missing_key(self) -> None:
        adapter = SpecializedGPTDecisionSupportAdapter(api_key="")
        status = adapter.diagnostic_status()

        self.assertEqual(status["state"], "not_configured")
        self.assertIn("OPENAI_API_KEY", status["reason"])
        self.assertEqual(status["gpt_name"], "Psiquiatria")


if __name__ == "__main__":
    unittest.main()
