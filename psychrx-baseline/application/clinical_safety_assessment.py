"""Canonical safety-state assessment for local PsychRx decision support.

This module contains structural safety policy derived from the Clinical Safety
Contract. It does not diagnose a risk state or prescribe a response. It only
prevents missing or unresolved safety data from being interpreted as reassuring.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping
import unicodedata


ESSENTIAL_SAFETY_FIELDS = (
    "suicide",
    "aggression",
    "mania_or_hypomania",
    "substances",
    "delirium",
    "intoxication",
    "withdrawal",
    "allergies",
    "severe_adverse_reaction",
    "interactions",
    "qt_risk",
    "pregnancy_or_lactation",
    "metabolic_risk",
    "acute_toxicity",
)

SAFETY_LABELS = {
    "suicide": "Suicidio",
    "aggression": "Risco de agressividade",
    "mania_or_hypomania": "Mania/hipomania",
    "substances": "Alcool/drogas/medicacao sem controle",
    "delirium": "Delirium",
    "intoxication": "Intoxicacao",
    "withdrawal": "Abstinencia",
    "allergies": "Alergias medicamentosas",
    "severe_adverse_reaction": "Reacao adversa grave previa",
    "adherence": "Adesao",
    "adverse_effects": "Efeitos adversos",
    "interactions": "Interacoes medicamentosas",
    "qt_risk": "Risco de QT",
    "pregnancy_or_lactation": "Gestacao/lactacao",
    "metabolic_risk": "Risco metabolico",
    "acute_toxicity": "Possivel toxicidade/intoxicacao aguda",
}


def _normalize(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or "").strip().lower())
    return text.encode("ascii", "ignore").decode("ascii").replace("-", "_").replace(" ", "_")


SAFE_STATES = {
    "negado",
    "negada",
    "ausente",
    "ausentes",
    "avaliado_sem_risco",
    "not_applicable",
    "nao_aplicavel",
}
PRESENT_STATES = {"presente", "present", "positivo", "positiva", "relevante", "relevantes"}
UNRESOLVED_STATES = {
    "",
    "not_assessed",
    "nao_avaliado",
    "nao_avaliada",
    "unknown",
    "desconhecido",
    "desconhecida",
}


@dataclass(frozen=True)
class ClinicalSafetyAssessment:
    """Display-safe result of structural safety completeness checks."""

    normalized_states: tuple[tuple[str, str], ...]
    warnings: tuple[str, ...]
    missing_or_unknown: tuple[str, ...]
    present_risks: tuple[str, ...]

    @property
    def closed(self) -> bool:
        return not self.warnings


class ClinicalSafetyAssessmentService:
    """Evaluate whether essential safety domains were explicitly assessed."""

    def assess(
        self,
        safety: Mapping[str, object] | None,
        *,
        has_current_medication: bool,
    ) -> ClinicalSafetyAssessment:
        values = safety or {}
        normalized = {field: _normalize(values.get(field, "not_assessed")) for field in ESSENTIAL_SAFETY_FIELDS}
        warnings: list[str] = []
        missing: list[str] = []
        present: list[str] = []

        for field in ESSENTIAL_SAFETY_FIELDS:
            state = normalized[field]
            label = SAFETY_LABELS[field]
            if state in SAFE_STATES:
                continue
            if state in PRESENT_STATES:
                warnings.append(f"{label}: Presente")
                present.append(field)
                continue
            warnings.append(f"{label}: Nao avaliado")
            missing.append(field)

        if has_current_medication:
            adherence = _normalize(values.get("adherence", "not_assessed"))
            normalized["adherence"] = adherence
            if adherence not in {"boa", "good", "adequada", "regular"}:
                display = "Nao avaliada" if adherence in UNRESOLVED_STATES else str(values.get("adherence", "Nao avaliada"))
                warnings.append(f"{SAFETY_LABELS['adherence']}: {display}")
                if adherence in UNRESOLVED_STATES:
                    missing.append("adherence")

            adverse = _normalize(values.get("adverse_effects", "not_assessed"))
            normalized["adverse_effects"] = adverse
            if adverse not in SAFE_STATES and adverse not in {"boa", "good"}:
                display = "Nao avaliados" if adverse in UNRESOLVED_STATES else str(values.get("adverse_effects", "Nao avaliados"))
                warnings.append(f"{SAFETY_LABELS['adverse_effects']}: {display}")
                if adverse in UNRESOLVED_STATES:
                    missing.append("adverse_effects")
        else:
            normalized["adherence"] = "not_applicable"
            normalized["adverse_effects"] = "not_applicable"

        return ClinicalSafetyAssessment(
            normalized_states=tuple(normalized.items()),
            warnings=tuple(dict.fromkeys(warnings)),
            missing_or_unknown=tuple(dict.fromkeys(missing)),
            present_risks=tuple(dict.fromkeys(present)),
        )
