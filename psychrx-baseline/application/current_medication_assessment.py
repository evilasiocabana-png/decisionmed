"""Current medication assessment for the local decision-support motor."""

from __future__ import annotations

import re
from dataclasses import dataclass

from application.clinical_decision_support_contract import (
    CurrentMedicationPayload,
    EvidenceCitationPayload,
)
from application.medication_strategy_table import MedicationStrategyTable


@dataclass(frozen=True)
class CurrentMedicationAssessment:
    """Structured assessment of the medication already in use."""

    medication_name: str
    current_dose: str
    registered_range: str
    current_dose_status: str
    duration_status: str
    response_status: str
    tolerability_status: str
    adherence_status: str
    optimization_possible: str
    source: EvidenceCitationPayload | None
    missing_fields: tuple[str, ...] = ()

    def summary(self) -> str:
        """Return a physician-facing, non-prescriptive summary."""
        missing = (
            f" Dados faltantes: {', '.join(self.missing_fields)}."
            if self.missing_fields
            else ""
        )
        return (
            "Avaliacao da medicacao atual: "
            f"{self.medication_name or 'nao informada'} {self.current_dose or 'dose nao informada'}. "
            f"Faixa cadastrada: {self.registered_range or 'nao localizada'}. "
            f"Dose atual: {self._human(self.current_dose_status)}. "
            f"Tempo de uso: {self._human(self.duration_status)}. "
            f"Adesao: {self._human(self.adherence_status)}. "
            f"Resposta: {self._human(self.response_status)}. "
            f"Tolerabilidade: {self._human(self.tolerability_status)}. "
            f"Otimizacao antes de troca: {self._human(self.optimization_possible)}."
            f"{missing}"
        )

    @staticmethod
    def _human(value: str) -> str:
        labels = {
            "below_registered_range": "abaixo da faixa cadastrada",
            "within_registered_range": "dentro da faixa cadastrada",
            "above_registered_range": "acima da faixa cadastrada",
            "dose_indeterminate": "indeterminada",
            "duration_possibly_insufficient": "possivelmente insuficiente",
            "duration_possibly_sufficient": "possivelmente suficiente",
            "duration_indeterminate": "indeterminado",
            "good_response": "boa resposta",
            "partial_response": "resposta parcial",
            "no_response": "sem resposta",
            "response_indeterminate": "indeterminada",
            "good_adherence": "boa",
            "insufficient_adherence": "insuficiente",
            "adherence_indeterminate": "indeterminada",
            "good_tolerability": "boa",
            "mild_adverse_effects": "efeitos leves",
            "moderate_adverse_effects": "efeitos moderados",
            "poor_tolerability": "ruim ou efeitos relevantes",
            "tolerability_indeterminate": "indeterminada",
            "possible_for_physician_review": "possivel para revisao medica",
            "not_favored": "nao favorecida",
            "indeterminate": "indeterminada",
        }
        return labels.get(value, value or "indeterminada")


class CurrentMedicationAssessmentService:
    """Calculates dose, duration, response and tolerability status."""

    def __init__(self, medication_table: MedicationStrategyTable | None = None) -> None:
        self._medication_table = medication_table or MedicationStrategyTable()

    def assess_all(
        self, medications: tuple[CurrentMedicationPayload, ...]
    ) -> tuple[CurrentMedicationAssessment, ...]:
        return tuple(self.assess(item) for item in medications if item.name.strip())

    def assess(self, medication: CurrentMedicationPayload) -> CurrentMedicationAssessment:
        dose_target, source = self._medication_table.current_dose_target(medication.name)
        current_dose = self._format_current_dose(medication)
        missing = self._missing_fields(medication)
        dose_basis = medication.dose_used or medication.dose_value or medication.dose_prescribed
        dose_status = self._dose_status(dose_basis, dose_target)
        duration_status = self._duration_status(medication.duration)
        if medication.duration_current_dose:
            duration_status = self._duration_status(medication.duration_current_dose)
        adherence_status = self._adherence_status(medication.adherence)
        response_status = self._response_status(medication.response)
        tolerability_status = self._tolerability_status(medication.tolerability)
        optimization_possible = self._optimization_possible(
            dose_status=dose_status,
            duration_status=duration_status,
            adherence_status=adherence_status,
            response_status=response_status,
            tolerability_status=tolerability_status,
        )
        return CurrentMedicationAssessment(
            medication_name=medication.name,
            current_dose=current_dose,
            registered_range=dose_target,
            current_dose_status=dose_status,
            duration_status=duration_status,
            adherence_status=adherence_status,
            response_status=response_status,
            tolerability_status=tolerability_status,
            optimization_possible=optimization_possible,
            source=source,
            missing_fields=missing,
        )

    @staticmethod
    def _format_current_dose(medication: CurrentMedicationPayload) -> str:
        dose_value = (
            str(medication.dose_used).strip()
            or str(medication.dose_value).strip()
            or str(medication.dose_prescribed).strip()
        )
        dose = " ".join(
            part
            for part in (dose_value, medication.dose_unit.strip())
            if part
        )
        frequency = medication.frequency.strip() or medication.schedule.strip()
        return f"{dose} {frequency}".strip()

    @staticmethod
    def _missing_fields(medication: CurrentMedicationPayload) -> tuple[str, ...]:
        missing = []
        for field_name in (
            "dose_value",
            "dose_unit",
            "frequency",
            "duration",
            "adherence",
            "response",
            "tolerability",
        ):
            if not str(getattr(medication, field_name, "")).strip():
                missing.append(field_name)
        return tuple(missing)

    def _dose_status(self, dose_value: str, registered_range: str) -> str:
        dose = self._first_number(dose_value)
        range_values = self._range_numbers(registered_range)
        if dose is None or range_values is None:
            return "dose_indeterminate"
        low, high = range_values
        if dose < low:
            return "below_registered_range"
        if dose > high:
            return "above_registered_range"
        return "within_registered_range"

    @staticmethod
    def _duration_status(duration: str) -> str:
        text = duration.lower().strip()
        if not text:
            return "duration_indeterminate"
        value = CurrentMedicationAssessmentService._first_number(text)
        if value is None:
            return "duration_indeterminate"
        if "dia" in text:
            days = value
        elif "semana" in text:
            days = value * 7
        elif "mes" in text:
            days = value * 30
        else:
            days = value
        return (
            "duration_possibly_sufficient"
            if days >= 28
            else "duration_possibly_insufficient"
        )

    @staticmethod
    def _response_status(response: str) -> str:
        text = response.lower()
        if "sem resposta" in text or "nenhuma" in text:
            return "no_response"
        if "parcial" in text or "pouca" in text:
            return "partial_response"
        if "boa" in text or "remissao" in text or "adequada" in text:
            return "good_response"
        return "response_indeterminate"

    @staticmethod
    def _adherence_status(adherence: str) -> str:
        text = adherence.lower()
        if "ruim" in text or "irregular" in text or "baixa" in text or "insuf" in text:
            return "insufficient_adherence"
        if "boa" in text or "regular" in text:
            return "good_adherence"
        return "adherence_indeterminate"

    @staticmethod
    def _tolerability_status(tolerability: str) -> str:
        text = tolerability.lower()
        if "ruim" in text or "grave" in text or "relevante" in text:
            return "poor_tolerability"
        if "moderad" in text:
            return "moderate_adverse_effects"
        if "leve" in text:
            return "mild_adverse_effects"
        if "boa" in text or "sem efeito" in text:
            return "good_tolerability"
        return "tolerability_indeterminate"

    @staticmethod
    def _optimization_possible(
        *,
        dose_status: str,
        duration_status: str,
        adherence_status: str,
        response_status: str,
        tolerability_status: str,
    ) -> str:
        if adherence_status == "insufficient_adherence":
            return "not_favored"
        if tolerability_status in {"poor_tolerability", "moderate_adverse_effects"}:
            return "not_favored"
        if dose_status == "above_registered_range":
            return "not_favored"
        if response_status in {"partial_response", "no_response"} and dose_status == "below_registered_range":
            return "possible_for_physician_review"
        if duration_status == "duration_possibly_insufficient":
            return "indeterminate"
        return "indeterminate"

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
