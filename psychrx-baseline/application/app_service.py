"""Application service for the local PsychRx app shell."""

from __future__ import annotations

from application.app_view_model import (
    ClinicalExperienceComponentViewModel,
    ClinicalExplanationStatusViewModel,
    ClinicalIntelligenceStatusViewModel,
    ClinicalNavigationStatusViewModel,
    ClinicalOperatingMindStatusViewModel,
    ClinicalQualityStatusViewModel,
    ClinicalResearchStatusViewModel,
    ClinicalSimulationStatusViewModel,
    ClinicalSnapshotStatusViewModel,
    ClinicalTimelineStatusViewModel,
    ConsultationCardViewModel,
    ConsultationRegionViewModel,
    DashboardPanelViewModel,
    DigitalClinicalTwinStatusViewModel,
    EvidenceRuntimeStatusViewModel,
    KernelStatusViewModel,
    KnowledgeGovernanceStatusViewModel,
    PsychRxAppViewModel,
    RoadmapTrackViewModel,
    RuntimeStatusViewModel,
    SafetyEngineStatusViewModel,
    ScientificValidationStatusViewModel,
    SafetyGuardrailViewModel,
    TherapeuticOptimizationStatusViewModel,
    WorkflowStepViewModel,
)
from application.kernel_adapter import ApplicationKernelAdapter
from clinical_research import ResearchCoordinator
from clinical_runtime import ClinicalRuntime
from clinical_intelligence import IntelligenceCoordinator
from clinical_simulation import SimulationCoordinator
from digital_clinical_twin import TwinCoordinator
from knowledge_governance_platform import GovernanceCoordinator
from scientific_validation import ValidationCoordinator


class PsychRxAppService:
    """Provides a read-only app state for the interface layer."""

    def __init__(
        self,
        kernel_adapter: ApplicationKernelAdapter | None = None,
        runtime: ClinicalRuntime | None = None,
        research_coordinator: ResearchCoordinator | None = None,
        scientific_validation: ValidationCoordinator | None = None,
        knowledge_governance: GovernanceCoordinator | None = None,
        digital_twin: TwinCoordinator | None = None,
        clinical_simulation: SimulationCoordinator | None = None,
        clinical_intelligence: IntelligenceCoordinator | None = None,
    ) -> None:
        self._kernel_adapter = kernel_adapter or ApplicationKernelAdapter()
        self._runtime = runtime or ClinicalRuntime()
        self._research_coordinator = research_coordinator or ResearchCoordinator()
        self._scientific_validation = scientific_validation or ValidationCoordinator()
        self._knowledge_governance = knowledge_governance or GovernanceCoordinator()
        self._digital_twin = digital_twin or TwinCoordinator()
        self._clinical_simulation = clinical_simulation or SimulationCoordinator()
        self._clinical_intelligence = clinical_intelligence or IntelligenceCoordinator()

    def get_app_view_model(self) -> PsychRxAppViewModel:
        """Return the complete read-only state consumed by the local UI."""
        kernel_result = self._kernel_adapter.get_kernel_result()
        return PsychRxAppViewModel(
            safety_guardrails=self._safety_guardrails(),
            clinical_workflow=self._clinical_workflow(),
            dashboard_panels=self._dashboard_panels(),
            roadmap_tracks=self._roadmap_tracks(),
            clinical_experience_components=self._clinical_experience_components(),
            consultation_regions=self._consultation_regions(kernel_result.blocked_reason),
            kernel_status=self._kernel_status(kernel_result),
            runtime_status=self._runtime_status(),
            safety_engine_status=self._safety_engine_status(),
            evidence_runtime_status=self._evidence_runtime_status(),
            therapeutic_optimization_status=self._therapeutic_optimization_status(),
            clinical_explanation_status=self._clinical_explanation_status(),
            clinical_snapshot_status=self._clinical_snapshot_status(),
            clinical_timeline_status=self._clinical_timeline_status(),
            clinical_navigation_status=self._clinical_navigation_status(),
            clinical_operating_mind_status=self._clinical_operating_mind_status(),
            clinical_quality_status=self._clinical_quality_status(),
            clinical_research_status=self._clinical_research_status(),
            scientific_validation_status=self._scientific_validation_status(),
            knowledge_governance_status=self._knowledge_governance_status(),
            digital_clinical_twin_status=self._digital_clinical_twin_status(),
            clinical_simulation_status=self._clinical_simulation_status(),
            clinical_intelligence_status=self._clinical_intelligence_status(),
            technical_registry=self._technical_registry(),
        )

    def _technical_registry(self) -> tuple[str, ...]:
        """Preserve structural integration labels without rendering them as UI cards."""
        return (
            "Kernel Status Widget",
            "Runtime Status Widget",
            "Safety Engine Status Widget",
            "Evidence Runtime Status Widget",
            "Therapeutic Optimization Status Widget",
            "Clinical Explanation Engine Status Widget",
            "Clinical Snapshot Engine Status Widget",
            "Clinical Timeline Engine Status Widget",
            "Clinical Navigation Engine Status Widget",
            "Clinical Operating Mind Status Widget",
            "Clinical Quality Engine Status Widget",
            "Clinical Research Platform Status Widget",
            "Scientific Validation Framework Status Widget",
            "Knowledge Governance Platform Status Widget",
            "Digital Clinical Twin Platform Status Widget",
            "Clinical Simulation Platform Status Widget",
            "Clinical Intelligence Platform Status Widget",
            "ClinicalExplanationResult",
            "ClinicalSimulationResult",
            "ClinicalOperatingMind",
            "ClinicalResearchResult",
            "ClinicalTimeline",
            "ClinicalNavigationState",
            "ClinicalQualityResult",
            "ClinicalSnapshot",
            "ClinicalIntelligenceResult",
            "DigitalClinicalTwin",
            "EvidenceResult",
            "SafetyResult",
            "TherapeuticOptimizationResult",
            "KnowledgeGovernanceResult",
            "ScientificValidationResult",
            "Evidence Graph Runtime",
            "Therapeutic Optimization Runtime",
            "Strategy Widget",
            "Monitoring Widget",
            "Investigation Workflow",
            "Clinical Compass",
            "Missing Information Widget",
            "Consultation Progress Widget",
            "Dynamic Question States",
            "Clinical Widget Framework",
            "Widget Registry",
            "Widget State Model",
            "Widget Visibility Rules",
            "Consultation Timeline",
            "Medication Timeline",
            "Symptom Timeline",
            "Response Timeline",
            "Estrategias terapeuticas ainda nao disponiveis",
            "Safety before Optimization",
            "Publication Gate",
            "Runtime coordena execucao",
            "Runtime integration: forbidden",
            "Runtime mutation: forbidden",
            "Official Twin mutation: forbidden",
            "Runtime execution: forbidden",
            "Patient reality: not represented",
            "Scientific Validation alone: insufficient",
            "AI implementation: none",
            "Autonomous decision: forbidden",
        )

    def _safety_guardrails(self) -> tuple[SafetyGuardrailViewModel, ...]:
        return (
            SafetyGuardrailViewModel(
                "Medico como decisor final",
                "Toda saida deve apoiar revisao medica, nunca substituir decisao clinica.",
            ),
            SafetyGuardrailViewModel(
                "Seguranca antes de estrategia",
                "Riscos, restricoes e alertas aparecem antes de qualquer comparacao.",
            ),
            SafetyGuardrailViewModel(
                "Nenhuma prescricao automatica",
                "O app nao gera conduta, dose, troca, associacao ou descontinuacao.",
            ),
            SafetyGuardrailViewModel(
                "Rastreabilidade obrigatoria",
                "Informacao clinica futura deve apontar fonte, versao e justificativa.",
            ),
        )

    def _clinical_workflow(self) -> tuple[WorkflowStepViewModel, ...]:
        steps = (
            ("Paciente", "Manter o paciente no centro do raciocinio."),
            ("Clinical Snapshot", "Representar o estado clinico dinamico."),
            ("Perguntas", "Expor lacunas que reduzem incerteza."),
            ("Hipoteses", "Organizar possibilidades diagnosticas sem fechar conduta."),
            ("Objetivos", "Definir alvos terapeuticos a revisar pelo medico."),
            ("Restricoes", "Destacar limites, riscos e preferencias."),
            ("Seguranca", "Bloquear raciocinio inseguro antes de estrategia."),
            ("Estrategias", "Comparar alternativas apenas com justificativa."),
            ("Explicacao", "Mostrar por que algo foi considerado."),
            ("Monitorizacao", "Acompanhar resposta, estabilidade e eventos adversos."),
        )
        return tuple(
            WorkflowStepViewModel(order=index, name=name, purpose=purpose)
            for index, (name, purpose) in enumerate(steps, start=1)
        )

    def _dashboard_panels(self) -> tuple[DashboardPanelViewModel, ...]:
        return (
            DashboardPanelViewModel(
                "Risk Widget",
                "Tornar riscos clinicos visiveis antes de qualquer estrategia.",
                "Nao reduzir alerta nem liberar conduta.",
            ),
            DashboardPanelViewModel(
                "Strategy Panel",
                "Organizar alternativas comparaveis para revisao medica.",
                "Nao prescrever nem escolher pelo medico.",
            ),
            DashboardPanelViewModel(
                "Evidence Panel",
                "Exibir fonte, qualidade, conflito e aplicabilidade.",
                "Nao transformar evidencia em regra individual automatica.",
            ),
            DashboardPanelViewModel(
                "Monitoring Panel",
                "Relacionar acompanhamento a risco, resposta e estabilidade.",
                "Nao substituir seguimento medico.",
            ),
        )

    def _roadmap_tracks(self) -> tuple[RoadmapTrackViewModel, ...]:
        return (
            RoadmapTrackViewModel(
                "Arquitetura e Engenharia",
                "Software, contratos, API futura, infraestrutura e testes.",
            ),
            RoadmapTrackViewModel(
                "Conhecimento Cientifico",
                "Diretrizes, evidencias, psicofarmacos e governanca.",
            ),
            RoadmapTrackViewModel(
                "Experiencia Clinica",
                "Consulta, dashboard medico, mobile e comunicacao.",
            ),
            RoadmapTrackViewModel(
                "Qualidade e Governanca",
                "Auditoria, validacao cientifica, seguranca e rastreabilidade.",
            ),
            RoadmapTrackViewModel(
                "Inteligencia Clinica",
                "IA assistiva futura sem autonomia decisoria.",
            ),
        )

    def _clinical_experience_components(
        self,
    ) -> tuple[ClinicalExperienceComponentViewModel, ...]:
        return (
            ClinicalExperienceComponentViewModel(
                "Consultation Room",
                "Tela principal da consulta com paciente, sintomas, riscos, estrategias e monitorizacao.",
                "Organiza consulta; nao decide conduta.",
            ),
            ClinicalExperienceComponentViewModel(
                "Guided Anamnesis",
                "Sugere perguntas objetivas para reduzir incerteza durante a fala do paciente.",
                "Perguntas sao apoio; nao fazem diagnostico automatico.",
            ),
            ClinicalExperienceComponentViewModel(
                "Clinical Investigation Panel",
                "Mostra poucas perguntas prioritarias e lacunas clinicas relevantes no momento da consulta.",
                "Organiza investigacao; nao faz diagnostico, nao usa IA e nao substitui julgamento medico.",
            ),
            ClinicalExperienceComponentViewModel(
                "Symptom Capture",
                "Captura sintomas de forma rapida e estruturada.",
                "Nao interpreta sozinho nem substitui exame clinico.",
            ),
            ClinicalExperienceComponentViewModel(
                "Risk Widget",
                "Mostra categorias de risco clinico como informacao visual conceitual.",
                "Nao calcula risco real, nao emite alerta clinico real e nao substitui Safety Engine.",
            ),
            ClinicalExperienceComponentViewModel(
                "Objectives Widget",
                "Mostra objetivos terapeuticos conceituais para revisao medica.",
                "Nao calcula objetivo, nao prioriza conduta e nao recomenda tratamento.",
            ),
            ClinicalExperienceComponentViewModel(
                "Strategy Widget",
                "Mostra a area futura de estrategias terapeuticas, mantendo bloqueio ate Kernel, Safety e Evidencia.",
                "Nao exibe conduta, medicamento, dose, troca, manutencao ou ranking.",
            ),
            ClinicalExperienceComponentViewModel(
                "Monitoring Widget",
                "Organiza monitorizacao longitudinal conceitual.",
                "Nao gera plano real, exame obrigatorio ou intervalo clinico.",
            ),
            ClinicalExperienceComponentViewModel(
                "Clinical Compass",
                "Mostra estado geral da consulta em modo estatico.",
                "Nao calcula suficiencia, confianca diagnostica ou prontidao clinica.",
            ),
            ClinicalExperienceComponentViewModel(
                "Missing Information Widget",
                "Lista lacunas clinicas que ainda precisam ser esclarecidas.",
                "Nao infere lacunas automaticamente nem bloqueia decisao real.",
            ),
            ClinicalExperienceComponentViewModel(
                "Consultation Progress Widget",
                "Mostra progresso visual por dominio da consulta.",
                "Nao valida prontidao clinica nem desbloqueia estrategia.",
            ),
            ClinicalExperienceComponentViewModel(
                "Clinical Timeline",
                "Mostra a consulta e a evolucao longitudinal como sequencias conceituais.",
                "Nao classifica paciente e nao calcula resposta clinica.",
            ),
            ClinicalExperienceComponentViewModel(
                "Patient Friendly Mode",
                "Traduz objetivos e monitorizacao para linguagem acessivel ao paciente.",
                "Nao orienta automedicacao.",
            ),
        )

    def _kernel_status(self, kernel_result) -> KernelStatusViewModel:
        return KernelStatusViewModel(
            kernel_status=kernel_result.status,
            pipeline_status="structural_read_only",
            strategy_blocked_reason=kernel_result.blocked_reason,
            future_integrations=(
                "Safety Engine",
                "Evidence Graph Runtime",
                "Therapeutic Optimization Runtime",
                "Clinical Reasoning Engines",
            ),
            read_only_mode=True,
        )

    def _runtime_status(self) -> RuntimeStatusViewModel:
        execution = self._runtime.execute()
        return RuntimeStatusViewModel(
            runtime_status=str(execution["status"]),
            session_status=str(execution["session"]["status"]),
            pipeline_status=str(execution["result"]["status"]),
            event_bus_status="in_process_structural",
            audit_status="in_memory_structural",
            trace_status="structural",
            read_only_mode=True,
        )

    def _safety_engine_status(self) -> SafetyEngineStatusViewModel:
        execution = self._runtime.execute()
        safety_result = execution["safety_result"]
        snapshot = safety_result["snapshot"]
        blocking_decision = safety_result["blocking_decision"]
        return SafetyEngineStatusViewModel(
            engine_status=str(safety_result["status"]),
            snapshot_status=str(snapshot["status"]),
            blocking_status=str(blocking_decision["status"]),
            alert_count=int(snapshot["alert_count"]),
            blocking_count=int(snapshot["blocking_count"]),
            trace_id=str(safety_result["trace_id"]),
            read_only_mode=True,
        )

    def _evidence_runtime_status(self) -> EvidenceRuntimeStatusViewModel:
        execution = self._runtime.execute()
        evidence_result = execution["evidence_result"]
        snapshot = evidence_result["snapshot"]
        return EvidenceRuntimeStatusViewModel(
            runtime_status=str(evidence_result["status"]),
            selected_count=int(snapshot["selected_count"]),
            discarded_count=int(snapshot["discarded_count"]),
            citation_count=int(snapshot["citation_count"]),
            version_policy=str(snapshot["version_policy"]),
            trace_id=str(evidence_result["trace_id"]),
            read_only_mode=True,
        )

    def _therapeutic_optimization_status(
        self,
    ) -> TherapeuticOptimizationStatusViewModel:
        execution = self._runtime.execute()
        optimization_result = execution["optimization_result"]
        return TherapeuticOptimizationStatusViewModel(
            engine_status=str(optimization_result["status"]),
            candidate_count=len(optimization_result["candidate_strategies"]),
            evaluated_count=len(optimization_result["evaluated_strategies"]),
            hypothesis_count=len(optimization_result["hypotheses"]),
            uncertainty_count=len(optimization_result["uncertainties"]),
            confidence=float(optimization_result["confidence"]),
            trace_id=str(optimization_result["trace_id"]),
            read_only_mode=True,
        )

    def _clinical_explanation_status(self) -> ClinicalExplanationStatusViewModel:
        execution = self._runtime.execute()
        explanation_result = execution["explanation_result"]
        return ClinicalExplanationStatusViewModel(
            engine_status=str(explanation_result["status"]),
            section_count=len(explanation_result["sections"]),
            warning_count=len(explanation_result["warnings"]),
            audience=str(explanation_result["audience"]["name"]),
            level=str(explanation_result["level"]["name"]),
            trace_id=str(explanation_result["trace"]["trace_id"]),
            read_only_mode=True,
        )

    def _clinical_snapshot_status(self) -> ClinicalSnapshotStatusViewModel:
        execution = self._runtime.execute()
        snapshot = execution["clinical_snapshot"]
        statistics = snapshot["statistics"]
        version = snapshot["version"]
        return ClinicalSnapshotStatusViewModel(
            status="available_read_only",
            snapshot_id=str(snapshot["snapshot_id"]),
            version=f"{version['major']}.{version['minor']}.{version['patch']}",
            safety_alerts=int(statistics["safety_alerts"]),
            evidence_items=int(statistics["evidence_items"]),
            hypotheses=int(statistics["hypotheses"]),
            explanations=int(statistics["explanations"]),
            trace_id=str(snapshot["trace_id"]),
            read_only_mode=True,
        )

    def _clinical_timeline_status(self) -> ClinicalTimelineStatusViewModel:
        execution = self._runtime.execute()
        timeline = execution["clinical_timeline"]
        statistics = timeline["statistics"]
        return ClinicalTimelineStatusViewModel(
            status="available_read_only",
            timeline_id=str(timeline["timeline_id"]),
            snapshot_count=int(statistics["snapshot_count"]),
            transition_count=int(statistics["transition_count"]),
            current_snapshot=str(timeline["current_snapshot"]),
            version=str(timeline["version"]),
            trace_id=str(timeline["trace_id"]),
            read_only_mode=True,
        )

    def _clinical_navigation_status(self) -> ClinicalNavigationStatusViewModel:
        execution = self._runtime.execute()
        navigation = execution["clinical_navigation"]
        return ClinicalNavigationStatusViewModel(
            status="available_read_only",
            navigation_id=str(navigation["navigation_id"]),
            active_widget=str(navigation["active_widget"]),
            breadcrumb_count=len(navigation["breadcrumbs"]),
            history_count=len(navigation["history"]["entries"]),
            trace_id=str(navigation["trace_id"]),
            read_only_mode=True,
        )

    def _clinical_operating_mind_status(self) -> ClinicalOperatingMindStatusViewModel:
        execution = self._runtime.execute()
        operating_mind = execution["clinical_operating_mind"]
        state = operating_mind["state"]
        trace = state["trace"]
        return ClinicalOperatingMindStatusViewModel(
            status=str(state["status"]),
            mind_id=str(state["mind_id"]),
            current_phase=str(state["current_phase"]),
            completed_phase_count=len(state["completed_phases"]),
            contract_count=len(state["contracts"]),
            audit_count=len(state["audit"]),
            trace_complete=bool(
                trace["runtime_trace"]
                and trace["safety_trace"]
                and trace["evidence_trace"]
                and trace["optimization_trace"]
                and trace["explanation_trace"]
                and trace["snapshot_id"]
                and trace["timeline_id"]
                and trace["navigation_session"]
            ),
            trace_id=str(trace["trace_id"]),
            read_only_mode=True,
        )

    def _clinical_quality_status(self) -> ClinicalQualityStatusViewModel:
        execution = self._runtime.execute()
        quality = execution["clinical_quality"]
        decision = quality["publication_decision"]
        return ClinicalQualityStatusViewModel(
            status=str(quality["status"]),
            quality_id=str(quality["quality_id"]),
            quality_score=float(quality["quality_score"]),
            publication_outcome=str(decision["outcome"]),
            publish_allowed=bool(decision["publish_allowed"]),
            blocking_issue_count=len(quality["blocking_issues"]),
            warning_count=len(quality["warnings"]),
            trace_id=str(quality["trace_id"]),
            read_only_mode=True,
        )

    def _clinical_research_status(self) -> ClinicalResearchStatusViewModel:
        result = self._research_coordinator.run_structural_experiment()
        return ClinicalResearchStatusViewModel(
            status="available_read_only",
            research_id=result.research_id,
            experiment_id=result.experiment_id,
            metrics_average=result.metrics.average(),
            benchmark_count=len(result.benchmark_results),
            validation_count=len(result.validation_results),
            promotion_state=result.promotion_decision.state,
            runtime_connected=False,
            trace_id=result.trace_id,
            read_only_mode=True,
        )

    def _scientific_validation_status(self) -> ScientificValidationStatusViewModel:
        result = self._scientific_validation.validate_candidate()
        return ScientificValidationStatusViewModel(
            status="available_read_only",
            validation_id=result.validation_id,
            knowledge_candidate=result.knowledge_candidate,
            source_count=len(result.scientific_sources),
            quality_status=result.quality_assessment.status,
            editorial_state=result.editorial_review.state,
            publication_outcome=result.publication_decision.outcome,
            knowledge_version=result.knowledge_version,
            runtime_connected=False,
            trace_id=result.trace_id,
            read_only_mode=True,
        )

    def _knowledge_governance_status(self) -> KnowledgeGovernanceStatusViewModel:
        result = self._knowledge_governance.validate_structure()
        return KnowledgeGovernanceStatusViewModel(
            status="available_read_only",
            governance_id=result.governance_id,
            ontology_version=result.ontology_version,
            entity_count=len(result.entity_registry),
            relationship_count=len(result.relationship_registry),
            taxonomy_version=result.taxonomy_version,
            dependency_issue_count=len(result.dependency_graph.issues),
            publication_decision=result.publication_decision,
            runtime_connected=False,
            trace_id=result.trace_id,
            read_only_mode=True,
        )

    def _digital_clinical_twin_status(self) -> DigitalClinicalTwinStatusViewModel:
        twin = self._digital_twin.build_twin()
        return DigitalClinicalTwinStatusViewModel(
            status="available_read_only",
            twin_id=twin.twin_id,
            timeline_reference=twin.timeline_reference,
            snapshot_count=len(twin.snapshot_history),
            transition_count=len(twin.state_transitions),
            quality_event_count=len(twin.quality_history),
            stability_item_count=len(twin.stability_profile),
            version=twin.version.value(),
            runtime_connected=False,
            trace_id=twin.trace_id,
            read_only_mode=True,
        )

    def _clinical_simulation_status(self) -> ClinicalSimulationStatusViewModel:
        result = self._clinical_simulation.simulate()
        return ClinicalSimulationStatusViewModel(
            status="available_read_only",
            simulation_id=result.simulation_id,
            sandbox_id=result.sandbox_id,
            twin_clone_id=result.twin_clone_id,
            scenario_id=result.scenario_id,
            branch_id=result.simulation_branch.branch_id,
            outcome_status=result.simulation_outcome.status,
            limitation_count=len(result.limitations),
            runtime_connected=False,
            production_mutation_allowed=False,
            trace_id=result.trace_id,
            read_only_mode=True,
        )

    def _clinical_intelligence_status(self) -> ClinicalIntelligenceStatusViewModel:
        result = self._clinical_intelligence.evaluate_capability()
        return ClinicalIntelligenceStatusViewModel(
            status="available_read_only",
            intelligence_id=result.intelligence_id,
            capability_id=result.capability.capability_id,
            capability_status=result.capability.status,
            contract_count=len(result.contracts),
            permission_count=len(result.permissions),
            governance_outcome=result.governance_decision.outcome,
            quality_validation=result.quality_validation,
            runtime_connected=False,
            autonomous_decision_allowed=False,
            trace_id=result.trace_id,
            read_only_mode=True,
        )

    def _consultation_regions(
        self, strategy_blocked_reason: str
    ) -> tuple[ConsultationRegionViewModel, ...]:
        return self._longitudinal_consultation_regions(strategy_blocked_reason)

    def _longitudinal_consultation_regions(
        self, strategy_blocked_reason: str
    ) -> tuple[ConsultationRegionViewModel, ...]:
        return (
            ConsultationRegionViewModel(
                "Paciente",
                "Como esta este paciente hoje?",
                (
                    ConsultationCardViewModel(
                        "Patient Header",
                        "Ancora a consulta no paciente sem reduzir a pessoa ao diagnostico.",
                        "ready",
                        (
                            "Paciente demo: PATIENT-001",
                            "Consulta atual: seguimento ambulatorial",
                            "Estado da coleta: parcial",
                            "Decisor final: medico",
                        ),
                        "Dados demonstrativos. Nao e prontuario e nao define diagnostico.",
                    ),
                    ConsultationCardViewModel(
                        "Motivo da consulta",
                        "Registra a demanda atual sem exigir diagnostico.",
                        "read-only",
                        (
                            "Queixa principal: registrar fala do paciente",
                            "O que mudou desde a ultima consulta?",
                            "Sofrimento atual: baixo | moderado | alto",
                            "Impacto funcional: investigar",
                        ),
                        "Motivo da consulta nao define diagnostico nem conduta.",
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Estado clinico",
                "Centraliza estabilidade, evolucao e resposta clinica antes do diagnostico.",
                (
                    ConsultationCardViewModel(
                        "Clinical Stability",
                        "Mostra o estado clinico longitudinal como centro da consulta.",
                        "ready",
                        (
                            "Estavel",
                            "Parcialmente estavel",
                            "Instavel",
                            "Recaida",
                            "Remissao",
                            "Resposta parcial",
                            "Sem resposta",
                            "Piora clinica",
                        ),
                        "Estado clinico organiza raciocinio; nao escolhe tratamento.",
                    ),
                    ConsultationCardViewModel(
                        "Resposta ao tratamento",
                        "Compara estado atual com evolucao percebida.",
                        "read-only",
                        (
                            "Melhora percebida",
                            "Sintomas persistentes",
                            "Tolerabilidade",
                            "Funcionalidade",
                            "Adesao",
                        ),
                        "Resposta percebida precisa de avaliacao medica.",
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Seguranca",
                "Riscos clinicos sempre visiveis antes de qualquer plano terapeutico.",
                (
                    ConsultationCardViewModel(
                        "Risk Panel",
                        "Lista riscos clinicos que precisam ser avaliados explicitamente.",
                        "critical",
                        (
                            "Suicidio",
                            "Agressividade",
                            "Interacoes medicamentosas",
                            "QT",
                            "Gestacao",
                            "Sedacao",
                            "Metabolico",
                        ),
                        "Seguranca clinica vem antes de estrategia. O painel nao calcula risco real.",
                    ),
                    ConsultationCardViewModel(
                        "Perguntas Agora",
                        "Perguntas criticas que nao devem ser esquecidas.",
                        "critical",
                        (
                            "Ideacao suicida?",
                            "Sintomas maniformes?",
                            "Uso de substancias?",
                            "Adesao ao tratamento?",
                            "Efeitos adversos?",
                        ),
                        "Perguntas criticas exigem avaliacao medica direta.",
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Sintomas atuais",
                "Biblioteca de sintomas presentes, ausentes e relevantes para seguimento.",
                (
                    ConsultationCardViewModel(
                        "Symptom Capture",
                        "Organiza sintomas de forma rapida para revisao durante a consulta.",
                        "read-only",
                        (
                            "Humor deprimido: leve | moderado | grave",
                            "Ansiedade: leve | moderada | grave",
                            "Insonia terminal | inicial | manutencao",
                            "Anedonia: presente | ausente",
                            "Lentificacao: presente | ausente",
                            "Ideacao suicida: negar | investigar | presente",
                        ),
                        "Captura visual nao equivale a escala validada nem diagnostico.",
                    ),
                    ConsultationCardViewModel(
                        "Sintomas ausentes",
                        "Registra o que foi negado para reduzir ambiguidade longitudinal.",
                        "read-only",
                        (
                            "Sintomas maniformes: ausente | investigar",
                            "Psicose: ausente | investigar",
                            "Uso de substancias: ausente | investigar",
                            "Risco agudo: ausente | investigar",
                        ),
                        "Ausencia de sintoma tambem deve ser confirmada clinicamente.",
                    ),
                    ConsultationCardViewModel(
                        "Sinais observados",
                        "Organiza exame do estado mental observado durante a consulta.",
                        "read-only",
                        (
                            "Hipomimia",
                            "Lentificacao psicomotora",
                            "Agitacao",
                            "Fala pressionada",
                            "Pensamento tangencial",
                        ),
                        "Sinais observados exigem interpretacao medica.",
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Contexto clinico",
                "Diagnostico vira contexto opcional, nao ponto de partida.",
                (
                    ConsultationCardViewModel(
                        "Hipotese conhecida / Em investigacao",
                        "Permite informar contexto diagnostico sem travar a consulta.",
                        "read-only",
                        (
                            "Hipotese conhecida: opcional",
                            "Em investigacao: sim | nao",
                            "Diagnostico diferencial: apenas se relevante",
                            "Nivel de incerteza: registrar, nao resolver automaticamente",
                        ),
                        "Contexto diagnostico nao fecha diagnostico e nao prescreve.",
                    ),
                    ConsultationCardViewModel(
                        "Guided Anamnesis",
                        "Sugere perguntas objetivas a partir do estado clinico atual.",
                        "read-only",
                        (
                            "O que mudou desde a ultima consulta?",
                            "Qual sintoma mais incomoda hoje?",
                            "Houve perda de funcionalidade?",
                            "Houve evento adverso ou baixa adesao?",
                            "O paciente percebeu melhora, piora ou estabilidade?",
                        ),
                        "Perguntas apoiam a entrevista; nao fazem diagnostico automatico.",
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Plano terapeutico",
                "Organiza mudancas planejadas sem transformar o sistema em prescritor.",
                (
                    ConsultationCardViewModel(
                        "Conduta planejada",
                        "Registra familias de plano discutidas pelo medico.",
                        "locked",
                        (
                            "Manter tratamento",
                            "Ajustar tratamento",
                            "Introduzir tratamento",
                            "Retirar medicamento",
                            "Associar medicamento",
                            "Solicitar investigacao adicional",
                            "Sem alteracao",
                        ),
                        strategy_blocked_reason,
                    ),
                    ConsultationCardViewModel(
                        "Strategy Panel",
                        "Compatibilidade: area futura de estrategias comparaveis.",
                        "locked",
                        (
                            "Manter",
                            "Ajustar dose",
                            "Substituir",
                            "Associar",
                            "Retirar gradualmente",
                            "Monitorar antes de alterar",
                        ),
                        "Nao prescreve, nao escolhe medicamento e nao ranqueia conduta.",
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Tratamento atual",
                "Tratamento em uso como contexto longitudinal, separado de qualquer plano futuro.",
                (
                    ConsultationCardViewModel(
                        "Current Medication",
                        "Mostra tratamento atual como contexto de consulta.",
                        "ready",
                        (
                            "Esta usando medicamento? sim | nao",
                            "Medicamento: confirmar com o paciente",
                            "Dose: registrar, nao sugerir",
                            "Tempo de uso",
                            "Adesao",
                            "Eventos adversos",
                            "Resposta percebida",
                        ),
                        "Nao sugere iniciar, suspender, ajustar ou trocar medicamento.",
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Objetivos",
                "Define o que a consulta tenta melhorar, antes de qualquer mudanca planejada.",
                (
                    ConsultationCardViewModel(
                        "Objetivos Terapeuticos",
                        "Objetivo da consulta definido com o paciente.",
                        "read-only",
                        (
                            "Melhorar ansiedade",
                            "Reduzir ansiedade",
                            "Melhorar humor",
                            "Melhorar sono",
                            "Dormir melhor",
                            "Reduzir efeitos adversos",
                            "Melhorar adesao",
                            "Rever medicacao",
                        ),
                        "Objetivos nao sao recomendacoes de tratamento.",
                    ),
                    ConsultationCardViewModel(
                        "Lacunas clinicas",
                        "Mostra informacoes ausentes antes de qualquer plano.",
                        "warning",
                        (
                            "Alergias e reacoes graves previas",
                            "Comorbidades renais, hepaticas e cardiovasculares",
                            "QT prolongado, epilepsia, gestacao ou lactacao",
                            "Medicacoes concomitantes e interacoes",
                        ),
                        "Lacunas nao bloqueiam o medico; apenas organizam o raciocinio.",
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Monitorizacao e retorno",
                "Organiza acompanhamento longitudinal, estabilidade e proxima revisao.",
                (
                    ConsultationCardViewModel(
                        "Monitoring Timeline",
                        "Mostra o que acompanhar ate o retorno.",
                        "read-only",
                        (
                            "Humor",
                            "Ansiedade",
                            "Sono",
                            "Peso",
                            "Libido",
                            "Adesao",
                            "Funcionalidade",
                        ),
                        "Monitorizacao organiza seguimento; nao cria ordem clinica.",
                    ),
                    ConsultationCardViewModel(
                        "Retorno",
                        "Organiza janela de retorno como informacao de acompanhamento.",
                        "read-only",
                        (
                            "2 semanas",
                            "4 semanas",
                            "6 semanas",
                            "3 meses",
                        ),
                        "Intervalo real depende do medico e do contexto clinico.",
                    ),
                    ConsultationCardViewModel(
                        "Patient Friendly Mode",
                        "Resumo que pode ser mostrado ao paciente sem linguagem tecnica excessiva.",
                        "ready",
                        (
                            "Queremos entender como voce esta hoje.",
                            "Vamos observar o que mudou desde a ultima consulta.",
                            "O plano deve ser decidido junto com seu medico.",
                            "O acompanhamento observa sintomas, resposta e tolerabilidade.",
                        ),
                        "Nao orienta automedicacao e nao substitui explicacao medica.",
                    ),
                    ConsultationCardViewModel(
                        "Evidence Summary",
                        "Espaco futuro para mostrar fontes em linguagem acessivel.",
                        "planned",
                        (
                            "Fonte cientifica: pendente",
                            "Qualidade da evidencia: pendente",
                            "Aplicabilidade ao caso: exige revisao medica",
                        ),
                        "Nenhuma informacao clinica deve aparecer sem fonte rastreavel.",
                    ),
                ),
            ),
        )

    def _legacy_consultation_regions(
        self, strategy_blocked_reason: str
    ) -> tuple[ConsultationRegionViewModel, ...]:
        return (
            ConsultationRegionViewModel(
                "Paciente",
                "Identifica o paciente, situa a consulta e mantem a pessoa no centro.",
                (
                    ConsultationCardViewModel(
                        "Patient Header",
                        "Ancora a consulta no paciente sem reduzir a pessoa ao diagnostico.",
                        "ready",
                        (
                            "Paciente demo: PATIENT-001",
                            "Consulta atual: seguimento ambulatorial",
                            "Estado da coleta: parcial",
                            "Decisor final: medico",
                        ),
                        "Dados demonstrativos. Nao e prontuario e nao define diagnostico.",
                    ),
                    ConsultationCardViewModel(
                        "Clinical Snapshot",
                        "Resumo dinamico do que ja foi organizado na consulta.",
                        "read-only",
                        (
                            "Sintomas atuais: humor, ansiedade, sono e funcionalidade",
                            "Hipoteses: em avaliacao medica",
                            "Objetivos: reduzir sofrimento e melhorar funcionamento",
                            "Incertezas: seguranca, adesao e efeitos adversos",
                        ),
                        "Snapshot nao fecha diagnostico nem prescreve.",
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Perguntas Agora",
                "Painel lateral com poucas perguntas de alta relevancia para o momento atual.",
                (
                    ConsultationCardViewModel(
                        "Live Question Panel",
                        "Mostra perguntas criticas que nao devem ser esquecidas.",
                        "critical",
                        (
                            "Ideacao suicida?",
                            "Sintomas maniformes?",
                            "Uso de substancias?",
                            "Adesao ao tratamento?",
                            "Efeitos adversos?",
                        ),
                        "Perguntas criticas exigem avaliacao medica direta.",
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Riscos",
                "Mantem a seguranca sempre visivel antes de qualquer planejamento terapeutico.",
                (
                    ConsultationCardViewModel(
                        "Risk Panel",
                        "Lista riscos clinicos que precisam ser avaliados explicitamente.",
                        "critical",
                        (
                            "Suicidio",
                            "Agressividade",
                            "Interacoes medicamentosas",
                            "QT",
                            "Gestacao",
                            "Sedacao",
                            "Metabolico",
                        ),
                        "Seguranca clinica vem antes de estrategia. O painel nao calcula risco real.",
                    ),
                    ConsultationCardViewModel(
                        "Safety First Gate",
                        "Mostra o estado conceitual do gate de seguranca.",
                        "read-only",
                        (
                            "Riscos criticos: investigar",
                            "Interacoes: verificar",
                            "Contraindicacoes: revisar",
                            "Encaminhamento: decisao medica",
                        ),
                        "Nenhum gate visual autoriza conduta.",
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Sintomas",
                "Captura rapida dos sintomas relevantes e sua intensidade observacional.",
                (
                    ConsultationCardViewModel(
                        "Symptom Capture",
                        "Organiza sintomas de forma rapida para revisao durante a consulta.",
                        "read-only",
                        (
                            "Humor deprimido: leve | moderado | grave",
                            "Ansiedade: leve | moderada | grave",
                            "Insônia: inicio | manutencao | terminal",
                            "Anedonia: presente | ausente",
                            "Ideacao suicida: negar | investigar | presente",
                        ),
                        "Captura visual nao equivale a escala validada nem diagnostico.",
                    ),
                    ConsultationCardViewModel(
                        "Funcionalidade e Qualidade de Vida",
                        "Mantem sintomas ligados ao funcionamento real do paciente.",
                        "read-only",
                        (
                            "Trabalho ou estudo",
                            "Autocuidado",
                            "Sono e energia",
                            "Relacionamentos",
                            "Atividades significativas",
                        ),
                        "O objetivo final e estabilidade clinica, nao apenas reduzir sintomas isolados.",
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Anamnese Guiada",
                "Transforma a fala do paciente em perguntas objetivas para o medico conduzir.",
                (
                    ConsultationCardViewModel(
                        "Guided Anamnesis",
                        "Sugere perguntas curtas, de alta relevancia, sem responder pelo medico.",
                        "read-only",
                        (
                            "Insonia: ha quanto tempo?",
                            "Sono: dificuldade para iniciar, manter ou acordar cedo?",
                            "Ansiedade: piora a noite?",
                            "Substancias: alcool, cafeina ou estimulantes?",
                            "Tratamento: adesao e efeitos adversos?",
                        ),
                        "Perguntas apoiam a entrevista; nao fazem diagnostico automatico.",
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Estrategias",
                "Organiza alternativas conceituais sem escolher, ranquear ou prescrever.",
                (
                    ConsultationCardViewModel(
                        "Strategy Panel",
                        "Mostra familias de estrategia que o medico pode considerar fora do modo automatico.",
                        "locked",
                        (
                            "Manter",
                            "Ajustar dose",
                            "Substituir",
                            "Associar",
                            "Retirar gradualmente",
                            "Monitorar antes de alterar",
                        ),
                        strategy_blocked_reason,
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Tratamento atual",
                "Mostra o tratamento em uso como contexto, separado de estrategia futura.",
                (
                    ConsultationCardViewModel(
                        "Current Medication",
                        "Mostra tratamento atual como contexto de consulta.",
                        "ready",
                        (
                            "Medicacoes atuais: confirmar com o paciente",
                            "Adesao: revisar durante a consulta",
                            "Efeitos adversos: investigar ativamente",
                            "Mudancas recentes: pendente",
                        ),
                        "Nao sugere iniciar, suspender, ajustar ou trocar medicamento.",
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Lacunas clinicas",
                "Mostra informacoes ausentes antes de qualquer estrategia.",
                (
                    ConsultationCardViewModel(
                        "Missing Information Widget",
                        "Lista pontos que ainda precisam ser esclarecidos pelo medico.",
                        "warning",
                        (
                            "Alergias e reacoes graves previas",
                            "Comorbidades renais, hepaticas e cardiovasculares",
                            "QT prolongado, epilepsia, gestacao ou lactacao",
                            "Medicacoes concomitantes e interacoes",
                        ),
                        "Lacunas nao bloqueiam o medico; apenas organizam o raciocinio.",
                    ),
                ),
            ),
            ConsultationRegionViewModel(
                "Monitorizacao",
                "Organiza o acompanhamento longitudinal de forma visual e silenciosa.",
                (
                    ConsultationCardViewModel(
                        "Objetivos Terapeuticos",
                        "Mantem claro o que a consulta esta tentando melhorar.",
                        "read-only",
                        (
                            "Melhorar sono",
                            "Reduzir ansiedade",
                            "Melhorar energia",
                            "Diminuir efeitos colaterais",
                            "Acompanhar resposta",
                        ),
                        "Objetivos nao sao recomendacoes de tratamento.",
                    ),
                    ConsultationCardViewModel(
                        "Monitoring Timeline",
                        "Mostra os marcos de acompanhamento que precisam ser planejados pelo medico.",
                        "read-only",
                        (
                            "Hoje",
                            "2 semanas",
                            "6 semanas",
                            "3 meses",
                            "Sintomas, funcionalidade, adesao e efeitos adversos",
                            "Seguranca e tolerabilidade",
                        ),
                        "Plano real depende do Clinical Kernel. Nao recomenda exame especifico nem intervalo obrigatorio.",
                    ),
                    ConsultationCardViewModel(
                        "Clinical Timeline",
                        "Liga consulta atual, resposta, remissao, recaida, recorrencia e estabilidade.",
                        "read-only",
                        (
                            "Consulta atual",
                            "Resposta parcial",
                            "Remissao",
                            "Recaida",
                            "Recorrencia",
                            "Estabilidade sustentada",
                        ),
                        "Timeline nao e prontuario oficial e nao classifica resposta automaticamente.",
                    ),
                    ConsultationCardViewModel(
                        "Patient Friendly Mode",
                        "Resumo que pode ser mostrado ao paciente sem linguagem tecnica excessiva.",
                        "ready",
                        (
                            "Queremos entender melhor seu sono, ansiedade e energia.",
                            "Vamos revisar seguranca, efeitos colaterais e adesao.",
                            "O plano deve ser decidido junto com seu medico.",
                            "O acompanhamento observa resposta e tolerabilidade ao longo do tempo.",
                        ),
                        "Nao orienta automedicacao e nao substitui explicacao medica.",
                    ),
                    ConsultationCardViewModel(
                        "Evidence Summary",
                        "Espaco futuro para mostrar fontes em linguagem acessivel.",
                        "planned",
                        (
                            "Fonte cientifica: pendente",
                            "Qualidade da evidencia: pendente",
                            "Aplicabilidade ao caso: exige revisao medica",
                        ),
                        "Nenhuma informacao clinica deve aparecer sem fonte rastreavel.",
                    ),
                ),
            ),
        )
