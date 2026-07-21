"""Canonical high-value clinical contexts for safe PsychRx routing.

The registry provides vocabulary and runtime boundaries only. It contains no
diagnostic criteria, patient-specific treatment selection, or emergency dosing.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ClinicalContextDefinition:
    context_id: str
    label: str
    category: str
    runtime_behavior: str
    evidence_status: str
    source_anchor: str
    clinical_boundary: str
    treatment_rule_allowed: bool = False

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class ClinicalContextAssessment:
    selected: tuple[ClinicalContextDefinition, ...]
    blocking_warnings: tuple[str, ...]
    unknown_ids: tuple[str, ...]

    def display_lines(self) -> tuple[str, ...]:
        return tuple(
            f"{item.label} [{item.evidence_status}; {item.runtime_behavior}]"
            for item in self.selected
        )


def _context(
    context_id: str,
    label: str,
    category: str,
    runtime_behavior: str,
    evidence_status: str,
    source_anchor: str,
    boundary: str,
) -> ClinicalContextDefinition:
    return ClinicalContextDefinition(
        context_id=context_id,
        label=label,
        category=category,
        runtime_behavior=runtime_behavior,
        evidence_status=evidence_status,
        source_anchor=source_anchor,
        clinical_boundary=boundary,
    )


CLINICAL_CONTEXTS = (
    _context("AGGRESSION_RISK", "Risco de agressividade", "acute_risk", "BLOCK_ROUTINE", "governance_validated", "docs/008; docs/047", "Avaliacao medica de seguranca antes do ranking."),
    _context("DELIRIUM_CONCERN", "Delirium em avaliacao", "acute_risk", "BLOCK_ROUTINE", "governance_validated", "docs/010; docs/017", "Nao interpretar como transtorno psiquiatrico primario sem avaliacao."),
    _context("INTOXICATION_CONCERN", "Intoxicacao em avaliacao", "acute_risk", "BLOCK_ROUTINE", "governance_validated", "docs/010; docs/017", "Interromper comparacao farmacologica de rotina."),
    _context("WITHDRAWAL_CONCERN", "Abstinencia em avaliacao", "acute_risk", "BLOCK_ROUTINE", "governance_validated", "docs/010; docs/017", "Interromper comparacao farmacologica de rotina."),
    _context("ALLERGY_HISTORY", "Alergia medicamentosa", "adverse_history", "BLOCK_ROUTINE", "governance_validated", "docs/008; docs/047", "Revisar alergeno e exposicao antes da comparacao."),
    _context("SEVERE_ADVERSE_HISTORY", "Reacao adversa grave previa", "adverse_history", "BLOCK_ROUTINE", "governance_validated", "docs/008; docs/047", "Revisar o evento e a classe implicada antes da comparacao."),
    _context("AKATHISIA", "Acatisia em avaliacao", "adverse_syndrome", "REVIEW_CONTEXT", "source_pending", "coverage-audit", "Contexto estruturado; sem regra de manejo validada."),
    _context("DRUG_INDUCED_PARKINSONISM", "Parkinsonismo medicamentoso em avaliacao", "adverse_syndrome", "REVIEW_CONTEXT", "source_pending", "coverage-audit", "Contexto estruturado; sem regra de manejo validada."),
    _context("ACUTE_DYSTONIA", "Distonia aguda em avaliacao", "adverse_syndrome", "REVIEW_CONTEXT", "source_pending", "coverage-audit", "Contexto estruturado; sem regra de manejo validada."),
    _context("TARDIVE_DYSKINESIA", "Discinesia tardia em avaliacao", "adverse_syndrome", "REVIEW_CONTEXT", "source_pending", "coverage-audit", "Contexto estruturado; sem regra de manejo validada."),
    _context("SEROTONIN_SYNDROME", "Sindrome serotoninergica em avaliacao", "adverse_syndrome", "BLOCK_ROUTINE", "source_anchored_screening", "DM-SS", "Triagem apenas; nao diagnostica nem calcula manejo."),
    _context("NEUROLEPTIC_MALIGNANT_SYNDROME", "Sindrome neuroleptica maligna em avaliacao", "adverse_syndrome", "BLOCK_ROUTINE", "source_anchored_screening", "DM-NMS", "Triagem apenas; nao diagnostica nem calcula manejo."),
    _context("ALCOHOL_CONTEXT", "Alcool", "substance_context", "REVIEW_CONTEXT", "source_pending", "coverage-audit", "Registrar contexto sem inferir tratamento."),
    _context("OPIOID_CONTEXT", "Opioides", "substance_context", "REVIEW_CONTEXT", "source_pending", "coverage-audit", "Registrar contexto sem inferir tratamento."),
    _context("NICOTINE_CONTEXT", "Nicotina/tabaco", "substance_context", "REVIEW_CONTEXT", "source_pending", "coverage-audit", "Registrar contexto sem inferir tratamento."),
    _context("BENZODIAZEPINE_CONTEXT", "Benzodiazepinicos", "substance_context", "REVIEW_CONTEXT", "source_pending", "coverage-audit", "Registrar contexto sem inferir tratamento."),
    _context("STIMULANT_CONTEXT", "Estimulantes/anfetaminas", "substance_context", "REVIEW_CONTEXT", "source_pending", "coverage-audit", "Registrar contexto sem inferir tratamento."),
    _context("COCAINE_CRACK_CONTEXT", "Cocaina/crack", "substance_context", "REVIEW_CONTEXT", "source_pending", "coverage-audit", "Registrar contexto sem inferir tratamento."),
    _context("CANNABIS_CONTEXT", "Cannabis", "substance_context", "REVIEW_CONTEXT", "source_pending", "coverage-audit", "Registrar contexto sem inferir tratamento."),
    _context("HALLUCINOGEN_CONTEXT", "Alucinogenos/LSD", "substance_context", "REVIEW_CONTEXT", "source_pending", "coverage-audit", "Registrar contexto sem inferir tratamento."),
    _context("NEUROCOGNITIVE_CONTEXT", "Transtorno neurocognitivo/demencia", "diagnostic_boundary", "REVIEW_CONTEXT", "source_pending", "coverage-audit", "Contexto diferencial; sem conversao automatica em tratamento."),
    _context("DEVELOPMENTAL_CONTEXT", "Contexto do neurodesenvolvimento", "diagnostic_boundary", "REVIEW_CONTEXT", "source_pending", "coverage-audit", "Requer avaliacao populacional e diagnostica especifica."),
    _context("PERINATAL_CONTEXT", "Contexto perinatal", "population_boundary", "REVIEW_CONTEXT", "governance_validated", "docs/008; docs/047", "Usar estados separados de gestacao, lactacao e pos-parto."),
)


class ClinicalContextRegistry:
    def __init__(self) -> None:
        self._by_id = {item.context_id: item for item in CLINICAL_CONTEXTS}

    def all(self) -> tuple[ClinicalContextDefinition, ...]:
        return CLINICAL_CONTEXTS

    def assess(self, selected_ids: tuple[str, ...]) -> ClinicalContextAssessment:
        selected: list[ClinicalContextDefinition] = []
        unknown: list[str] = []
        warnings: list[str] = []
        for raw_id in selected_ids:
            context_id = str(raw_id or "").strip().upper()
            item = self._by_id.get(context_id)
            if item is None:
                if context_id:
                    unknown.append(context_id)
                continue
            if item not in selected:
                selected.append(item)
                if item.runtime_behavior == "BLOCK_ROUTINE":
                    warnings.append(f"{item.label}: revisao obrigatoria antes do ranking")
        warnings.extend(f"Contexto clinico desconhecido: {item}" for item in unknown)
        return ClinicalContextAssessment(
            selected=tuple(selected),
            blocking_warnings=tuple(warnings),
            unknown_ids=tuple(unknown),
        )

    def as_payload(self) -> list[dict[str, object]]:
        return [item.to_dict() for item in self.all()]
