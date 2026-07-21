"""Read-only ViewModel for the local PsychRx app shell."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class AppStatusViewModel:
    """High-level status exposed to the interface."""

    product_name: str = "PsychRx"
    mode: str = "Clinical Reasoning Support"
    safety_status: str = "READ ONLY - NO PRESCRIPTION"
    current_phase: str = "Clinical Kernel Integration / A04 SNRIs blocked: source corpus required"
    version: str = "1.1-scientific-progress"


@dataclass(frozen=True)
class SafetyGuardrailViewModel:
    """Clinical safety limits that must stay visible in the UI."""

    title: str
    description: str
    severity: str = "mandatory"


@dataclass(frozen=True)
class WorkflowStepViewModel:
    """Conceptual clinical workflow step."""

    order: int
    name: str
    purpose: str
    status: str = "conceptual"


@dataclass(frozen=True)
class DashboardPanelViewModel:
    """Conceptual dashboard panel."""

    name: str
    responsibility: str
    forbidden_behavior: str


@dataclass(frozen=True)
class RoadmapTrackViewModel:
    """Enterprise roadmap track."""

    name: str
    focus: str


@dataclass(frozen=True)
class ClinicalExperienceComponentViewModel:
    """Official component of the Clinical Experience Layer."""

    name: str
    role: str
    safety_limit: str


@dataclass(frozen=True)
class ConsultationCardViewModel:
    """Read-only card shown in the consultation MVP surface."""

    title: str
    purpose: str
    status: str
    items: tuple[str, ...] = field(default_factory=tuple)
    safety_note: str = ""


@dataclass(frozen=True)
class ConsultationRegionViewModel:
    """Region of the consultation MVP layout."""

    name: str
    purpose: str
    cards: tuple[ConsultationCardViewModel, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class KernelStatusViewModel:
    """Read-only structural kernel metadata for the workspace."""

    kernel_status: str = "unavailable"
    pipeline_status: str = "not_started"
    strategy_blocked_reason: str = ""
    future_integrations: tuple[str, ...] = field(default_factory=tuple)
    read_only_mode: bool = True


@dataclass(frozen=True)
class RuntimeStatusViewModel:
    """Read-only Clinical Runtime metadata for the workspace."""

    runtime_status: str = "not_available"
    session_status: str = "not_started"
    pipeline_status: str = "not_started"
    event_bus_status: str = "not_started"
    audit_status: str = "not_started"
    trace_status: str = "not_started"
    read_only_mode: bool = True


@dataclass(frozen=True)
class SafetyEngineStatusViewModel:
    """Read-only Safety Engine metadata for the workspace."""

    engine_status: str = "not_available"
    snapshot_status: str = "not_evaluated"
    blocking_status: str = "not_evaluated"
    alert_count: int = 0
    blocking_count: int = 0
    trace_id: str = ""
    read_only_mode: bool = True


@dataclass(frozen=True)
class EvidenceRuntimeStatusViewModel:
    """Read-only Evidence Runtime metadata for the workspace."""

    runtime_status: str = "not_available"
    selected_count: int = 0
    discarded_count: int = 0
    citation_count: int = 0
    version_policy: str = "latest"
    trace_id: str = ""
    read_only_mode: bool = True


@dataclass(frozen=True)
class TherapeuticOptimizationStatusViewModel:
    """Read-only Therapeutic Optimization Engine metadata."""

    engine_status: str = "not_available"
    candidate_count: int = 0
    evaluated_count: int = 0
    hypothesis_count: int = 0
    uncertainty_count: int = 0
    confidence: float = 0.0
    trace_id: str = ""
    read_only_mode: bool = True


@dataclass(frozen=True)
class ClinicalExplanationStatusViewModel:
    """Read-only Clinical Explanation Engine metadata."""

    engine_status: str = "not_available"
    section_count: int = 0
    warning_count: int = 0
    audience: str = "clinician"
    level: str = "summary"
    trace_id: str = ""
    read_only_mode: bool = True


@dataclass(frozen=True)
class ClinicalSnapshotStatusViewModel:
    """Read-only Clinical Snapshot Engine metadata."""

    status: str = "not_available"
    snapshot_id: str = ""
    version: str = ""
    safety_alerts: int = 0
    evidence_items: int = 0
    hypotheses: int = 0
    explanations: int = 0
    trace_id: str = ""
    read_only_mode: bool = True


@dataclass(frozen=True)
class ClinicalTimelineStatusViewModel:
    """Read-only Clinical Timeline Engine metadata."""

    status: str = "not_available"
    timeline_id: str = ""
    snapshot_count: int = 0
    transition_count: int = 0
    current_snapshot: str = ""
    version: str = ""
    trace_id: str = ""
    read_only_mode: bool = True


@dataclass(frozen=True)
class ClinicalNavigationStatusViewModel:
    """Read-only Clinical Navigation Engine metadata."""

    status: str = "not_available"
    navigation_id: str = ""
    active_widget: str = ""
    breadcrumb_count: int = 0
    history_count: int = 0
    trace_id: str = ""
    read_only_mode: bool = True


@dataclass(frozen=True)
class ClinicalOperatingMindStatusViewModel:
    """Read-only Clinical Operating Mind metadata."""

    status: str = "not_available"
    mind_id: str = ""
    current_phase: str = ""
    completed_phase_count: int = 0
    contract_count: int = 0
    audit_count: int = 0
    trace_complete: bool = False
    trace_id: str = ""
    read_only_mode: bool = True


@dataclass(frozen=True)
class ClinicalQualityStatusViewModel:
    """Read-only Clinical Quality Engine metadata."""

    status: str = "not_available"
    quality_id: str = ""
    quality_score: float = 0.0
    publication_outcome: str = ""
    publish_allowed: bool = False
    blocking_issue_count: int = 0
    warning_count: int = 0
    trace_id: str = ""
    read_only_mode: bool = True


@dataclass(frozen=True)
class ClinicalResearchStatusViewModel:
    """Read-only Clinical Research Platform metadata."""

    status: str = "not_available"
    research_id: str = ""
    experiment_id: str = ""
    metrics_average: float = 0.0
    benchmark_count: int = 0
    validation_count: int = 0
    promotion_state: str = ""
    runtime_connected: bool = False
    trace_id: str = ""
    read_only_mode: bool = True


@dataclass(frozen=True)
class ScientificValidationStatusViewModel:
    """Read-only Scientific Validation Framework metadata."""

    status: str = "not_available"
    validation_id: str = ""
    knowledge_candidate: str = ""
    source_count: int = 0
    quality_status: str = ""
    editorial_state: str = ""
    publication_outcome: str = ""
    knowledge_version: str = ""
    runtime_connected: bool = False
    trace_id: str = ""
    read_only_mode: bool = True


@dataclass(frozen=True)
class KnowledgeGovernanceStatusViewModel:
    """Read-only Knowledge Governance Platform metadata."""

    status: str = "not_available"
    governance_id: str = ""
    ontology_version: str = ""
    entity_count: int = 0
    relationship_count: int = 0
    taxonomy_version: str = ""
    dependency_issue_count: int = 0
    publication_decision: str = ""
    runtime_connected: bool = False
    trace_id: str = ""
    read_only_mode: bool = True


@dataclass(frozen=True)
class DigitalClinicalTwinStatusViewModel:
    """Read-only Digital Clinical Twin Platform metadata."""

    status: str = "not_available"
    twin_id: str = ""
    timeline_reference: str = ""
    snapshot_count: int = 0
    transition_count: int = 0
    quality_event_count: int = 0
    stability_item_count: int = 0
    version: str = ""
    runtime_connected: bool = False
    trace_id: str = ""
    read_only_mode: bool = True


@dataclass(frozen=True)
class ClinicalSimulationStatusViewModel:
    """Read-only Clinical Simulation Platform metadata."""

    status: str = "not_available"
    simulation_id: str = ""
    sandbox_id: str = ""
    twin_clone_id: str = ""
    scenario_id: str = ""
    branch_id: str = ""
    outcome_status: str = ""
    limitation_count: int = 0
    runtime_connected: bool = False
    production_mutation_allowed: bool = False
    trace_id: str = ""
    read_only_mode: bool = True


@dataclass(frozen=True)
class ClinicalIntelligenceStatusViewModel:
    """Read-only Clinical Intelligence Platform metadata."""

    status: str = "not_available"
    intelligence_id: str = ""
    capability_id: str = ""
    capability_status: str = ""
    contract_count: int = 0
    permission_count: int = 0
    governance_outcome: str = ""
    quality_validation: str = ""
    runtime_connected: bool = False
    autonomous_decision_allowed: bool = False
    trace_id: str = ""
    read_only_mode: bool = True


@dataclass(frozen=True)
class PsychRxAppViewModel:
    """Single contract consumed by the local app interface."""

    status: AppStatusViewModel = field(default_factory=AppStatusViewModel)
    safety_guardrails: tuple[SafetyGuardrailViewModel, ...] = field(
        default_factory=tuple
    )
    clinical_workflow: tuple[WorkflowStepViewModel, ...] = field(
        default_factory=tuple
    )
    dashboard_panels: tuple[DashboardPanelViewModel, ...] = field(
        default_factory=tuple
    )
    roadmap_tracks: tuple[RoadmapTrackViewModel, ...] = field(default_factory=tuple)
    clinical_experience_components: tuple[
        ClinicalExperienceComponentViewModel, ...
    ] = field(default_factory=tuple)
    consultation_regions: tuple[ConsultationRegionViewModel, ...] = field(
        default_factory=tuple
    )
    kernel_status: KernelStatusViewModel = field(default_factory=KernelStatusViewModel)
    runtime_status: RuntimeStatusViewModel = field(default_factory=RuntimeStatusViewModel)
    safety_engine_status: SafetyEngineStatusViewModel = field(
        default_factory=SafetyEngineStatusViewModel
    )
    evidence_runtime_status: EvidenceRuntimeStatusViewModel = field(
        default_factory=EvidenceRuntimeStatusViewModel
    )
    therapeutic_optimization_status: TherapeuticOptimizationStatusViewModel = field(
        default_factory=TherapeuticOptimizationStatusViewModel
    )
    clinical_explanation_status: ClinicalExplanationStatusViewModel = field(
        default_factory=ClinicalExplanationStatusViewModel
    )
    clinical_snapshot_status: ClinicalSnapshotStatusViewModel = field(
        default_factory=ClinicalSnapshotStatusViewModel
    )
    clinical_timeline_status: ClinicalTimelineStatusViewModel = field(
        default_factory=ClinicalTimelineStatusViewModel
    )
    clinical_navigation_status: ClinicalNavigationStatusViewModel = field(
        default_factory=ClinicalNavigationStatusViewModel
    )
    clinical_operating_mind_status: ClinicalOperatingMindStatusViewModel = field(
        default_factory=ClinicalOperatingMindStatusViewModel
    )
    clinical_quality_status: ClinicalQualityStatusViewModel = field(
        default_factory=ClinicalQualityStatusViewModel
    )
    clinical_research_status: ClinicalResearchStatusViewModel = field(
        default_factory=ClinicalResearchStatusViewModel
    )
    scientific_validation_status: ScientificValidationStatusViewModel = field(
        default_factory=ScientificValidationStatusViewModel
    )
    knowledge_governance_status: KnowledgeGovernanceStatusViewModel = field(
        default_factory=KnowledgeGovernanceStatusViewModel
    )
    digital_clinical_twin_status: DigitalClinicalTwinStatusViewModel = field(
        default_factory=DigitalClinicalTwinStatusViewModel
    )
    clinical_simulation_status: ClinicalSimulationStatusViewModel = field(
        default_factory=ClinicalSimulationStatusViewModel
    )
    clinical_intelligence_status: ClinicalIntelligenceStatusViewModel = field(
        default_factory=ClinicalIntelligenceStatusViewModel
    )
    technical_registry: tuple[str, ...] = field(default_factory=tuple)
    clinical_disclaimer: str = (
        "PsychRx apoia raciocinio medico em psicofarmacologia. "
        "Nao prescreve, nao substitui o medico e nao responde como ferramenta "
        "assistencial autonoma."
    )

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-safe representation."""
        return asdict(self)
