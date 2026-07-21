"""Contract between PsychRx UI and the specialized clinical GPT.

This module defines structured payloads only. It does not implement clinical
reasoning, medication selection, prescribing, or dose recommendation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


DecisionAction = Literal[
    "maintain",
    "optimize_current",
    "increase_dose",
    "decrease_dose",
    "substitute",
    "associate",
    "taper_or_withdraw",
    "select_candidate",
    "investigate_before_change",
    "insufficient_information",
]


@dataclass(frozen=True)
class CurrentMedicationPayload:
    """Medication already reported by the physician during the visit."""

    name: str
    indication: str = ""
    formulation: str = ""
    route: str = ""
    dose_value: str = ""
    dose_prescribed: str = ""
    dose_used: str = ""
    dose_unit: str = ""
    frequency: str = ""
    schedule: str = ""
    start_date: str = ""
    last_dose_change_date: str = ""
    duration: str = ""
    duration_current_dose: str = ""
    adherence: str = ""
    perceived_benefit: str = ""
    response: str = ""
    adverse_effects: str = ""
    tolerability: str = ""
    reason_for_use: str = ""


@dataclass(frozen=True)
class ClinicalSafetyPayload:
    """Safety state collected before any strategy is discussed."""

    suicide: str = "not_assessed"
    suicide_plan: str = "not_assessed"
    suicide_intent: str = "not_assessed"
    suicide_means_access: str = "not_assessed"
    suicide_recent_attempt: str = "not_assessed"
    aggression: str = "not_assessed"
    mania_or_hypomania: str = "not_assessed"
    substances: str = "not_assessed"
    adherence: str = "not_assessed"
    adverse_effects: str = "not_assessed"
    interactions: str = "not_assessed"
    qt_risk: str = "not_assessed"
    pregnancy_or_lactation: str = "not_assessed"
    metabolic_risk: str = "not_assessed"
    delirium: str = "not_assessed"
    intoxication: str = "not_assessed"
    withdrawal: str = "not_assessed"
    allergies: str = "not_assessed"
    severe_adverse_reaction: str = "not_assessed"
    acute_toxicity: str = "not_assessed"
    toxidrome_signals: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ClinicalDecisionSupportRequest:
    """Input sent from the app to the specialized GPT."""

    patient_label: str = ""
    birth_date: str = ""
    pregnancy_status: str = "not_assessed"
    lactation_status: str = "not_assessed"
    postpartum_status: str = "not_assessed"
    sex_context: str = "not_informed"
    weight_kg: str = ""
    renal_status: str = "not_assessed"
    hepatic_status: str = "not_assessed"
    diagnostic_context: str = ""
    current_state: str = ""
    symptoms: tuple[str, ...] = field(default_factory=tuple)
    observed_signs: tuple[str, ...] = field(default_factory=tuple)
    impairment_domains: tuple[str, ...] = field(default_factory=tuple)
    impairment_severity: str = ""
    stability: str = ""
    comorbidities: tuple[str, ...] = field(default_factory=tuple)
    clinical_axes: tuple[str, ...] = field(default_factory=tuple)
    clinical_context_ids: tuple[str, ...] = field(default_factory=tuple)
    current_medications: tuple[CurrentMedicationPayload, ...] = field(
        default_factory=tuple
    )
    safety: ClinicalSafetyPayload = field(default_factory=ClinicalSafetyPayload)
    clinician_question: str = (
        "What decision-support advice is supported by the current clinical "
        "state, safety screening, medication history, and traceable evidence?"
    )

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-safe representation for transport to a GPT."""
        return asdict(self)


@dataclass(frozen=True)
class EvidenceCitationPayload:
    """Traceable scientific source used by a decision-support item."""

    source_id: str
    title: str
    organization: str = ""
    year: str = ""
    section: str = ""
    excerpt_anchor: str = ""
    evidence_type: str = ""
    quality: str = ""
    applicability: str = ""
    limitations: str = ""

    def is_traceable(self) -> bool:
        """Return whether the citation points to a concrete source location."""
        return bool(self.source_id and self.title and self.section)


@dataclass(frozen=True)
class ActionEvidencePayload:
    """Evidence attached to one proposed action."""

    action: DecisionAction
    rationale: str
    citations: tuple[EvidenceCitationPayload, ...] = field(default_factory=tuple)
    unresolved_reason: str = ""

    def has_evidence_or_unresolved_reason(self) -> bool:
        """Require either traceable evidence or an explicit unresolved marker."""
        return any(citation.is_traceable() for citation in self.citations) or bool(
            self.unresolved_reason
        )


@dataclass(frozen=True)
class MedicationActionExplanationPayload:
    """Five physician-facing answers for one medication already in use."""

    medication_name: str
    maintain_reason: str
    increase_reason: str
    substitute_reason: str
    associate_reason: str
    evidence_level: str
    substitution_candidate: MedicationOptionPayload | None = None

    def is_complete(self) -> bool:
        """Return whether every requested explanation is explicit."""
        return bool(
            self.medication_name
            and self.maintain_reason
            and self.increase_reason
            and self.substitute_reason
            and self.associate_reason
            and self.evidence_level
        )


@dataclass(frozen=True)
class PharmacologicalTargetPayload:
    """Target that links impairment to the pharmacological rationale."""

    impairment_domain: str
    symptom_target: str
    pharmacological_target: str
    therapeutic_dose_target: str = ""
    dose_source: EvidenceCitationPayload | None = None
    dose_dependent_profile: str = ""
    dose_profile_source: EvidenceCitationPayload | None = None
    unresolved_reason: str = ""

    def has_dose_traceability_or_unresolved_reason(self) -> bool:
        """Dose target must be sourced or explicitly unresolved."""
        return bool(
            self.unresolved_reason
            or (self.dose_source and self.dose_source.is_traceable())
        )


@dataclass(frozen=True)
class MedicationOptionPayload:
    """Candidate class or medication proposed by the specialized GPT."""

    name: str
    role: Literal[
        "current",
        "initiation_candidate",
        "substitution_candidate",
        "association_candidate",
    ]
    reason: str
    drug_class: str = ""
    pharmacological_target: str = ""
    dose_guidance: str = ""
    evidence: tuple[EvidenceCitationPayload, ...] = field(default_factory=tuple)
    safety_notes: tuple[str, ...] = field(default_factory=tuple)
    unresolved_reason: str = ""

    def has_evidence_or_unresolved_reason(self) -> bool:
        """Medication candidates must be traceable or explicitly unresolved."""
        return any(citation.is_traceable() for citation in self.evidence) or bool(
            self.unresolved_reason
        )


@dataclass(frozen=True)
class ClinicalDecisionSupportResponse:
    """Output returned by the specialized GPT to the PsychRx app."""

    summary: str
    recommended_action: DecisionAction
    clinical_rationale: tuple[str, ...] = field(default_factory=tuple)
    impairment_targets: tuple[str, ...] = field(default_factory=tuple)
    pharmacological_targets: tuple[PharmacologicalTargetPayload, ...] = field(
        default_factory=tuple
    )
    substitution_options: tuple[MedicationOptionPayload, ...] = field(
        default_factory=tuple
    )
    association_options: tuple[MedicationOptionPayload, ...] = field(
        default_factory=tuple
    )
    action_evidence: tuple[ActionEvidencePayload, ...] = field(default_factory=tuple)
    medication_action_explanations: tuple[
        MedicationActionExplanationPayload, ...
    ] = field(default_factory=tuple)
    rejected_alternatives: tuple[str, ...] = field(default_factory=tuple)
    safety_warnings: tuple[str, ...] = field(default_factory=tuple)
    monitoring_targets: tuple[str, ...] = field(default_factory=tuple)
    monitoring_governance_summary: tuple[str, ...] = field(default_factory=tuple)
    population_evidence_summary: tuple[str, ...] = field(default_factory=tuple)
    disease_use_summary: tuple[str, ...] = field(default_factory=tuple)
    interaction_summary: tuple[str, ...] = field(default_factory=tuple)
    phenotype_summary: tuple[str, ...] = field(default_factory=tuple)
    clinical_context_summary: tuple[str, ...] = field(default_factory=tuple)
    coverage_summary: tuple[str, ...] = field(default_factory=tuple)
    evidence_governance_summary: tuple[str, ...] = field(default_factory=tuple)
    scientific_readiness: str = "not_assessed"
    eligibility_summary: tuple[str, ...] = field(default_factory=tuple)
    excluded_medications: tuple[str, ...] = field(default_factory=tuple)
    strategy_code: str = ""
    confidence: str = "not_calculated"
    status: Literal["ready_for_clinician_review", "blocked", "unresolved"] = (
        "unresolved"
    )
    prescription_boundary: str = (
        "Suporte a decisao medica. O medico permanece responsavel pela "
        "prescricao final, escolha do medicamento, dose e conduta clinica."
    )

    def validate_for_display(self) -> tuple[str, ...]:
        """Return structural issues that prevent safe display in the app."""
        issues: list[str] = []
        if not self.summary:
            issues.append("summary_missing")
        if not self.clinical_rationale:
            issues.append("clinical_rationale_missing")
        if not self.action_evidence:
            issues.append("action_evidence_missing")
        for item in self.action_evidence:
            if not item.has_evidence_or_unresolved_reason():
                issues.append(f"action_evidence_untraceable:{item.action}")
        for item in self.medication_action_explanations:
            if not item.is_complete():
                issues.append(
                    f"medication_action_explanation_incomplete:{item.medication_name}"
                )
            if (
                item.substitution_candidate
                and not item.substitution_candidate.has_evidence_or_unresolved_reason()
            ):
                issues.append(
                    f"medication_action_candidate_untraceable:{item.medication_name}"
                )
        for target in self.pharmacological_targets:
            if not target.has_dose_traceability_or_unresolved_reason():
                issues.append(
                    f"pharmacological_target_untraceable:{target.impairment_domain}"
                )
        for option in self.substitution_options + self.association_options:
            if not option.has_evidence_or_unresolved_reason():
                issues.append(f"medication_option_untraceable:{option.name}")
        return tuple(issues)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-safe representation for the app UI."""
        return asdict(self)


def empty_decision_support_response() -> ClinicalDecisionSupportResponse:
    """Return a safe unresolved response until the specialized GPT answers."""
    return ClinicalDecisionSupportResponse(
        summary="Aguardando resposta do GPT especializado.",
        recommended_action="insufficient_information",
        clinical_rationale=(
            "O app ainda nao recebeu conselho estruturado com evidencia rastreavel.",
        ),
        action_evidence=(
            ActionEvidencePayload(
                action="insufficient_information",
                rationale="Nenhuma acao pode ser exibida sem fonte ou pendencia explicita.",
                unresolved_reason="specialized_gpt_response_missing",
            ),
        ),
        status="unresolved",
    )
