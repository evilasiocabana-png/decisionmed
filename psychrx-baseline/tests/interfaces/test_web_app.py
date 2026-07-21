import json
import unittest
import http.client
import threading
from pathlib import Path

from interfaces.web.server import (
    STATIC_ROOT,
    PsychRxRequestHandler,
    _load_motor_medication_details,
    _load_toxidrome_screening_signals,
    create_server,
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


class PsychRxWebAppTest(unittest.TestCase):
    def test_static_files_exist(self) -> None:
        self.assertTrue((STATIC_ROOT / "index.html").is_file())
        self.assertTrue((STATIC_ROOT / "styles.css").is_file())
        self.assertTrue((STATIC_ROOT / "medication_decision.css").is_file())
        self.assertTrue((STATIC_ROOT / "app.js").is_file())
        index = (STATIC_ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("Raciocinio psicofarmacologico por apresentacao clinica", index)
        self.assertIn("uma decisao por vez", index)
        self.assertIn('autocomplete="off"', index)
        self.assertIn("medication_decision.css?v=3", index)
        self.assertIn("app.js?v=toxidrome-antidote-display-1", index)
        self.assertIn('data-card="population"', index)
        self.assertIn('id="patient-age-display"', index)
        self.assertIn('id="pregnancy-status"', index)
        self.assertIn('id="lactation-status"', index)
        self.assertIn('id="postpartum-status"', index)
        self.assertIn('id="renal-status"', index)
        self.assertIn('id="hepatic-status"', index)
        self.assertIn('data-group="clinical-contexts"', index)
        self.assertIn('id="coverage-audit-summary"', index)
        self.assertIn("clinical-condition-theory", index)
        self.assertIn("fill-random-case", index)
        self.assertIn("test-case-sequence-label", index)
        self.assertIn("fill-prescription-example", index)
        self.assertIn("Gerar caso teste", index)
        self.assertIn("Preencher caso receita real", index)
        self.assertIn("Paciente", index)
        self.assertIn("patient-name", index)
        self.assertIn("Nascimento", index)
        self.assertIn("patient-birthdate", index)
        self.assertIn("Qual e o contexto da consulta?", index)
        self.assertIn("Existe uma condicao ou diagnostico de referencia?", index)
        self.assertIn("continue-diagnosis", index)
        self.assertIn('data-card="acute-safety"', index)
        self.assertIn('data-card="safety-review"', index)
        self.assertIn("essential-safety-list", index)
        self.assertIn("Campo sem resposta permanece nao avaliado", index)
        self.assertIn('data-group="acute-toxicity-signals"', index)
        self.assertIn("Ha sinais de toxicidade ou intoxicacao aguda?", index)
        self.assertIn("summary-acute-safety", index)
        self.assertIn("acute-toxidrome-details", index)
        self.assertIn("Antidotos e medidas especificas podem ser exibidos", index)
        self.assertIn("doses, via, descontaminacao e execucao ficam fora do PsychRx", index)
        self.assertIn("NIH-MEDLINEPLUS = MedlinePlus/NIH", index)
        self.assertIn("data-jump=\"diagnosis\"", index)
        self.assertIn("Como ele esta hoje?", index)
        self.assertIn("phenotype-intensity-list", index)
        self.assertIn("Quais sintomas predominam?", index)
        self.assertIn("O que queremos trabalhar no tratamento?", index)
        self.assertIn("Objetivos de tolerabilidade e funcionamento", index)
        self.assertIn("data-group=\"secondary-objectives\"", index)
        self.assertIn("Receita atual", index)
        self.assertIn("Campos marcados com * sao obrigatorios", index)
        self.assertIn("medication-required-status", index)
        self.assertIn("current-medication-status", index)
        self.assertIn("Sem medicacao atual", index)
        self.assertIn("current-medication-name", index)
        self.assertIn("O que queremos trabalhar no tratamento", index)
        self.assertIn("Ajuste antes de comparar com a receita", index)
        self.assertIn("clinical-axes", index)
        self.assertIn("summary-clinical-axes", index)
        self.assertNotIn("current-medication-axis", index)
        self.assertIn("Eixos", index)
        self.assertIn("current-medication-dose-number", index)
        self.assertIn("current-medication-duration", index)
        self.assertIn("current-medication-response", index)
        self.assertIn("current-medication-tolerability", index)
        self.assertIn("current-medication-list", index)
        self.assertIn("add-current-medication", index)
        self.assertIn("Perfil farmacologico desejado", index)
        self.assertIn("Quais restricoes refinam a escolha?", index)
        self.assertIn("Gerar conselho do motor", index)
        self.assertNotIn("Comparacao farmacologica", index)
        self.assertIn("Decisao do medico", index)
        self.assertNotIn("Fechamento rapido do motor", index)
        self.assertNotIn("final-medication-status", index)
        self.assertNotIn("final-refresh-counsel", index)
        self.assertIn("Plano terapeutico e monitorizacao", index)
        self.assertIn("data-single=\"presentation\"", index)
        self.assertNotIn("data-single=\"phenotype\"", index)
        self.assertIn("data-group=\"symptoms\"", index)
        self.assertNotIn("data-single=\"objective\"", index)
        self.assertIn("data-group=\"restrictions\"", index)
        self.assertIn("data-group=\"monitoring\"", index)
        self.assertIn("data-single=\"reassessment\"", index)
        self.assertIn("Condicao / diagnostico / quadro de uso", index)
        self.assertIn("Fibromialgia", index)
        self.assertIn("TOC resistente", index)
        self.assertIn("Transtorno por uso de alcool", index)
        self.assertIn("Alcool/drogas ou medicacao sem controle", index)
        self.assertIn("Depressao com fadiga/hipersonia/baixa energia", index)
        self.assertIn("Transtorno bipolar - mania/hipomania", index)
        self.assertIn("summary-presentation", index)
        self.assertIn("summary-condition", index)
        self.assertIn("summary-phenotype", index)
        self.assertIn("summary-profile", index)
        self.assertIn("level-1-strategy", index)
        self.assertIn("level-2-target", index)
        self.assertIn("level-3-status", index)
        self.assertIn("Conselho do motor", index)
        self.assertIn("Resumo farmacologico pratico", index)
        self.assertIn("decision-support-practical-action", index)
        self.assertLess(index.index("Conselho do motor"), index.index("fill-random-case"))
        self.assertIn("decision-support-practical-current", index)
        self.assertIn("decision-support-practical-target", index)
        self.assertIn("decision-support-practical-dose-range", index)
        self.assertIn("decision-support-practical-next", index)
        self.assertIn("Faixa terapeutica", index)
        self.assertIn("decision-support-disease-use", index)
        self.assertIn("decision-support-disease-use-label", index)
        self.assertIn("Uso por doenca", index)
        self.assertIn("decision-support-advice", index)
        self.assertIn("decision-support-rationale", index)
        self.assertIn("decision-support-current-medication", index)
        self.assertIn("Interacoes medicamentosas", index)
        self.assertIn("decision-support-interactions", index)
        self.assertIn("decision-support-target", index)
        self.assertIn("decision-support-substitution", index)
        self.assertIn("decision-support-association", index)
        self.assertIn("decision-support-evidence", index)
        self.assertIn("decision-support-evidence-map", index)
        self.assertIn("decision-support-pharmacology", index)
        self.assertIn("request-decision-support", index)
        self.assertIn("decision-support-status", index)
        self.assertIn("Gerar conselho manualmente", index)
        self.assertIn("Motor local pronto para organizar o caso", index)
        self.assertNotIn("data-single=\"chosen-strategy\"", index)
        self.assertIn("Restricoes aplicadas", index)
        self.assertIn("Alvo farmacologico", index)
        self.assertIn("physician-strategy", index)
        self.assertIn("physician-medication", index)
        self.assertIn("physician-dose-number", index)
        self.assertIn("physician-dose-unit", index)
        self.assertIn("physician-frequency", index)
        self.assertIn("physician-decision-preview", index)
        self.assertNotIn("data-single=\"therapeutic-moment\"", index)
        self.assertNotIn("Problema medicamentoso atual", index)
        self.assertNotIn("<textarea", index)
        app_js = (STATIC_ROOT / "app.js").read_text(encoding="utf-8")
        styles = (STATIC_ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn("PRESENTATIONS", app_js)
        self.assertIn("RANDOM_CASES", app_js)
        self.assertIn("PRESCRIPTION_EXAMPLE_CASE", app_js)
        self.assertIn("fillPrescriptionExampleCase", app_js)
        self.assertIn("sourceLegendHTML", app_js)
        self.assertIn("formatInteractionSummary", app_js)
        self.assertIn("BNF = British National Formulary/NICE", app_js)
        self.assertIn("DM = DailyMed/FDA", app_js)
        self.assertIn("HC = Health Canada", app_js)
        self.assertIn("ST-E = Stahl Essential", app_js)
        self.assertIn("applyScenarioToForm", app_js)
        self.assertIn("Sr. Carlsson", app_js)
        self.assertIn("Naltrexona", app_js)
        self.assertIn("Trazodona", app_js)
        self.assertIn("Fluoxetina", app_js)
        self.assertIn("Clonazepam", app_js)
        self.assertIn("Bromazepam", app_js)
        self.assertIn("currentMedicationDetails", app_js)
        self.assertIn("buildMedicationCoverageTestCases", app_js)
        self.assertIn("guidedFeatureScenarios", app_js)
        self.assertIn("interactionCoverageScenarios", app_js)
        self.assertIn("Caso teste interacao", app_js)
        self.assertIn("Serotonergica ISRS + SARI", app_js)
        self.assertIn("Medicamento fora da base", app_js)
        self.assertIn("medicationCoverageScenario", app_js)
        self.assertIn("associationCoverageScenarios", app_js)
        self.assertIn("prescriptionBasedCoverageScenarios", app_js)
        self.assertIn("Toxicidade medicamentosa aguda suspeita", app_js)
        self.assertIn("Intoxicacao ou exposicao excessiva suspeita", app_js)
        self.assertIn("Clonus hiperreflexia tremor ou mioclonia", app_js)
        self.assertIn("Superdose ingestao excessiva ou mudanca abrupta recente", app_js)
        self.assertIn("prescriptionItemsForAxes", app_js)
        self.assertIn("axisForMedicationDetail", app_js)
        self.assertIn("doseBandLines", app_js)
        self.assertIn("doseValueFromBand", app_js)
        self.assertIn("shortDoseBandLabel", app_js)
        self.assertNotIn("buildExhaustiveTestCases", app_js)
        self.assertIn("fillRandomCase", app_js)
        self.assertIn("Caso teste ${scenarioNumber}/${RANDOM_CASES.length}", app_js)
        self.assertIn("TEST_SIGNALS_BY_AXIS", app_js)
        self.assertIn("clinicalSignalsForAxes", app_js)
        self.assertIn("CLINICAL_THEORY", app_js)
        self.assertIn("renderClinicalConditionTheory", app_js)
        self.assertIn("safetyFriendlyText", app_js)
        self.assertIn("ESSENTIAL_SAFETY_ASSESSMENTS", app_js)
        self.assertIn("function populationComplete()", app_js)
        self.assertIn('birth_date: document.getElementById("patient-birthdate")', app_js)
        self.assertIn('pregnancy_status: populationState("pregnancy-status")', app_js)
        self.assertIn('renal_status: populationState("renal-status")', app_js)
        self.assertIn('hepatic_status: populationState("hepatic-status")', app_js)
        self.assertIn("essentialSafetyComplete", app_js)
        self.assertIn('suicide: safetyState("suicide")', app_js)
        self.assertNotIn('suicide: symptoms.includes("Ideacao suicida") ? "Presente" : "Negado"', app_js)
        self.assertIn("confidenceLabel", app_js)
        self.assertIn("currentMedicationAssessmentFallback", app_js)
        self.assertIn("axisCandidatesFallback", app_js)
        self.assertIn("diseaseUseFallback", app_js)
        self.assertIn("A revisao farmacologica continua em paralelo", app_js)
        self.assertIn("Diagnosticos diferenciais", app_js)
        self.assertIn("WHO-CDDR", app_js)
        self.assertIn("NICE-NG222", app_js)
        self.assertIn("Craving/uso de substancias", app_js)
        self.assertIn("Sintomas psicoticos", app_js)
        self.assertIn("nextRandomCaseIndex += 1", app_js)
        self.assertIn("P1 Idade", app_js)
        self.assertIn("P1 Populacao especial", app_js)
        self.assertIn("P2 Contexto clinico", app_js)
        self.assertIn("P3 Governanca farmacologica", app_js)
        self.assertIn("P3 Monitorizacao oficial", app_js)
        self.assertIn("P4 Cobertura canonica", app_js)
        self.assertIn("P5 Integracao", app_js)
        self.assertIn("setClinicalContextSelection", app_js)
        self.assertIn("activeScenarioSequenceLabel", app_js)
        self.assertIn("Atual: ${activeScenarioSequenceLabel}", app_js)
        self.assertNotIn("Math.random", app_js)
        fill_random_case_body = app_js.split("function fillRandomCase()")[1].split("function medicationDraftFromFields()")[0]
        self.assertNotIn('openCard("decision")', fill_random_case_body)
        self.assertIn("Pronto para opcao inicial", app_js)
        self.assertIn("select_candidate", app_js)
        self.assertIn("doseTargetSummary", app_js)
        self.assertIn("doseTargetDisplay", app_js)
        self.assertIn("doseProfileDisplay", app_js)
        self.assertIn("cleanDoseProfileText", app_js)
        self.assertIn("doseProfileHTML", app_js)
        self.assertIn("doseTargetDisplayHTML", app_js)
        self.assertIn("strategyDoseRange", app_js)
        self.assertIn("Dose - efeito", app_js)
        self.assertIn("formatDiseaseUse", app_js)
        self.assertIn("diseaseUseLabel", app_js)
        self.assertIn("phenotypeDecisionBase", app_js)
        self.assertIn("eligibilityLine", app_js)
        self.assertIn("decision-support-disease-use", app_js)
        self.assertIn("doseSourceLabel", app_js)
        self.assertIn('return "TM"', app_js)
        self.assertIn("sourceAbbreviation", app_js)
        self.assertIn("parenthesizedSource", app_js)
        self.assertIn("NICE = National Institute for Health and Care Excellence", app_js)
        self.assertIn("decision-support-source-legend", app_js)
        self.assertIn("decision-support-population-evidence", index)
        self.assertIn("formatPopulationEvidence", app_js)
        self.assertIn("populationAgeBandForDisplay", app_js)
        self.assertIn("populationReviewNoticeHTML", app_js)
        self.assertIn("populationRangeUnderAdultHTML", app_js)
        self.assertIn("Faixa etaria do paciente", app_js)
        self.assertIn("Revisao pediatrica obrigatoria", app_js)
        self.assertIn("nao liberam dose pediatrica automatica", app_js)
        self.assertIn("population-review-notice", styles)
        self.assertIn("population-range-under-adult", styles)
        self.assertIn("UK-SMPC = informacao oficial de produto do Reino Unido", app_js)
        self.assertIn("formatMedicationWithClass", app_js)
        self.assertIn("displayDrugClass", app_js)
        self.assertIn("medicationClassByName", app_js)
        self.assertIn("primaryClinicalAxis", app_js)
        self.assertIn('labelParts.join(" - ")', app_js)
        self.assertIn("item.reason_for_use", app_js)
        self.assertIn("medicationNameFromDoseRange", app_js)
        self.assertIn("medicationFocusForDoseRange", app_js)
        self.assertIn("PREFERRED_MEDICATIONS_BY_AXIS", app_js)
        self.assertIn("suggestedMedicationForAxis", app_js)
        self.assertIn("axisMedicationComparison", app_js)
        self.assertIn("axisMedicationComparisonData", app_js)
        self.assertIn("shortAxisActionSummary", app_js)
        self.assertIn("bestMotor2RowForMedication", app_js)
        self.assertIn("MOTOR2_UI_FALLBACK_RANGES", app_js)
        self.assertIn("0,5-1 mg/dia (DM)", app_js)
        self.assertIn("6-18 mg/dia (HC)", app_js)
        self.assertIn("25-100 mg a noite (DM/ST-E/GG)", app_js)
        self.assertIn("apiRows.length", app_js)
        self.assertIn("axisDisplayLabel", app_js)
        self.assertIn("comparisonConditionLabel", app_js)
        self.assertIn("axisLabel", app_js)
        self.assertIn("referencia cadastrada: ${condition}", app_js)
        self.assertIn("doseStatusAgainstRange", app_js)
        self.assertIn("doseComparisonLabel", app_js)
        self.assertIn("practicalActionForMedication", app_js)
        self.assertIn("residualTargetSummary", app_js)
        self.assertIn("Alvo residual nao definido", app_js)
        self.assertNotIn("tratar alvo residual", app_js)
        self.assertNotIn("checar tempo, alvo residual", app_js)
        self.assertIn("abaixo da faixa", app_js)
        self.assertIn("dentro da faixa", app_js)
        self.assertIn("acima da faixa", app_js)
        self.assertIn("motorComparableRange", app_js)
        self.assertIn("Faixa por dose-efeito", app_js)
        self.assertIn("Faixa por quadro", app_js)
        self.assertIn("Conduta sugerida: avaliar otimizacao gradual", app_js)
        self.assertIn("Conduta sugerida: manter e monitorar", app_js)
        self.assertIn("Candidato do robo: ${effectiveCandidate.label}. Conduta:", app_js)
        self.assertIn("effectiveRobotCandidateForAxis", app_js)
        self.assertIn("current_axis_coverage", app_js)
        self.assertIn("Medicamento atual:", app_js)
        self.assertIn("Faixa usada na comparacao:", app_js)
        self.assertIn("Leitura da dose:", app_js)
        self.assertIn("dose-efeito revisavel", app_js)
        self.assertNotIn("Dose-efeito disponivel: ${doseBandForMedication(item.name)}", app_js)
        self.assertIn("robotRegimenStrategy", app_js)
        self.assertIn("robotRegimenStrategyHTML", app_js)
        self.assertIn("axis-medication-list", app_js)
        self.assertIn("axis-action-list", app_js)
        self.assertIn("therapeuticRangeRows", app_js)
        self.assertIn("therapeuticRangeListHTML", app_js)
        self.assertIn("therapeutic-range-list", app_js)
        self.assertIn("rowByMedication", app_js)
        self.assertIn("sugerido pelo robo / na receita atual", app_js)
        self.assertIn("Medicamentos por eixo", app_js)
        self.assertIn("doseEffect:", app_js)
        self.assertIn("row.doseEffect || row.range", app_js)
        self.assertNotIn("Todos os medicamentos/eixos", app_js)
        self.assertIn("strategyActionHTML", app_js)
        self.assertIn("medicationActionExplanationsHTML", app_js)
        self.assertIn("Conduta por medicamento", app_js)
        self.assertIn("replacementCandidateForMedication", app_js)
        self.assertIn("medicationPrimaryDecision", app_js)
        self.assertIn("Substituir por ${replacement}", app_js)
        replacement_body = app_js.split("function replacementCandidateForMedication")[1].split("function medicationPrimaryDecision")[0]
        self.assertIn("item?.substitution_candidate", replacement_body)
        self.assertIn("option?.unresolved_reason", replacement_body)
        self.assertIn("cleanCandidateName(option?.name)", replacement_body)
        self.assertNotIn("suggestedMedicationForAxis", replacement_body)
        self.assertNotIn("currentMedicationsForAxis", replacement_body)
        self.assertNotIn("response?.substitution_options", replacement_body)
        self.assertIn("doseGuidanceForReplacement", app_js)
        self.assertIn("doseGuidanceSourceForReplacement", app_js)
        self.assertIn("doseGuidanceDisplay", app_js)
        self.assertIn("replacementDosePlan", app_js)
        self.assertIn("dailyQuantityLabel", app_js)
        self.assertIn("dailyQuantityFromDoseGuidance", app_js)
        self.assertIn("medicationDoseDecisionDetails", app_js)
        self.assertIn("Dose atual:", app_js)
        self.assertIn("Quantidade/dia atual:", app_js)
        self.assertIn("Faixa diaria para revisao:", app_js)
        self.assertIn("Base atual", app_js)
        self.assertIn("Candidato do motor", app_js)
        self.assertIn("Inicio gradual:", app_js)
        self.assertIn("Tempo nessa etapa:", app_js)
        self.assertIn("Evolucao para faixa terapeutica:", app_js)
        self.assertIn("Faixa terapeutica de referencia:", app_js)
        self.assertIn("O motor identificou motivo para troca, mas nao encontrou candidato comparavel.", app_js)
        self.assertIn("actionsRenderedPerMedication", app_js)
        self.assertIn("return regimen()", app_js)
        self.assertIn("Motivo da troca", app_js)
        self.assertIn('return {label: "Manter", reason: "", showReason: false}', app_js)
        self.assertNotIn("Ver justificativas completas", app_js)
        self.assertNotIn('class="medication-decision-details"', app_js)
        self.assertIn("response?.medication_action_explanations", app_js)
        self.assertIn('setHTML("decision-support-practical-target", strategy)', app_js)
        self.assertIn("Receita sugerida pelo robo por eixo", app_js)
        self.assertIn("receita atual nao cobre", app_js)
        self.assertNotIn("<b>Hoje:</b>", app_js)
        self.assertNotIn("<b>Acao:</b>", app_js)
        self.assertIn('clonazepam: "0.5"', app_js)
        self.assertIn('bromazepam: "3"', app_js)
        self.assertIn('quetiapina: "25"', app_js)
        self.assertIn("decision-support-practical-target", app_js)
        self.assertIn("Medicacao / estrategia", index)
        self.assertIn("decision-support-practical-dose-range", app_js)
        self.assertIn("Primeira consulta", app_js)
        self.assertIn("Seguimento", app_js)
        self.assertIn("selectedPhenotypes", app_js)
        self.assertIn("currentMedicationItems", app_js)
        self.assertIn("initializeClinicalFlow", app_js)
        self.assertIn('"diagnosis"', app_js)
        self.assertIn('"continue-diagnosis": "diagnosis"', app_js)
        self.assertIn("[data-single] button.active, [data-group] button.active", app_js)
        self.assertIn("refreshDependentOptions", app_js)
        self.assertIn("buildProfile", app_js)
        self.assertIn("suggestedStrategy", app_js)
        self.assertIn("summaryRows", app_js)
        self.assertNotIn("renderStrategies", app_js)
        self.assertNotIn("renderComparison", app_js)
        self.assertIn("openCard", app_js)
        self.assertIn("buildDecisionSupportRequest", app_js)
        self.assertIn("currentMedicationPayload", app_js)
        self.assertIn("reason_for_use", app_js)
        self.assertIn("CLINICAL_AXES", app_js)
        self.assertIn("suggestedClinicalAxes", app_js)
        self.assertIn("selectedClinicalAxes", app_js)
        self.assertIn("clinical_axes", app_js)
        self.assertIn("clinicalAxes", app_js)
        suggested_axes_body = app_js.split("function suggestedClinicalAxes()")[1].split("function renderClinicalAxisOptions")[0]
        self.assertNotIn("therapeuticObjectiveFromAxes()", suggested_axes_body)
        self.assertIn('setGroupSelection("clinical-axes", scenario.clinicalAxes || suggestedClinicalAxes())', app_js)
        medication_case_body = app_js.split("function medicationCoverageScenario")[1].split("function associationCoverageScenarios")[0]
        association_case_body = app_js.split("function associationCoverageScenarios")[1].split("function firstDetailByAxis")[0]
        prescription_case_body = app_js.split("function prescriptionBasedCoverageScenarios")[1].split("function buildMedicationCoverageTestCases")[0]
        suite_builder_body = app_js.split("function buildMedicationCoverageTestCases")[1].split("RANDOM_CASES = buildMedicationCoverageTestCases")[0]
        self.assertIn("clinicalAxes: [axis]", medication_case_body)
        self.assertIn("const axes = Array.from(new Set", association_case_body)
        self.assertIn("clinicalAxes: axes", association_case_body)
        self.assertIn("clinicalAxes: pattern.axes", prescription_case_body)
        self.assertNotIn("objective: blueprint.objective", medication_case_body)
        self.assertNotIn("objective: blueprint.objective", association_case_body)
        self.assertNotIn("objective: blueprint.objective", prescription_case_body)
        self.assertIn("Caso teste receita clinica", app_js)
        self.assertIn("pattern.axes.length} eixo", app_js)
        self.assertLess(
            suite_builder_body.index("prescriptionBasedCoverageScenarios"),
            suite_builder_body.index("interactionCoverageScenarios"),
        )
        self.assertLess(
            suite_builder_body.index("prescriptionCases.slice(0, 7)"),
            suite_builder_body.index("guidedFeatureScenarios"),
        )
        self.assertLess(
            suite_builder_body.index("guidedFeatureScenarios"),
            suite_builder_body.index("prescriptionCases.slice(7)"),
        )
        self.assertIn("Humor isolado com receita combinada do mesmo eixo", app_js)
        self.assertIn("Humor e ansiedade", app_js)
        self.assertIn("Depressao ansiosa com insonia", app_js)
        self.assertIn("TEPT com sono, resgate e substancias", app_js)
        self.assertIn("TEPT complexo com cinco eixos", app_js)
        self.assertIn("for (let index = 0; index < 160; index += 1)", app_js)
        self.assertIn("substancias/craving", app_js)
        self.assertIn("sono/sedacao", app_js)
        self.assertIn("ansiedade/resgate", app_js)
        self.assertIn("dor/sintomas somaticos", app_js)
        self.assertIn("energia/cognicao", app_js)
        self.assertIn("libido/funcao sexual", app_js)
        self.assertIn("peso/metabolico", app_js)
        self.assertIn("compulsividade/TOC", app_js)
        self.assertIn("medicationResponseStability", app_js)
        self.assertIn("missingPracticalInputs", app_js)
        self.assertIn("missingClosureInputs", app_js)
        self.assertIn("practicalActionLabel", app_js)
        self.assertIn("Aguardar dados: faltam ${missing.join", app_js)
        self.assertIn("updateMedicationRequiredStatus", app_js)
        self.assertIn("noCurrentMedicationSelected", app_js)
        self.assertIn("loadMedicationOptions", app_js)
        self.assertIn("/api/medications", app_js)
        self.assertIn("/api/toxidrome-screening", app_js)
        self.assertIn("renderSelectedToxidromeDetails", app_js)
        self.assertIn("Antidoto/medida", app_js)
        self.assertIn("data-antidote-summary", app_js)
        self.assertIn("/api/clinical-contexts", app_js)
        self.assertIn("clinical_context_ids", app_js)
        self.assertIn("evidence_governance_summary", app_js)
        self.assertIn("scientific_readiness", app_js)
        self.assertIn("monitoring_governance_summary", app_js)
        self.assertIn("/api/clinical-coverage", app_js)
        self.assertIn("coverage_summary", app_js)
        self.assertIn("acute_toxicity", app_js)
        self.assertIn("toxidrome_signals", app_js)
        self.assertIn('medication: "safety-review"', app_js)
        self.assertIn('"safety-review": "acute-safety"', app_js)
        self.assertIn('"acute-safety": "profile"', app_js)
        self.assertNotIn("finalizeAndRefreshCounsel", app_js)
        self.assertNotIn("applyFinalCompletionToMedication", app_js)
        self.assertIn("requestDecisionSupport", app_js)
        self.assertIn("practicalStrategy", app_js)
        self.assertIn("actionBlockers", app_js)
        self.assertIn("pauseReasonText", app_js)
        self.assertIn("pauseActionText", app_js)
        self.assertIn("interromper a estrategia farmacologica de rotina", app_js)
        self.assertIn("nao definem uma toxindrome especifica", app_js)
        self.assertIn("as faixas terapeuticas ficam somente como contexto", app_js)
        self.assertIn("acuteToxicityPriority", app_js)
        self.assertIn("Ranking pausado durante a avaliacao aguda", app_js)
        self.assertIn("Comparacao de dose e conduta pausadas", app_js)
        self.assertIn("HHS-CHEMM, CDC-OD, DM-SS e DM-NMS", app_js)
        self.assertIn("Ja coberto", app_js)
        self.assertIn("Nao coberto", app_js)
        self.assertIn("currentAxisLabel", app_js)
        self.assertIn("Quadro: ${row.condition}. ", app_js)
        self.assertIn("Faixa usada na comparacao", app_js)
        self.assertIn("Resolver seguranca imediata", app_js)
        self.assertIn("hasSuicideBlocker", app_js)
        self.assertNotIn("Farmacos em foco", app_js)
        self.assertIn("Acao imediata: avaliar risco suicida", app_js)
        self.assertIn("manejo de crise pelo medico", app_js)
        self.assertNotIn("Nao avaliado enquanto o motor estiver bloqueado", app_js)
        self.assertIn("practicalJustificationHTML", app_js)
        self.assertIn("Receita: ${medications.length} medicamento(s)", app_js)
        self.assertIn("Eixos cobertos:", app_js)
        self.assertIn("objectiveSummaryHTML", app_js)
        self.assertNotIn('setSingleSelection("objective"', app_js)
        self.assertNotIn('selectedSingle("objective")', app_js)
        self.assertIn("updatePracticalAdvice", app_js)
        self.assertIn("updatePhysicianDecisionPreview", app_js)
        self.assertIn("handleSelectableButton", app_js)
        self.assertIn("bindDirectSelectableButtons", app_js)
        self.assertIn('single.dataset.single === "presentation"', app_js)
        self.assertNotIn("openCard(nextCard(activeCardName()))", app_js)
        self.assertIn("estrategia", app_js)
        self.assertIn("perfil farmacologico", index.lower())

    def test_interface_imports_application_only(self) -> None:
        source = Path("interfaces/web/server.py").read_text(encoding="utf-8")

        self.assertIn("from application.app_service import PsychRxAppService", source)
        self.assertNotIn("from domain", source)
        self.assertNotIn("from knowledge", source)
        self.assertNotIn("from evidence", source)
        self.assertNotIn("from reasoning", source)
        self.assertNotIn("from safety", source)

    def test_server_factory_uses_request_handler(self) -> None:
        server = create_server(port=0)
        try:
            self.assertIs(server.RequestHandlerClass, PsychRxRequestHandler)
        finally:
            server.server_close()

    def test_medication_options_endpoint_reads_motor_matrix(self) -> None:
        server = create_server(port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        host, port = server.server_address
        try:
            conn = http.client.HTTPConnection(host, port, timeout=5)
            conn.request("GET", "/api/medications")
            response = conn.getresponse()
            body = json.loads(response.read().decode("utf-8"))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

        self.assertEqual(response.status, 200)
        self.assertGreaterEqual(len(body["medications"]), 40)
        self.assertIn("Amitriptilina", body["medications"])
        self.assertIn("Haloperidol", body["medications"])
        self.assertIn("Naltrexona", body["medications"])
        self.assertIn("medication_details", body)
        classes = {item["name"]: item["drug_class"] for item in body["medication_details"]}
        self.assertEqual(classes["Sertralina"], "SSRI")
        self.assertEqual(classes["Fluoxetina"], "SSRI")
        details = {item["name"]: item for item in body["medication_details"]}
        self.assertIn("dose_band", details["Mirtazapina"])
        self.assertIn("15", details["Mirtazapina"]["dose_band"])
        self.assertIn("motor2_ranges", details["Clonazepam"])
        clonazepam_ranges = details["Clonazepam"]["motor2_ranges"]
        self.assertTrue(
            any(
                item["condition_range"] == "0,5-1 mg/dia (DM)"
                for item in clonazepam_ranges
            )
        )
        self.assertIn("motor2_ranges", details["Trazodona"])
        trazodone_ranges = details["Trazodona"]["motor2_ranges"]
        self.assertTrue(
            any(
                item["condition"] == "Insonia"
                and item["condition_range"] == "25-100 mg a noite (DM/ST-E/GG)"
                for item in trazodone_ranges
            )
        )
        self.assertIn("motor2_ranges", details["Acamprosato"])
        acamprosate_ranges = details["Acamprosato"]["motor2_ranges"]
        self.assertTrue(
            any(
                item["dose_effect_min"] == "666"
                and item["dose_effect_max"] == "666"
                and "666 mg" in item["dose_effect_band"]
                for item in acamprosate_ranges
            )
        )
        self.assertIn("association_fit", details["Bupropiona XL"])
        self.assertTrue(details["Bupropiona XL"]["association_fit"])

    def test_toxidrome_screening_endpoint_returns_source_anchored_signals(self) -> None:
        rows = _load_toxidrome_screening_signals()
        self.assertGreaterEqual(len(rows), 10)
        self.assertEqual(rows[0]["signal_id"], "NONE")
        self.assertTrue(any("Naloxona" in row["antidote_or_specific_measure"] for row in rows))
        self.assertTrue(any("Atropina" in row["antidote_or_specific_measure"] for row in rows))

        server = create_server(port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        host, port = server.server_address
        try:
            conn = http.client.HTTPConnection(host, port, timeout=5)
            conn.request("GET", "/api/toxidrome-screening")
            response = conn.getresponse()
            body = json.loads(response.read().decode("utf-8"))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

        self.assertEqual(response.status, 200)
        self.assertGreaterEqual(len(body["signals"]), 10)
        self.assertTrue(any("CDC-OD" in item["source_id"] for item in body["signals"]))
        self.assertTrue(any("antidote_or_specific_measure" in item for item in body["signals"]))

    def test_clinical_context_endpoint_exposes_non_treatment_registry(self) -> None:
        server = create_server(port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        host, port = server.server_address
        try:
            conn = http.client.HTTPConnection(host, port, timeout=5)
            conn.request("GET", "/api/clinical-contexts")
            response = conn.getresponse()
            body = json.loads(response.read().decode("utf-8"))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

        self.assertEqual(200, response.status)
        self.assertGreaterEqual(len(body["contexts"]), 20)
        self.assertTrue(all(not item["treatment_rule_allowed"] for item in body["contexts"]))
        self.assertTrue(any(item["context_id"] == "DELIRIUM_CONCERN" for item in body["contexts"]))

    def test_coverage_audit_endpoint_exposes_scientific_gaps(self) -> None:
        server = create_server(port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        host, port = server.server_address
        try:
            conn = http.client.HTTPConnection(host, port, timeout=5)
            conn.request("GET", "/api/coverage-audit")
            response = conn.getresponse()
            body = json.loads(response.read().decode("utf-8"))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

        self.assertEqual(200, response.status)
        self.assertEqual(83, body["medication_count"])
        self.assertEqual(44, body["interaction_gap_count"])
        self.assertEqual(0, body["disease_use_formally_validated_count"])
        self.assertEqual("structural_only_scientific_review_pending", body["scientific_runtime_readiness"])

    def test_clinical_coverage_endpoint_reconciles_all_51_topics(self) -> None:
        server = create_server(port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        host, port = server.server_address
        try:
            conn = http.client.HTTPConnection(host, port, timeout=5)
            conn.request("GET", "/api/clinical-coverage")
            response = conn.getresponse()
            body = json.loads(response.read().decode("utf-8"))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

        self.assertEqual(200, response.status)
        self.assertEqual(51, body["topic_count"])
        self.assertEqual({"covered": 17, "partial": 13, "relevant_gap": 12, "contextual_only": 9}, body["summary"])
        self.assertEqual([], body["validation_issues"])

    def test_random_case_suite_keeps_existing_scenarios_and_adds_guided_groups(self) -> None:
        details = _load_motor_medication_details()

        def dose_band_lines(detail: dict) -> list[str]:
            lines = [
                line.strip()
                for line in str(detail.get("dose_band", "")).splitlines()
                if line.strip() and any(char.isdigit() for char in line)
            ]
            lines = [
                line
                for line in lines
                if not line.lower().startswith("faixa usual")
                and not line.lower().startswith("faixa antidepressiva usual")
            ]
            return lines or [""]

        prescription_cases = 160
        medication_cases = sum(len(dose_band_lines(detail)) for detail in details)
        association_cases = sum(
            1 for detail in details if str(detail.get("association_fit", "")).strip()
        )

        interaction_cases = 8
        guided_cases = 20
        self.assertEqual(
            prescription_cases + medication_cases + association_cases + interaction_cases + guided_cases,
            362,
        )

    def test_decision_support_endpoint_returns_contract_payload(self) -> None:
        server = create_server(port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        host, port = server.server_address
        try:
            conn = http.client.HTTPConnection(host, port, timeout=5)
            payload = json.dumps(
                {
                    "birth_date": "1980-01-01",
                    "pregnancy_status": "Nao aplicavel",
                    "lactation_status": "Nao aplicavel",
                    "postpartum_status": "Nao aplicavel",
                    "renal_status": "Preservada",
                    "hepatic_status": "Preservada",
                    "symptoms": ["Humor deprimido"],
                    "impairment_domains": ["Trabalho"],
                    "stability": "Sem resposta",
                    "current_medications": [
                        {"name": "Sertralina"},
                        {"name": "Trazodona"},
                    ],
                    "safety": safety_payload(),
                }
            )
            conn.request(
                "POST",
                "/api/decision-support",
                body=payload,
                headers={"Content-Type": "application/json"},
            )
            response = conn.getresponse()
            body = json.loads(response.read().decode("utf-8"))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

        self.assertEqual(response.status, 200)
        self.assertIn("summary", body)
        self.assertEqual(body["recommended_action"], "substitute")
        self.assertIn("prescription_boundary", body)
        self.assertIn("interaction_summary", body)
        self.assertTrue(
            any("somacao serotoninergica" in item for item in body["interaction_summary"])
        )

    def test_unknown_medication_interaction_is_explicitly_flagged(self) -> None:
        from application.clinical_decision_support_service import ClinicalDecisionSupportService

        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "symptoms": ["Humor deprimido"],
                "impairment_domains": ["Trabalho"],
                "stability": "Resposta parcial",
                "current_medications": [
                    {"name": "Sertralina", "response": "Resposta parcial"},
                    {"name": "Medicamento externo", "response": "Resposta parcial"},
                ],
                "safety": safety_payload(),
            }
        )
        interactions = response.to_dict()["interaction_summary"]

        self.assertTrue(
            any("Medicamento nao cadastrado: Medicamento externo" in item for item in interactions)
        )
        self.assertTrue(any("Fonte: PENDENTE/DM/ANVISA/EMA" in item for item in interactions))

    def test_known_gap_corrections_return_practical_advice(self) -> None:
        from application.clinical_decision_support_service import ClinicalDecisionSupportService

        service = ClinicalDecisionSupportService()
        safety = safety_payload()
        scenarios = (
            (
                "Diazepam",
                "Transtorno de ansiedade generalizada",
                "reduzir ansiedade",
                ("Ansiedade", "Tensao", "Insonia inicial"),
                "2",
                "TAG: 2-10",
            ),
            (
                "Oxazepam",
                "Transtorno de ansiedade generalizada",
                "reduzir ansiedade",
                ("Ansiedade", "Tensao", "Insonia inicial"),
                "10",
                "TAG: 10-15",
            ),
            (
                "Naltrexona",
                "Transtorno por uso de alcool",
                "Estabilizacao",
                ("Compulsao", "Ansiedade", "Insonia inicial"),
                "25",
                "vicios: 25-50",
            ),
        )

        for medication, context, objective, symptoms, dose, expected_range in scenarios:
            with self.subTest(medication=medication):
                response = service.build_response(
                    {
                        "birth_date": "1980-01-01",
                        "pregnancy_status": "Nao aplicavel",
                        "lactation_status": "Nao aplicavel",
                        "postpartum_status": "Nao aplicavel",
                        "renal_status": "Preservada",
                        "hepatic_status": "Preservada",
                        "diagnostic_context": context,
                        "clinical_presentation": "Revisao medicamentosa",
                        "therapeutic_objective": objective,
                        "symptoms": symptoms,
                        "impairment_domains": ("Trabalho",),
                        "impairment_severity": "Importante",
                        "stability": "Resposta parcial",
                        "pharmacological_profile": ("Ansiedade: 4", "Compulsividade: 4"),
                        "current_medications": (
                            {
                                "name": medication,
                                "dose_value": dose,
                                "dose_unit": "mg",
                                "frequency": "1x/dia",
                                "duration": "8 semanas",
                                "adherence": "Boa",
                                "response": "Resposta parcial",
                                "tolerability": "Boa",
                            },
                        ),
                        "safety": safety,
                    }
                )
                payload = response.to_dict()
                target = payload["pharmacological_targets"][0]
                self.assertEqual(payload["status"], "unresolved")
                self.assertEqual(payload["scientific_readiness"], "structural_only_scientific_review_pending")
                self.assertNotEqual(payload["recommended_action"], "insufficient_information")
                self.assertIn(expected_range, target["therapeutic_dose_target"])
                self.assertNotIn("nao cadastrado", target["therapeutic_dose_target"].lower())

    def test_current_dose_inside_range_does_not_suggest_dose_increase(self) -> None:
        from application.clinical_decision_support_service import ClinicalDecisionSupportService

        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "diagnostic_context": "Depressao com insonia/baixa ingestao/perda de peso",
                "clinical_presentation": "Revisao medicamentosa",
                "therapeutic_objective": "melhorar sono",
                "symptoms": ("Insonia inicial", "Insonia terminal", "Ansiedade"),
                "impairment_domains": ("Sono", "Trabalho"),
                "impairment_severity": "Importante",
                "stability": "Resposta parcial",
                "pharmacological_profile": ("Insonia: 4", "Ansiedade: 3"),
                "current_medications": (
                    {
                        "name": "Agomelatina",
                        "dose_value": "50",
                        "dose_unit": "mg",
                        "frequency": "1x/dia",
                        "duration": "8 semanas",
                        "adherence": "Boa",
                        "response": "Resposta parcial",
                        "tolerability": "Boa",
                    },
                ),
                "safety": safety_payload(),
            }
        )

        self.assertEqual(response.status, "unresolved")
        self.assertEqual(response.recommended_action, "optimize_current")
        self.assertNotEqual(response.recommended_action, "increase_dose")

    def test_app_state_is_json_safe(self) -> None:
        from application.app_service import PsychRxAppService

        payload = PsychRxAppService().get_app_view_model().to_dict()
        encoded = json.dumps(payload, ensure_ascii=False)

        self.assertIn("PsychRx", encoded)
        self.assertIn("READ ONLY", encoded)
        self.assertIn("Clinical Kernel Integration", encoded)
        self.assertIn("Patient Header", encoded)
        self.assertIn("Clinical Investigation Panel", encoded)
        self.assertIn("Objectives Widget", encoded)
        self.assertIn("Risk Widget", encoded)


if __name__ == "__main__":
    unittest.main()
