"""Deterministic decision-support table for the PsychRx consultation app.

This module does not prescribe, select a patient-specific medication, or replace
the physician. It maps the structured consultation fields to a display-safe
decision-support response so the local app works without a specialized GPT.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from application.antidepressant_indication_dose_matrix import (
    AntidepressantIndicationDoseMatrix,
)
from application.clinical_decision_support_contract import (
    ActionEvidencePayload,
    ClinicalDecisionSupportResponse,
    CurrentMedicationPayload,
    EvidenceCitationPayload,
    MedicationActionExplanationPayload,
    MedicationOptionPayload,
    PharmacologicalTargetPayload,
)
from application.clinical_context_registry import ClinicalContextAssessment
from application.clinical_coverage_matrix import ClinicalCoverageMatch
from application.clinical_safety_assessment import ClinicalSafetyAssessmentService
from application.clinical_phenotype_filter import ClinicalPhenotypeFilter, PhenotypeAssessment
from application.current_medication_assessment import (
    CurrentMedicationAssessment,
    CurrentMedicationAssessmentService,
)
from application.disease_use_filter import DiseaseUseFilter, MedicationEligibility
from application.medication_strategy_table import (
    MedicationStrategyEntry,
    MedicationStrategyTable,
)
from application.medication_dose_profile_table import MedicationDoseProfileTable
from application.medication_disease_use_table import MedicationDiseaseUseTable
from application.medication_interaction_table import MedicationInteractionTable
from application.medication_population_evidence_table import (
    MedicationPopulationEvidenceTable,
)
from application.motor2_strategy_matrix import Motor2StrategyMatrix
from application.monitoring_governance import MonitoringGovernanceService
from application.pharmacological_decision_matrix import PharmacologicalDecisionMatrix
from application.patient_population_context import PatientPopulationContext


@dataclass(frozen=True)
class RuleTableContext:
    """Normalized inputs used by the local rule table."""

    symptoms: tuple[str, ...]
    observed_signs: tuple[str, ...]
    impairment_domains: tuple[str, ...]
    impairment_severity: str
    stability: str
    comorbidities: tuple[str, ...]
    medications: tuple[CurrentMedicationPayload, ...]
    safety: dict[str, str]
    diagnostic_context: str = ""
    clinical_presentation: str = ""
    therapeutic_objective: str = ""
    pharmacological_profile: tuple[str, ...] = ()
    clinical_axes: tuple[str, ...] = ()
    population: PatientPopulationContext | None = None
    clinical_contexts: ClinicalContextAssessment | None = None
    coverage: ClinicalCoverageMatch | None = None


class DecisionSupportRuleTable:
    """Maps consultation state to local decision-support advice."""

    def __init__(
        self,
        medication_table: MedicationStrategyTable | None = None,
        pharmacological_matrix: PharmacologicalDecisionMatrix | None = None,
        medication_assessment: CurrentMedicationAssessmentService | None = None,
        indication_dose_matrix: AntidepressantIndicationDoseMatrix | None = None,
        dose_profile_table: MedicationDoseProfileTable | None = None,
        motor2_strategy_matrix: Motor2StrategyMatrix | None = None,
        disease_use_table: MedicationDiseaseUseTable | None = None,
        interaction_table: MedicationInteractionTable | None = None,
        phenotype_filter: ClinicalPhenotypeFilter | None = None,
        disease_use_filter: DiseaseUseFilter | None = None,
        safety_assessment: ClinicalSafetyAssessmentService | None = None,
        monitoring_governance: MonitoringGovernanceService | None = None,
        population_evidence_table: MedicationPopulationEvidenceTable | None = None,
    ) -> None:
        self._medication_table = medication_table or MedicationStrategyTable()
        self._pharmacological_matrix = (
            pharmacological_matrix or PharmacologicalDecisionMatrix()
        )
        self._medication_assessment = (
            medication_assessment
            or CurrentMedicationAssessmentService(self._medication_table)
        )
        self._indication_dose_matrix = (
            indication_dose_matrix or AntidepressantIndicationDoseMatrix()
        )
        self._dose_profile_table = dose_profile_table or MedicationDoseProfileTable()
        self._motor2_strategy_matrix = motor2_strategy_matrix or Motor2StrategyMatrix()
        self._disease_use_table = disease_use_table or MedicationDiseaseUseTable()
        self._interaction_table = interaction_table or MedicationInteractionTable()
        self._phenotype_filter = phenotype_filter or ClinicalPhenotypeFilter()
        self._disease_use_filter = disease_use_filter or DiseaseUseFilter(
            self._disease_use_table
        )
        self._safety_assessment = safety_assessment or ClinicalSafetyAssessmentService()
        self._monitoring_governance = monitoring_governance or MonitoringGovernanceService()
        self._population_evidence_table = (
            population_evidence_table or MedicationPopulationEvidenceTable()
        )

    def build(self, context: RuleTableContext) -> ClinicalDecisionSupportResponse:
        """Return a deterministic response for physician review."""
        phenotype = self._phenotype_filter.assess(
            clinical_presentation=context.clinical_presentation,
            diagnostic_context=context.diagnostic_context,
            symptoms=context.symptoms,
            observed_signs=context.observed_signs,
            pharmacological_profile=context.pharmacological_profile,
            safety=context.safety,
        )
        safety_warnings = tuple(
            dict.fromkeys(
                (
                    *(context.population.blocking_warnings if context.population else ("Idade: Nao avaliada",)),
                    *(context.clinical_contexts.blocking_warnings if context.clinical_contexts else ()),
                    *self._safety_warnings(context),
                )
            )
        )
        if safety_warnings:
            return self._blocked_response(context, safety_warnings, phenotype)

        medication_assessments = self._medication_assessment.assess_all(
            context.medications
        )
        action = self._select_action(context, medication_assessments)
        strategy_code = self._strategy_code(action, context)
        target = self._target(context)
        raw_ranked_options = self._ranked_options(context)
        ranked_options, eligibilities = self._filtered_ranked_options(
            raw_ranked_options,
            context=context,
            action=action,
            phenotype=phenotype,
        )
        if self._requires_candidate(action) and raw_ranked_options and not ranked_options:
            return self._no_eligible_candidate_response(
                context=context,
                action=action,
                phenotype=phenotype,
                eligibilities=eligibilities,
            )
        evidence_governance, scientific_readiness = self._evidence_governance(
            context, raw_ranked_options, eligibilities
        )
        monitoring = self._monitoring_governance.assess(
            symptoms=context.symptoms,
            action=action,
            medications=context.medications,
        )
        summary = self._summary_for(action, context, medication_assessments)
        rationale = (
            *((context.population.display_line(),) if context.population else ()),
            *self._rationale(action, context, medication_assessments),
        )

        return ClinicalDecisionSupportResponse(
            summary=summary,
            recommended_action=action,
            clinical_rationale=rationale,
            impairment_targets=context.impairment_domains,
            pharmacological_targets=(
                self._pharmacological_target(context, target, action, ranked_options),
            ),
            substitution_options=self._substitution_options(
                action, context, target, ranked_options
            ),
            association_options=self._association_options(action, context, target),
            action_evidence=(self._action_evidence(action, context, ranked_options),),
            medication_action_explanations=self._medication_action_explanations(
                context, medication_assessments
            ),
            rejected_alternatives=self._rejected_alternatives(action),
            safety_warnings=self._risk_warnings(context),
            monitoring_targets=monitoring.targets,
            monitoring_governance_summary=monitoring.display_lines(),
            population_evidence_summary=self._population_evidence_summary(
                context, ranked_options
            ),
            disease_use_summary=self._disease_use_summary(
                context, action, ranked_options, phenotype
            ),
            interaction_summary=self._interaction_summary(context),
            phenotype_summary=phenotype.display_lines(),
            clinical_context_summary=(
                context.clinical_contexts.display_lines()
                if context.clinical_contexts
                else ()
            ),
            coverage_summary=((context.coverage.display_line(),) if context.coverage else ()),
            evidence_governance_summary=evidence_governance,
            scientific_readiness=scientific_readiness,
            eligibility_summary=tuple(item.display_line() for item in eligibilities if item.eligible)[:5],
            excluded_medications=tuple(item.display_line() for item in eligibilities if not item.eligible)[:8],
            strategy_code=strategy_code,
            confidence=(
                self._confidence(context)
                if scientific_readiness == "scientifically_runtime_eligible"
                else f"{self._confidence(context)}_source_pending"
            ),
            status=(
                "ready_for_clinician_review"
                if scientific_readiness == "scientifically_runtime_eligible"
                else "unresolved"
            ),
            prescription_boundary=(
                "Suporte a decisao medica. O motor organiza uma hipotese de "
                "estrategia; o medico permanece responsavel pela escolha final "
                "do medicamento, dose, prescricao e conduta."
            ),
        )

    def _blocked_response(
        self,
        context: RuleTableContext,
        safety_warnings: tuple[str, ...],
        phenotype: PhenotypeAssessment | None = None,
    ) -> ClinicalDecisionSupportResponse:
        phenotype = phenotype or PhenotypeAssessment(
            primary_phenotype="UNSPECIFIED_OR_INSUFFICIENT_DATA",
            secondary_phenotypes=(),
            supporting_features=(),
            confidence="low",
        )
        acute_toxicity = any("toxicidade/intoxicacao aguda" in item for item in safety_warnings)
        summary = (
            "Prioridade aguda: interromper o ranking farmacologico de rotina e realizar avaliacao medica urgente."
            if acute_toxicity
            else "Conselho suspenso: resolver seguranca antes de estrategia."
        )
        primary_rationale = (
            "A triagem identificou sinais possivelmente compativeis com toxicidade ou intoxicacao aguda. O padrao nao constitui diagnostico de toxindrome."
            if acute_toxicity
            else "A tabela local bloqueou estrategia porque existe red flag, adesao ruim, efeito adverso relevante ou item de seguranca nao avaliado."
        )
        return ClinicalDecisionSupportResponse(
            summary=summary,
            recommended_action="investigate_before_change",
            clinical_rationale=(
                primary_rationale,
                "Fluxo obrigatorio: seguranca -> estado clinico -> receita atual -> estrategia.",
                *((context.population.display_line(),) if context.population else ()),
                *self._regimen_axis_lines(context),
            ),
            impairment_targets=context.impairment_domains,
            pharmacological_targets=(
                PharmacologicalTargetPayload(
                    impairment_domain=", ".join(context.impairment_domains) or "nao informado",
                    symptom_target=", ".join(context.symptoms) or "nao informado",
                    pharmacological_target="seguranca antes de alvo farmacologico",
                    therapeutic_dose_target="Nao aplicavel enquanto seguranca estiver bloqueada.",
                    unresolved_reason="safety_first_required",
                ),
            ),
            action_evidence=(
                ActionEvidencePayload(
                    action="investigate_before_change",
                    rationale=(
                        "O algoritmo local exige fechamento de seguranca antes de "
                        "qualquer aumento, reducao, troca, associacao ou retirada."
                    ),
                    citations=(self._operational_citation("Safety gate"),),
                ),
            ),
            medication_action_explanations=self._medication_action_explanations(
                context, safety_blocked=True
            ),
            safety_warnings=safety_warnings,
            monitoring_targets=("seguranca", "adesao", "efeitos adversos", "risco agudo"),
            monitoring_governance_summary=self._monitoring_governance.assess(
                symptoms=context.symptoms,
                action="investigate_before_change",
                medications=context.medications,
            ).display_lines(),
            population_evidence_summary=self._population_evidence_summary(context),
            interaction_summary=self._interaction_summary(context),
            phenotype_summary=phenotype.display_lines(),
            clinical_context_summary=(
                context.clinical_contexts.display_lines()
                if context.clinical_contexts
                else ()
            ),
            coverage_summary=((context.coverage.display_line(),) if context.coverage else ()),
            strategy_code="NO_DRUG_RECOMMENDATION",
            confidence="high_for_blocking",
            status="blocked",
        )

    def _no_eligible_candidate_response(
        self,
        *,
        context: RuleTableContext,
        action: str,
        phenotype: PhenotypeAssessment,
        eligibilities: tuple[MedicationEligibility, ...],
    ) -> ClinicalDecisionSupportResponse:
        exclusions = tuple(item.display_line() for item in eligibilities if not item.eligible)
        return ClinicalDecisionSupportResponse(
            summary=(
                "Ranking farmacologico nao liberado: nenhum candidato elegivel "
                "passou pelo filtro de fenotipo, uso por doenca/quadro e estrategia."
            ),
            recommended_action="insufficient_information",
            clinical_rationale=(
                f"Fenotipo avaliado: {phenotype.primary_phenotype}.",
                f"Eixos clinicos a cobrir: {', '.join(context.clinical_axes) if context.clinical_axes else 'nao definidos'}.",
                *self._axis_coverage_lines(context),
                "O motor nao presume compatibilidade quando o uso por doenca/quadro esta ausente, restrito ou incompativel.",
                "Revisar diagnostico, fase clinica, estrategia pretendida e dados de seguranca antes de selecionar medicamento.",
            ),
            impairment_targets=context.impairment_domains,
            pharmacological_targets=(
                PharmacologicalTargetPayload(
                    impairment_domain=", ".join(context.impairment_domains) or "nao informado",
                    symptom_target=", ".join(context.symptoms) or "nao informado",
                    pharmacological_target="sem candidato elegivel apos filtro",
                    therapeutic_dose_target="Nao aplicavel sem candidato elegivel.",
                    unresolved_reason="no_eligible_candidate_after_disease_use_filter",
                ),
            ),
            action_evidence=(
                ActionEvidencePayload(
                    action="insufficient_information",
                    rationale="Filtro de elegibilidade aplicado antes do ranking principal.",
                    citations=(self._operational_citation("Disease-use eligibility filter"),),
                ),
            ),
            medication_action_explanations=self._medication_action_explanations(
                context
            ),
            monitoring_targets=self._monitoring_targets(context, action=action),
            monitoring_governance_summary=self._monitoring_governance.assess(
                symptoms=context.symptoms,
                action=action,
                medications=context.medications,
            ).display_lines(),
            population_evidence_summary=self._population_evidence_summary(context),
            phenotype_summary=phenotype.display_lines(),
            clinical_context_summary=(
                context.clinical_contexts.display_lines()
                if context.clinical_contexts
                else ()
            ),
            coverage_summary=((context.coverage.display_line(),) if context.coverage else ()),
            evidence_governance_summary=tuple(
                dict.fromkeys(
                    f"Uso por quadro: {item.evidence_status or 'status nao informado'}"
                    for item in eligibilities
                )
            ),
            scientific_readiness="structural_only_scientific_review_pending",
            interaction_summary=self._interaction_summary(context),
            excluded_medications=exclusions[:8],
            strategy_code=self._strategy_code(action, context),
            confidence="moderate_structural",
            status="unresolved",
            prescription_boundary=(
                "Suporte a decisao medica. O medico permanece responsavel pela "
                "escolha final do medicamento, dose, prescricao e conduta."
            ),
        )

    def _population_evidence_summary(
        self,
        context: RuleTableContext,
        ranked_options: tuple[MedicationStrategyEntry, ...] = (),
    ) -> tuple[str, ...]:
        """Return official source excerpts for the assessed age band.

        These lines are informational and never make an otherwise ineligible
        medication or dose eligible for therapeutic runtime use.
        """
        if not context.population or context.population.age_band == "UNKNOWN":
            return ()
        names = tuple(
            dict.fromkeys(
                (
                    *(medication.name for medication in context.medications),
                    *(option.name for option in ranked_options),
                )
            )
        )
        if not names:
            return (
                f"Faixa etaria {context.population.age_band}: "
                "nenhum medicamento atual ou candidato para cruzamento de fonte.",
            )
        evidence = self._population_evidence_table.for_medications(
            names, context.population.age_band
        )
        lines = [item.display_line() for item in evidence]
        located = {self._normalize_text(item.medication_name) for item in evidence}
        lines.extend(
            f"{name} | {context.population.age_band}: fonte populacional oficial nao localizada (PENDENTE)"
            for name in names
            if self._normalize_text(name) not in located
        )
        return tuple(lines[:5])

    def _select_action(
        self,
        context: RuleTableContext,
        medication_assessments: tuple[CurrentMedicationAssessment, ...] = (),
    ):
        stability = context.stability.lower()
        has_medication = bool(context.medications)
        adverse = context.safety.get("adverse_effects", "").lower()
        assessment = medication_assessments[0] if medication_assessments else None

        if not has_medication and context.pharmacological_profile and context.symptoms:
            return "select_candidate"
        if context.pharmacological_profile and not stability:
            return "investigate_before_change"
        if "estavel" in stability:
            return "maintain"
        if "parcial" in stability and has_medication:
            motor2_assessment = self._motor2_current_assessment(context)
            if motor2_assessment and motor2_assessment.suggested_action in {
                "increase_dose",
                "optimize_current",
            }:
                if (
                    motor2_assessment.suggested_action == "optimize_current"
                    and self._uncovered_clinical_axes(context)
                ):
                    return "associate"
                return motor2_assessment.suggested_action
            indication_dose_status = self._current_indication_dose_status(context)
            if adverse in {"leves", "moderados"}:
                return "optimize_current"
            if indication_dose_status == "below_registered_range":
                return "increase_dose"
            if indication_dose_status in {"within_registered_range", "above_registered_range"}:
                if self._uncovered_clinical_axes(context):
                    return "associate"
                return "optimize_current"
            if assessment and assessment.current_dose_status == "below_registered_range":
                return "increase_dose"
            if assessment and assessment.current_dose_status in {
                "within_registered_range",
                "above_registered_range",
            }:
                return "optimize_current"
            return "optimize_current"
        if "parcial" in stability:
            return "insufficient_information"
        if "sem resposta" in stability and has_medication:
            motor2_assessment = self._motor2_current_assessment(context)
            if motor2_assessment and motor2_assessment.suggested_action in {
                "increase_dose",
                "substitute",
                "optimize_current",
            }:
                return motor2_assessment.suggested_action
            indication_dose_status = self._current_indication_dose_status(context)
            if indication_dose_status == "below_registered_range":
                return "increase_dose"
            if assessment and assessment.current_dose_status == "below_registered_range":
                return "increase_dose"
            return "substitute"
        if "sem resposta" in stability:
            return "insufficient_information"
        if any(term in stability for term in ("instavel", "recaida", "piora")):
            return "investigate_before_change"
        return "insufficient_information"

    def _motor2_current_assessment(self, context: RuleTableContext):
        """Return Motor 2 assessment for the first medication, when available."""
        if not context.medications:
            return None
        return self._motor2_assessment_for_medication(context, context.medications[0])

    def _motor2_assessment_for_medication(
        self,
        context: RuleTableContext,
        medication: CurrentMedicationPayload,
    ):
        """Return a condition-aware Motor 2 assessment for one medication."""
        clinical_text = " ".join(
            (
                context.clinical_presentation,
                context.diagnostic_context,
                context.therapeutic_objective,
                *context.symptoms,
                *context.pharmacological_profile,
                *context.impairment_domains,
            )
        )
        dose = medication.dose_used or medication.dose_value or medication.dose_prescribed
        return self._motor2_strategy_matrix.assess(
            medication_name=medication.name,
            current_dose=dose,
            clinical_text=clinical_text,
            response_state=medication.response or context.stability,
        )

    def _current_indication_dose_status(self, context: RuleTableContext) -> str:
        """Compare current dose with the condition-specific registered range."""
        if not context.medications:
            return "dose_indeterminate"
        medication = context.medications[0]
        indication_range = self._indication_dose_matrix.range_for(
            medication_name=medication.name,
            clinical_presentation=context.clinical_presentation,
            symptoms=context.symptoms,
            pharmacological_profile=context.pharmacological_profile,
            impairment_domains=context.impairment_domains,
            diagnostic_context=context.diagnostic_context,
            therapeutic_objective=context.therapeutic_objective,
        )
        if not indication_range:
            return "dose_indeterminate"
        dose = self._first_number(
            medication.dose_used or medication.dose_value or medication.dose_prescribed
        )
        range_values = self._range_numbers(indication_range.range_text)
        if dose is None or range_values is None:
            return "dose_indeterminate"
        low, high = range_values
        if dose < low:
            return "below_registered_range"
        if dose > high:
            return "above_registered_range"
        return "within_registered_range"

    def _target(self, context: RuleTableContext) -> str:
        axes_to_cover = self._uncovered_clinical_axes(context) or context.clinical_axes
        axes = " ".join(axes_to_cover).lower()
        return self._target_for_axes_text(axes, context)

    @staticmethod
    def _target_for_axes_text(axes: str, context: RuleTableContext) -> str:
        if "sono" in axes:
            return "sono / sedacao / ativacao"
        if "ansiedade" in axes:
            return "ansiedade / serotoninergico"
        if "dor" in axes or "somaticos" in axes:
            return "dor / sintomas somaticos"
        if "energia" in axes or "cognicao" in axes:
            return "energia / cognicao / ativacao"
        if "compulsividade" in axes or "toc" in axes:
            return "compulsividade / serotonergico"
        if "libido" in axes or "sexual" in axes:
            return "funcao sexual / baixa disfuncao sexual"
        if "peso" in axes or "metabolico" in axes:
            return "peso / perfil metabolico"
        if "humor" in axes or "tept" in axes:
            return "humor / energia / antidepressivo"
        if "substancias" in axes:
            return "compulsividade / craving / reducao de uso"
        if "estabilizacao" in axes:
            return "estabilizacao do humor"
        if "psicose" in axes:
            return "organizacao do pensamento / antipsicotico"
        symptoms = set(context.symptoms)
        if {"Insonia inicial", "Insonia terminal"} & symptoms:
            return "sono / sedacao / ativacao"
        if {"Ansiedade", "Irritabilidade"} & symptoms:
            return "ansiedade / serotoninergico"
        if {"Humor deprimido", "Anedonia", "Fadiga"} & symptoms:
            return "humor / energia / antidepressivo"
        return "alvo farmacologico pendente por sintoma dominante indefinido"

    def _summary_for(
        self,
        action: str,
        context: RuleTableContext,
        medication_assessments: tuple[CurrentMedicationAssessment, ...] = (),
    ) -> str:
        assessment_text = (
            f" {medication_assessments[0].summary()}"
            if medication_assessments
            else ""
        )
        if context.pharmacological_profile:
            profile = ", ".join(context.pharmacological_profile)
            medication = (
                ", ".join(item.name for item in context.medications)
                or "sem medicacao atual"
            )
            return (
                "Ranking farmacologico gerado para revisao medica. "
                f"Perfil desejado: {profile}. Base: "
                f"{'diagnostico informado' if self._has_defined_diagnosis(context) else 'fenotipo/quadro clinico sem diagnostico fechado'}. "
                f"Receita atual: {medication}."
                f"{assessment_text}"
            )
        labels = {
            "maintain": "Manter tratamento atual e monitorar resposta.",
            "increase_dose": "Avaliar otimizacao de dose do tratamento atual.",
            "optimize_current": "Revisar tratamento atual antes de trocar.",
            "substitute": "Avaliar substituicao por falta de resposta suficiente.",
            "associate": "Avaliar associacao apenas se resposta parcial persistir.",
            "select_candidate": "Indicar opcao farmacologica inicial para revisao medica.",
            "investigate_before_change": "Investigar antes de alterar medicacao.",
            "insufficient_information": "Completar informacoes antes de estrategia.",
        }
        medication = ", ".join(item.name for item in context.medications) or "sem medicacao atual"
        profile = (
            f" Perfil desejado: {', '.join(context.pharmacological_profile)}."
            if context.pharmacological_profile
            else ""
        )
        return f"{labels.get(action, action)} Receita atual: {medication}.{profile}{assessment_text}"

    def _rationale(
        self,
        action: str,
        context: RuleTableContext,
        medication_assessments: tuple[CurrentMedicationAssessment, ...] = (),
    ) -> tuple[str, ...]:
        motor2 = self._motor2_current_assessment(context)
        motor2_lines = (
            (
                f"Motor 2: {motor2.strategy_text}",
                f"Motor 2 status: {motor2.dose_status}; regra: {motor2.reason}.",
            )
            if motor2
            else ()
        )
        return (
            f"Base de decisao: {'diagnostico informado' if self._has_defined_diagnosis(context) else 'fenotipo clinico sem diagnostico fechado'}.",
            f"Diagnostico/contexto informado: {context.diagnostic_context or 'nao informado'}.",
            f"Apresentacao clinica: {context.clinical_presentation or 'nao informada'}.",
            f"Estabilidade clinica: {context.stability or 'nao informada'}.",
            f"Sintomas-alvo: {', '.join(context.symptoms) if context.symptoms else 'nao informados'}.",
            *self._residual_target_lines(context),
            f"Eixos clinicos a cobrir: {', '.join(context.clinical_axes) if context.clinical_axes else 'nao definidos'}.",
            *self._axis_coverage_lines(context),
            f"Prejuizo funcional: {', '.join(context.impairment_domains) if context.impairment_domains else 'nao informado'}; gravidade: {context.impairment_severity or 'nao informada'}.",
            f"Perfil farmacologico desejado: {', '.join(context.pharmacological_profile) if context.pharmacological_profile else 'nao informado'}.",
            f"Receita atual: {', '.join(item.name for item in context.medications) if context.medications else 'sem medicacao em uso registrada'}.",
            *self._regimen_axis_lines(context),
            *tuple(item.summary() for item in medication_assessments),
            *motor2_lines,
            *self._risk_context_lines(context),
            self._action_reason(action),
            "Resposta gerada por matriz farmacologica local do PsychRx, com filtro de fenotipo e uso por doenca/quadro antes do ranking.",
        )

    def _action_reason(self, action: str) -> str:
        reasons = {
            "maintain": "Estabilidade favorece continuidade e monitorizacao.",
            "increase_dose": "Resposta parcial com tolerabilidade favoravel favorece revisar dose, tempo de uso e faixa terapeutica antes de trocar.",
            "optimize_current": "Dose atual ja pode estar na faixa cadastrada; resposta parcial sugere revisar tempo, adesao, tolerabilidade e quais sintomas ou prejuizos permanecem antes de discutir troca/associacao.",
            "substitute": "Sem resposta com medicacao atual favorece discutir troca apos confirmar dose, tempo e adesao adequados.",
            "associate": "Resposta parcial com eixo clinico ainda sem cobertura clara favorece discutir cobertura adicional desse eixo antes de trocar toda a receita.",
            "select_candidate": "Sem medicacao atual: a matriz compara candidatos farmacologicos contra sintomas, prejuizos, objetivo terapeutico e restricoes para revisao medica.",
            "investigate_before_change": "Instabilidade ou piora exige reavaliar contexto, risco, adesao e diagnostico antes de estrategia.",
            "insufficient_information": "Faltam dados suficientes para comparar manter, otimizar, substituir ou associar.",
        }
        return reasons.get(action, "Acao nao mapeada na tabela local.")

    def _residual_target_lines(self, context: RuleTableContext) -> tuple[str, ...]:
        """Explain what may remain without converting a snapshot into longitudinal fact."""
        response_states = (
            context.stability,
            *(medication.response for medication in context.medications),
        )
        if not any("parcial" in str(item).strip().lower() for item in response_states):
            return ()
        if context.symptoms:
            return (
                "Alvo residual ainda nao confirmado longitudinalmente. "
                "Sintomas atuais a verificar como persistentes: "
                f"{', '.join(context.symptoms)}.",
            )
        return (
            "Alvo residual nao definido: registrar quais sintomas ou prejuizos "
            "persistem e seu impacto funcional antes de discutir troca ou associacao.",
        )

    def _medication_action_explanations(
        self,
        context: RuleTableContext,
        medication_assessments: tuple[CurrentMedicationAssessment, ...] = (),
        *,
        safety_blocked: bool = False,
    ) -> tuple[MedicationActionExplanationPayload, ...]:
        """Compare four strategies and evidence separately for each medication."""
        assessments = medication_assessments or self._medication_assessment.assess_all(
            context.medications
        )
        explanations: list[MedicationActionExplanationPayload] = []
        for medication, assessment in zip(context.medications, assessments):
            if safety_blocked:
                reason = (
                    "Nao avaliavel agora: a prioridade de seguranca precisa ser "
                    "resolvida antes de comparar estrategias farmacologicas."
                )
                explanations.append(
                    MedicationActionExplanationPayload(
                        medication_name=medication.name,
                        maintain_reason=reason,
                        increase_reason=reason,
                        substitute_reason=reason,
                        associate_reason=reason,
                        evidence_level=(
                            "Nao aplicavel a decisao neste momento: o Safety First "
                            "Engine interrompeu a comparacao."
                        ),
                    )
                )
                continue

            motor2 = self._motor2_assessment_for_medication(context, medication)
            dose_status = (
                motor2.dose_status if motor2 and motor2.row else assessment.current_dose_status
            )
            response_status = assessment.response_status
            tolerability_status = assessment.tolerability_status
            adherence_status = assessment.adherence_status
            duration_status = assessment.duration_status
            good_tolerability = tolerability_status in {
                "good_tolerability",
                "mild_adverse_effects",
            }
            uncovered_axes = self._uncovered_clinical_axes(context)

            if response_status == "good_response" and good_tolerability:
                maintain_reason = (
                    "Favorecida: ha boa resposta e tolerabilidade aceitavel; manter "
                    "preserva o beneficio enquanto a resposta e monitorada."
                )
            elif response_status == "partial_response":
                maintain_reason = (
                    "Condicional: existe resposta parcial; manter depende de confirmar "
                    "tempo, adesao, tolerabilidade e quais sintomas ou prejuizos persistem."
                )
            elif response_status == "no_response":
                maintain_reason = (
                    "Nao favorecida como estrategia isolada: foi registrada ausencia "
                    "de resposta; antes de insistir, revisar dose, tempo, adesao e diagnostico."
                )
            else:
                maintain_reason = "Nao avaliavel: a resposta clinica deste medicamento nao foi definida."

            if dose_status.startswith("below") and good_tolerability:
                increase_reason = (
                    "Favorecida para discussao medica: a dose esta abaixo da faixa "
                    "comparavel e a tolerabilidade registrada permite revisar otimizacao."
                )
            elif dose_status.startswith("within"):
                increase_reason = (
                    "Nao favorecida automaticamente: a dose ja esta dentro da faixa "
                    "comparavel; aumentar exige beneficio esperado e monitorizacao adicionais."
                )
            elif dose_status.startswith("above"):
                increase_reason = (
                    "Nao favorecida: a dose esta acima da faixa comparavel; revisar "
                    "seguranca antes de qualquer ajuste."
                )
            else:
                increase_reason = (
                    "Nao avaliavel: falta uma dose ou faixa numerica comparavel para "
                    "sustentar aumento."
                )

            adequate_trial = (
                duration_status == "duration_possibly_sufficient"
                and adherence_status == "good_adherence"
            )
            if response_status == "no_response" and dose_status.startswith(
                ("within", "above")
            ) and adequate_trial:
                substitute_reason = (
                    "Favorecida para discussao medica: nao houve resposta apesar de "
                    "dose em faixa comparavel, tempo possivelmente suficiente e boa adesao."
                )
            elif response_status == "no_response":
                substitute_reason = (
                    "Condicional: a ausencia de resposta favorece revisar troca, mas "
                    "ainda e necessario confirmar dose, tempo e adesao adequados."
                )
            elif response_status == "partial_response":
                substitute_reason = (
                    "Nao favorecida de imediato: existe resposta parcial; primeiro "
                    "confirmar o que permanece e se a estrategia atual pode ser otimizada."
                )
            elif response_status == "good_response":
                substitute_reason = (
                    "Nao favorecida: ha boa resposta registrada e nao foi demonstrado "
                    "um motivo clinico para perder o beneficio atual."
                )
            else:
                substitute_reason = "Nao avaliavel: a resposta clinica ainda nao foi definida."

            if response_status == "partial_response" and uncovered_axes:
                associate_reason = (
                    "Condicionalmente favorecida: ha resposta parcial e eixo sem "
                    f"cobertura clara ({', '.join(uncovered_axes)}); confirmar alvo, "
                    "interacoes e carga de efeitos adversos antes de potencializar."
                )
            elif response_status == "partial_response":
                associate_reason = (
                    "Nao favorecida automaticamente: ha resposta parcial, mas nenhum "
                    "eixo adicional sem cobertura clara foi demonstrado."
                )
            elif response_status == "no_response":
                associate_reason = (
                    "Nao favorecida antes da revisao: sem resposta, primeiro confirmar "
                    "adequacao do ensaio, diagnostico e necessidade de troca."
                )
            elif response_status == "good_response":
                associate_reason = (
                    "Nao favorecida: ha boa resposta e nao foi demonstrado eixo residual "
                    "que justifique aumentar a carga farmacologica."
                )
            else:
                associate_reason = "Nao avaliavel: resposta e eixo adicional nao foram definidos."

            substitution_candidate = None
            if substitute_reason.startswith(("Favorecida", "Condicional")):
                substitution_candidate = self._substitution_candidate_for_medication(
                    context, medication
                )

            explanations.append(
                MedicationActionExplanationPayload(
                    medication_name=medication.name,
                    maintain_reason=maintain_reason,
                    increase_reason=increase_reason,
                    substitute_reason=substitute_reason,
                    associate_reason=associate_reason,
                    evidence_level=self._medication_evidence_level(assessment, motor2),
                    substitution_candidate=substitution_candidate,
                )
            )
        return tuple(explanations)

    def _substitution_candidate_for_medication(
        self,
        context: RuleTableContext,
        medication: CurrentMedicationPayload,
    ) -> MedicationOptionPayload | None:
        """Return a traceable candidate for one medication-specific switch review."""
        axis_text = medication.reason_for_use or " ".join(context.clinical_axes)
        target = self._target_for_axes_text(axis_text.lower(), context)
        candidates = self._medication_table.substitution_candidates(
            target=target,
            current_names=tuple(item.name for item in context.medications),
        )
        if not candidates:
            return None
        return self._candidate_to_option(
            candidates[0], "substitution_candidate", target
        )

    def _medication_evidence_level(self, assessment, motor2) -> str:
        """Describe traceability without inventing an evidence-strength grade."""
        labels: list[str] = []
        if assessment.source:
            source_id = assessment.source.source_id.upper()
            if source_id.startswith("DM-"):
                labels.append("DM")
            elif "TABELA-MOTOR" in source_id:
                labels.append("TM")
            else:
                labels.append(assessment.source.source_id)
        if motor2 and motor2.row:
            source_text = (
                f"{motor2.row.range_source}; {motor2.row.dose_effect_source}"
            ).upper()
            source_markers = (
                ("TM/ABA 1", "TM/T1"),
                ("DAILYMED", "DM"),
                ("DM:", "DM"),
                ("FDA", "DM"),
                ("STAHL_ESSENTIAL", "ST-E"),
                ("STAHL ESSENTIAL", "ST-E"),
                ("STAHL_PG", "ST-PG"),
                ("STAHL PG", "ST-PG"),
                ("GOODMAN", "GG"),
                ("ANVISA", "ANVISA"),
            )
            labels.extend(
                label for marker, label in source_markers if marker in source_text
            )
        if "TM/T1" in labels:
            labels = [label for label in labels if label != "TM"]
        sources = "/".join(dict.fromkeys(labels)) or "PENDENTE"
        if motor2 and motor2.row and self._formally_validated_status(
            motor2.row.evidence_status
        ):
            return (
                "Governada para runtime: fonte rastreavel e status formalmente "
                f"validado; a decisao continua sujeita ao contexto clinico ({sources})."
            )
        if sources != "PENDENTE":
            return (
                "Rastreavel, com forca comparativa ainda nao classificada: existem "
                f"fontes para faixa/perfil, mas nao um grau forte/moderado da decisao ({sources})."
            )
        return (
            "Pendente: nenhuma fonte aplicavel foi demonstrada para graduar esta "
            "decisao por medicamento (PENDENTE)."
        )

    def _regimen_axis_lines(self, context: RuleTableContext) -> tuple[str, ...]:
        """Return a compact map of the current medication regimen by axis."""
        if not context.medications:
            return ()
        mapped: list[str] = []
        for medication in context.medications:
            axis = medication.reason_for_use or self._infer_medication_axis(medication.name)
            dose = " ".join(
                item
                for item in (
                    medication.dose_used or medication.dose_value or medication.dose_prescribed,
                    medication.dose_unit,
                    medication.frequency,
                )
                if item
            )
            mapped.append(f"{medication.name}{f' {dose}' if dose else ''} -> {axis}")
        return (f"Regime atual por eixos: {'; '.join(mapped)}.",)

    def _axis_coverage_lines(self, context: RuleTableContext) -> tuple[str, ...]:
        if not context.clinical_axes:
            return ()
        covered = self._covered_clinical_axes(context)
        uncovered = self._uncovered_clinical_axes(context)
        return (
            f"Eixos cobertos pela receita: {', '.join(covered) if covered else 'nenhum eixo coberto identificado'}.",
            f"Eixos sem cobertura clara: {', '.join(uncovered) if uncovered else 'nenhum eixo descoberto'}.",
        )

    def _covered_clinical_axes(self, context: RuleTableContext) -> tuple[str, ...]:
        covered: list[str] = []
        medication_axes = tuple(
            medication.reason_for_use or self._infer_medication_axis(medication.name)
            for medication in context.medications
        )
        for required in context.clinical_axes:
            if any(self._axis_matches(required, medication_axis) for medication_axis in medication_axes):
                covered.append(required)
        return tuple(dict.fromkeys(covered))

    def _uncovered_clinical_axes(self, context: RuleTableContext) -> tuple[str, ...]:
        covered = set(self._covered_clinical_axes(context))
        return tuple(axis for axis in context.clinical_axes if axis not in covered)

    @staticmethod
    def _axis_matches(required: str, medication_axis: str) -> bool:
        required_text = DecisionSupportRuleTable._normalize_text(required)
        medication_text = DecisionSupportRuleTable._normalize_text(medication_axis)
        if required_text == medication_text:
            return True
        aliases = {
            "humor/tept": ("humor", "ansiedade", "tept", "antidepressivo"),
            "sono/sedacao": ("sono", "sedacao"),
            "ansiedade/resgate": ("ansiedade", "resgate"),
            "impulsividade/irritabilidade": ("impulsividade", "irritabilidade"),
            "compulsividade/toc": ("compulsividade", "toc", "obsessivo", "serotonergico"),
            "substancias/craving": ("substancias", "craving", "dependencia"),
            "dor/sintomas somaticos": ("dor", "somaticos", "fibromialgia"),
            "energia/cognicao": ("energia", "cognicao", "ativacao"),
            "libido/funcao sexual": ("libido", "sexual"),
            "peso/metabolico": ("peso", "metabolico"),
            "estabilizacao do humor": ("estabilizacao", "bipolar", "humor"),
            "psicose/organizacao do pensamento": ("psicose", "organizacao", "antipsicotico"),
            "efeito adverso/contramedicacao": ("efeito adverso", "contramedicacao"),
        }
        return any(token in medication_text for token in aliases.get(required_text, (required_text,)))

    @staticmethod
    def _infer_medication_axis(name: str) -> str:
        """Infer the practical axis when the physician has not filled it yet."""
        normalized = DecisionSupportRuleTable._normalize_text(name)
        if any(token in normalized for token in ("unialtrex", "naltrexona")):
            return "substancias/craving"
        if any(token in normalized for token in ("trazodona", "zolpidem", "zopiclona")):
            return "sono/sedacao"
        if any(token in normalized for token in ("rivotril", "clonazepam", "lexotan", "bromazepam", "diazepam", "alprazolam", "lorazepam")):
            return "ansiedade/resgate"
        if any(token in normalized for token in ("fluoxetina", "sertralina", "escitalopram", "citalopram", "paroxetina", "fluvoxamina")):
            return "humor/ansiedade/TEPT"
        if any(token in normalized for token in ("litio", "lamotrigina", "valproato", "carbamazepina")):
            return "estabilizacao do humor"
        if any(token in normalized for token in ("quetiapina", "risperidona", "olanzapina", "aripiprazol", "haloperidol", "amisulprida")):
            return "psicose/organizacao do pensamento ou potencializacao"
        return "eixo nao definido"

    @staticmethod
    def _normalize_text(value: str) -> str:
        import unicodedata

        text = unicodedata.normalize("NFKD", str(value or "").lower())
        return text.encode("ascii", "ignore").decode("ascii")

    def _risk_context_lines(self, context: RuleTableContext) -> tuple[str, ...]:
        consequences = self._risk_consequences(context)
        if not consequences:
            return ()
        return tuple(
            f"Risco avaliado: {risk} -> consequencia operacional: {effect}."
            for risk, effect in consequences
        )

    def _risk_warnings(self, context: RuleTableContext) -> tuple[str, ...]:
        return tuple(
            f"{risk}: {effect}"
            for risk, effect in self._risk_consequences(context)
            if effect in {"CAUTELA", "REDUZIR_COMPATIBILIDADE", "EXIGIR_REVISAO_MEDICA", "BLOQUEAR_OPCAO", "AVALIACAO_URGENTE"}
        )

    @staticmethod
    def _risk_consequences(context: RuleTableContext) -> tuple[tuple[str, str], ...]:
        mapping = {
            "Gestacao": "EXIGIR_REVISAO_MEDICA",
            "Lactacao": "EXIGIR_REVISAO_MEDICA",
            "Idoso": "CAUTELA",
            "Obesidade": "REDUZIR_COMPATIBILIDADE",
            "Diabetes": "REDUZIR_COMPATIBILIDADE",
            "Doenca renal": "CAUTELA",
            "Doenca hepatica": "CAUTELA",
            "Epilepsia": "BLOQUEAR_OPCAO",
            "Glaucoma": "CAUTELA",
            "Retencao urinaria": "CAUTELA",
            "QT prolongado": "BLOQUEAR_OPCAO",
            "Risco cardiovascular": "EXIGIR_REVISAO_MEDICA",
            "Uso de substancias": "EXIGIR_REVISAO_MEDICA",
            "Interacoes relevantes": "EXIGIR_REVISAO_MEDICA",
            "Fitoterapicos e suplementos": "INFORMAR",
            "Alergia ou reacao grave anterior": "BLOQUEAR_OPCAO",
        }
        return tuple(
            (item, mapping[item])
            for item in context.comorbidities
            if item in mapping
        )

    def _pharmacological_target(
        self,
        context: RuleTableContext,
        target: str,
        action: str,
        ranked_options=(),
    ) -> PharmacologicalTargetPayload:
        dose_medication = self._dose_target_medication(context, action, ranked_options)
        indication_range = self._indication_dose_matrix.range_for(
            medication_name=dose_medication,
            clinical_presentation=context.clinical_presentation,
            symptoms=context.symptoms,
            pharmacological_profile=context.pharmacological_profile,
            impairment_domains=context.impairment_domains,
            diagnostic_context=context.diagnostic_context,
            therapeutic_objective=context.therapeutic_objective,
        )
        if indication_range:
            dose_target = (
                f"{indication_range.medication} / {indication_range.condition_label}: "
                f"{indication_range.range_text}"
            )
            dose_source = indication_range.source
        else:
            dose_target = f"{dose_medication or 'medicamento'} / faixa por quadro: nao cadastrado"
            dose_source = self._operational_citation("Aba 1 dose range not registered")
        dose_profile = self._dose_profile_table.find(dose_medication)
        return PharmacologicalTargetPayload(
            impairment_domain=", ".join(context.impairment_domains) or "nao informado",
            symptom_target=", ".join(context.symptoms) or "nao informado",
            pharmacological_target=target,
            therapeutic_dose_target=dose_target,
            dose_source=dose_source or self._operational_citation("Dose target policy"),
            dose_dependent_profile=(
                dose_profile.display_summary()
                if dose_profile
                else f"Dose - efeito: pendente pesquisar para {dose_medication or 'medicamento'}."
            ),
            dose_profile_source=(
                dose_profile.citation()
                if dose_profile
                else self._operational_citation("Dose-dependent profile pending")
            ),
        )

    @staticmethod
    def _dose_target_medication(
        context: RuleTableContext,
        action: str,
        ranked_options=(),
    ) -> str:
        if action in {
            "maintain",
            "increase_dose",
            "optimize_current",
            "decrease_dose",
            "taper_or_withdraw",
        }:
            return context.medications[0].name if context.medications else ""
        if ranked_options:
            return ranked_options[0].name
        return context.medications[0].name if context.medications else ""

    def _disease_use_summary(
        self,
        context: RuleTableContext,
        action: str,
        ranked_options=(),
        phenotype: PhenotypeAssessment | None = None,
    ) -> tuple[str, ...]:
        phenotype = phenotype or self._phenotype_filter.assess(
            clinical_presentation=context.clinical_presentation,
            diagnostic_context=context.diagnostic_context,
            symptoms=context.symptoms,
            observed_signs=context.observed_signs,
            pharmacological_profile=context.pharmacological_profile,
            safety=context.safety,
        )
        medication = self._dose_target_medication(context, action, ranked_options)
        return self._disease_use_filter.summary_for(
            medication,
            diagnostic_context=context.diagnostic_context,
            phenotype=phenotype,
            limit=4,
        )

    def _interaction_summary(self, context: RuleTableContext) -> tuple[str, ...]:
        if not context.medications:
            return ("Sem receita atual para cruzar interacoes.",)
        findings = self._interaction_table.findings(
            context.medications,
            comorbidities=context.comorbidities,
            safety=context.safety,
        )
        if not findings:
            return ("Sem interacao prioritaria cadastrada para os dados informados. Fonte: TM/PENDENTE.",)
        return tuple(finding.display_line() for finding in findings[:6])

    def _substitution_options(
        self,
        action: str,
        context: RuleTableContext,
        target: str,
        ranked_options=(),
    ) -> tuple[MedicationOptionPayload, ...]:
        if ranked_options and action in {"substitute", "select_candidate"}:
            role = (
                "initiation_candidate"
                if action == "select_candidate"
                else "substitution_candidate"
            )
            options: list[MedicationOptionPayload] = []
            for option in ranked_options[:5]:
                dose_guidance, dose_source = self._medication_table.current_dose_target(
                    option.name
                )
                evidence = tuple(
                    dict.fromkeys(
                        citation
                        for citation in (option.citation, dose_source)
                        if citation is not None
                    )
                )
                options.append(
                    MedicationOptionPayload(
                        name=f"{option.name} (pontuacao {option.score})",
                        role=role,
                        reason=option.reason,
                        pharmacological_target=", ".join(option.matched_targets),
                        dose_guidance=dose_guidance if dose_source else "",
                        evidence=evidence,
                        safety_notes=option.caution_hits,
                    )
                )
            return tuple(options)
        if action not in {"substitute", "select_candidate"}:
            return ()
        if action not in {
            "substitute",
            "select_candidate",
            "investigate_before_change",
            "insufficient_information",
        }:
            return ()
        candidates = self._medication_table.substitution_candidates(
            target=target,
            current_names=tuple(item.name for item in context.medications),
        )
        role = (
            "initiation_candidate"
            if action == "select_candidate"
            else "substitution_candidate"
        )
        return tuple(
            self._candidate_to_option(candidate, role, target)
            for candidate in candidates
        ) or (
            MedicationOptionPayload(
                name="Candidato farmacologico pendente",
                role=role,
                reason=(
                    "A matriz farmacologica ainda nao encontrou candidato para este alvo. "
                    "Revisar se a medicacao atual esta cadastrada e se o sintoma/prejuizo "
                    "foi mapeado na tabela."
                ),
                pharmacological_target=target,
                unresolved_reason="candidate_not_in_local_medication_table",
            ),
        )

    def _association_options(
        self, action: str, context: RuleTableContext, target: str
    ) -> tuple[MedicationOptionPayload, ...]:
        if action not in {
            "associate",
            "optimize_current",
            "increase_dose",
            "investigate_before_change",
            "insufficient_information",
        }:
            return ()
        candidates = self._medication_table.association_candidates(
            target=target,
            current_names=tuple(item.name for item in context.medications),
        )
        return tuple(
            self._candidate_to_option(candidate, "association_candidate", target)
            for candidate in candidates
        ) or (
            MedicationOptionPayload(
                name="Associacao posterior pendente",
                role="association_candidate",
                reason=(
                    "A tabela prioriza otimizar o tratamento atual. Associacao fica "
                    "pendente se nao houver candidato rastreado para o sintoma, "
                    "prejuizo ou eixo ainda sem cobertura."
                ),
                pharmacological_target=target,
                unresolved_reason="association_candidate_not_in_local_medication_table",
            ),
        )

    def _candidate_to_option(
        self,
        candidate: MedicationStrategyEntry,
        role: str,
        target: str,
    ) -> MedicationOptionPayload:
        if role == "initiation_candidate":
            action_label = "opcao inicial"
        elif role == "substitution_candidate":
            action_label = "substituicao"
        else:
            action_label = "associacao"
        cautions = "; ".join(candidate.cautions) if candidate.cautions else "cautelas nao informadas"
        return MedicationOptionPayload(
            name=candidate.name,
            role=role,  # type: ignore[arg-type]
            reason=(
                f"Candidato de {action_label} para revisao medica porque a Tabela Motor "
                f"vincula {candidate.name} ao alvo {target}. Classe: "
                f"{candidate.drug_class}. Faixa informativa: {candidate.usual_adult_range}. "
                f"Cautelas da tabela: {cautions}."
            ),
            drug_class=candidate.drug_class,
            pharmacological_target=", ".join(candidate.targets),
            dose_guidance=candidate.usual_adult_range,
            evidence=(candidate.source, self._operational_citation(f"{action_label} candidate mapping")),
            safety_notes=candidate.cautions,
        )

    def _action_evidence(
        self, action: str, context: RuleTableContext, ranked_options=()
    ) -> ActionEvidencePayload:
        target = self._target(context)
        citations = list(self._candidate_citations(context, target))
        citations.extend(option.citation for option in ranked_options)
        citations.append(self._operational_citation("Local decision table"))
        return ActionEvidencePayload(
            action=action,
            rationale=(
                "Matriz farmacologica aplicada ao encadeamento clinico-operacional: contexto "
                "clinico, estado atual, sintomas-alvo, prejuizo funcional, gravidade, "
                "perfil desejado, receita atual e seguranca. O motor define estrategia, "
                "detecta fenotipo, aplica uso por doenca/quadro e so entao pontua candidatos elegiveis."
            ),
            citations=tuple(dict.fromkeys(citations)),
        )

    def _ranked_options(self, context: RuleTableContext):
        return self._pharmacological_matrix.rank(
            presentation=context.clinical_presentation,
            symptoms=context.symptoms,
            pharmacological_profile=(*context.pharmacological_profile, *context.clinical_axes),
            impairment_domains=(*context.impairment_domains, *context.clinical_axes),
            restrictions=context.comorbidities,
            current_medications=tuple(item.name for item in context.medications),
            limit=15,
        )

    def _filtered_ranked_options(
        self,
        ranked_options,
        *,
        context: RuleTableContext,
        action: str,
        phenotype: PhenotypeAssessment,
    ):
        if action not in {"substitute", "select_candidate", "associate"}:
            return ranked_options, ()
        return self._disease_use_filter.filter_ranked_options(
            ranked_options,
            diagnostic_context=context.diagnostic_context,
            strategy=self._strategy_code(action, context),
            phenotype=phenotype,
        )

    @staticmethod
    def _requires_candidate(action: str) -> bool:
        return action in {"substitute", "select_candidate", "associate"}

    @staticmethod
    def _has_defined_diagnosis(context: RuleTableContext) -> bool:
        text = context.diagnostic_context.lower()
        return bool(text and "nao informado" not in text and "investigacao" not in text)

    @staticmethod
    def _first_number(text: str) -> float | None:
        match = re.search(r"\d+(?:[.,]\d+)?", str(text))
        if not match:
            return None
        return float(match.group(0).replace(",", "."))

    @staticmethod
    def _range_numbers(text: str) -> tuple[float, float] | None:
        values = [
            float(item.replace(",", "."))
            for item in re.findall(r"\d+(?:[.,]\d+)?", str(text))
        ]
        if not values:
            return None
        if len(values) == 1:
            return values[0], values[0]
        return min(values), max(values)

    @staticmethod
    def _strategy_code(action: str, context: RuleTableContext) -> str:
        if action == "maintain":
            return "KEEP_CURRENT"
        if action in {"increase_dose", "optimize_current"}:
            return "OPTIMIZE_DOSE"
        if action == "substitute":
            return "SWITCH_MONOTHERAPY"
        if action == "select_candidate":
            return "INITIAL_MONOTHERAPY"
        if action == "associate":
            return "AUGMENT"
        if action == "taper_or_withdraw":
            return "TAPER_OR_STOP"
        return "NO_DRUG_RECOMMENDATION"

    def _candidate_dose_targets(
        self, context: RuleTableContext, target: str
    ) -> tuple[str, EvidenceCitationPayload | None]:
        candidates = self._all_candidates(context, target)
        if not candidates:
            return "", None
        lines = []
        for candidate in candidates[:4]:
            lines.append(f"{candidate.name}: {candidate.usual_adult_range}")
        return "; ".join(lines), candidates[0].source

    def _candidate_citations(
        self, context: RuleTableContext, target: str
    ) -> tuple[EvidenceCitationPayload, ...]:
        citations: list[EvidenceCitationPayload] = []
        current = context.medications[0].name if context.medications else ""
        current_entry = self._medication_table.find_current(current)
        if current_entry:
            citations.append(current_entry.source)
        citations.extend(candidate.source for candidate in self._all_candidates(context, target))
        return tuple(citations)

    def _all_candidates(
        self, context: RuleTableContext, target: str
    ) -> tuple[MedicationStrategyEntry, ...]:
        current_names = tuple(item.name for item in context.medications)
        candidates = (
            self._medication_table.substitution_candidates(target, current_names)
            + self._medication_table.association_candidates(target, current_names)
        )
        unique: dict[str, MedicationStrategyEntry] = {}
        for candidate in candidates:
            unique.setdefault(candidate.name, candidate)
        return tuple(unique.values())

    def _rejected_alternatives(self, action: str) -> tuple[str, ...]:
        if action in {"increase_dose", "optimize_current"}:
            return (
                "Substituicao imediata fica em segundo plano enquanto ha resposta parcial e tolerabilidade aceitavel.",
                "Associacao imediata fica pendente antes de revisar dose atual, tempo de uso e quais sintomas ou prejuizos permanecem.",
            )
        if action == "substitute":
            return (
                "Manter sem revisar estrategia rejeitado pela tabela porque ha sem resposta registrada.",
                "Aumento automatico de dose nao e definido sem confirmar faixa terapeutica e tolerabilidade.",
            )
        return ()

    def _monitoring_targets(
        self, context: RuleTableContext, *, action: str = ""
    ) -> tuple[str, ...]:
        return self._monitoring_governance.assess(
            symptoms=context.symptoms,
            action=action,
            medications=context.medications,
        ).targets

    def _confidence(self, context: RuleTableContext) -> str:
        score = 0
        score += bool(context.symptoms)
        score += bool(context.impairment_domains)
        score += context.stability.lower() not in {"", "nao definido"}
        score += bool(context.medications)
        score += not self._safety_warnings(context)
        if score >= 5:
            return "high_structural"
        if score >= 3:
            return "moderate_structural"
        return "low_structural"

    def _evidence_governance(
        self,
        context: RuleTableContext,
        ranked_options,
        eligibilities: tuple[MedicationEligibility, ...],
    ) -> tuple[tuple[str, ...], str]:
        statuses: list[str] = []
        lines: list[str] = []
        for option in ranked_options:
            status = str(getattr(option, "evidence_status", "") or "status_not_recorded")
            statuses.append(status)
            lines.append(f"Matriz farmacologica / {option.name}: {status}")
        for item in eligibilities:
            status = item.evidence_status or "status_not_recorded"
            statuses.append(status)
            lines.append(f"Uso por quadro / {item.medication_name}: {status}")
        motor2 = self._motor2_current_assessment(context)
        if motor2 and motor2.row:
            status = motor2.row.evidence_status or "status_not_recorded"
            statuses.append(status)
            lines.append(f"Motor 2 / {motor2.row.medication_name}: {status}")
        readiness = (
            "scientifically_runtime_eligible"
            if statuses and all(self._formally_validated_status(item) for item in statuses)
            else "structural_only_scientific_review_pending"
        )
        if not lines:
            lines.append("Nenhuma linha cientificamente elegivel foi demonstrada para esta resposta.")
        return tuple(dict.fromkeys(lines)), readiness

    @staticmethod
    def _formally_validated_status(status: str) -> bool:
        normalized = str(status or "").lower()
        return (
            ("validated" in normalized or "aprovad" in normalized)
            and "pending" not in normalized
            and "pendente" not in normalized
        )

    def _safety_warnings(self, context: RuleTableContext) -> tuple[str, ...]:
        assessment = self._safety_assessment.assess(
            context.safety,
            has_current_medication=bool(context.medications),
        )
        return assessment.warnings

    def _operational_citation(self, section: str) -> EvidenceCitationPayload:
        return EvidenceCitationPayload(
            source_id="PSYCHRX-LOCAL-RULE-TABLE",
            title="PsychRx Local Decision-Support Rule Table",
            organization="PsychRx",
            year="2026",
            section=section,
            excerpt_anchor=section.lower().replace(" ", "-"),
            evidence_type="operational_rule",
            quality="local_structural_logic",
            applicability="physician_review_only",
            limitations="Nao substitui evidencia cientifica publicada nem julgamento medico.",
        )
