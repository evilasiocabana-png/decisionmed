"""Motor 2 strategy matrix for dose-effect aware decision support.

Motor 2 is a parallel layer over the original pharmacological motor.  It
crosses current medication, current dose, dose-effect notes, and the
condition-specific range from the reviewed matrix.  It never invents a range:
when the medication-condition pair is absent, it returns an explicit review
state instead of calling the action "dose optimization".
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from unicodedata import normalize


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MOTOR2_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "motor2_strategy_matrix.csv"
)


@dataclass(frozen=True)
class Motor2StrategyRow:
    """One Motor 2 row produced from dose-effect x condition range crossing."""

    medication_id: str
    medication_name: str
    drug_class: str
    condition_or_context: str
    condition_key: str
    dose_effect_band: str
    dose_effect_min: str
    dose_effect_max: str
    dose_effect_goal: str
    dominant_effect: str
    mechanism_or_target: str
    condition_range: str
    condition_range_min: str
    condition_range_max: str
    range_source: str
    strategy_if_below_range: str
    strategy_if_within_range_partial_response: str
    strategy_if_within_range_no_response: str
    strategy_if_above_range: str
    strategy_if_range_missing: str
    dose_effect_source: str
    evidence_status: str
    notes: str

    def has_condition_range(self) -> bool:
        """Return true when a reviewed range exists for this condition."""
        return bool(self.condition_range and self.condition_range != "nao cadastrado")

    def has_dose_effect_range(self) -> bool:
        """Return true when a source-backed dose-effect range can be compared."""
        normalized_band = self.dose_effect_band.lower()
        has_pending_marker = (
            "pendente_pesquisar" in normalized_band
            or "pendente pesquisar" in normalized_band
        )
        return bool(
            self.dose_effect_band
            and self.dose_effect_min
            and self.dose_effect_max
            and not has_pending_marker
        )

    def has_dose_effect_text(self) -> bool:
        """Return true when dose-effect text exists but cannot be numeric-compared."""
        normalized_band = self.dose_effect_band.lower()
        has_pending_marker = (
            "pendente_pesquisar" in normalized_band
            or "pendente pesquisar" in normalized_band
        )
        return bool(self.dose_effect_band and not has_pending_marker)

    def display_range(self) -> str:
        """Return the range text for UI summaries."""
        if self.has_condition_range():
            return (
                f"{self.medication_name} / {self.condition_or_context}: "
                f"{self.condition_range}"
            )
        if self.has_dose_effect_range():
            return (
                f"{self.medication_name} / dose-efeito: "
                f"{self.dose_effect_min}-{self.dose_effect_max} mg/dia"
            )
        if self.has_dose_effect_text():
            return f"{self.medication_name} / dose-efeito contextual: {self.dose_effect_band}"
        return f"{self.medication_name} / faixa por quadro: nao cadastrada"


@dataclass(frozen=True)
class Motor2StrategyAssessment:
    """Action hint derived from Motor 2 for one current medication."""

    row: Motor2StrategyRow | None
    dose_status: str
    suggested_action: str
    strategy_text: str
    reason: str


class Motor2StrategyMatrix:
    """Lookup and strategy helper for the Motor 2 matrix."""

    def __init__(self, csv_path: Path | None = None) -> None:
        self._csv_path = csv_path or DEFAULT_MOTOR2_PATH
        self._rows: tuple[Motor2StrategyRow, ...] | None = None

    def rows(self) -> tuple[Motor2StrategyRow, ...]:
        """Return all Motor 2 rows."""
        if self._rows is None:
            self._rows = self._load_rows()
        return self._rows

    def rows_for(self, medication_name: str) -> tuple[Motor2StrategyRow, ...]:
        """Return rows for a medication name."""
        normalized = self._normalize_medication(medication_name)
        if not normalized:
            return ()
        return tuple(
            row
            for row in self.rows()
            if self._normalize_medication(row.medication_name) == normalized
        )

    def assess(
        self,
        *,
        medication_name: str,
        current_dose: str,
        clinical_text: str = "",
        response_state: str = "",
    ) -> Motor2StrategyAssessment:
        """Return a Motor 2 strategy assessment.

        The assessment only asserts dose optimization when a condition-specific
        range exists and the current dose is below it.
        """
        row = self._best_row(
            medication_name=medication_name,
            clinical_text=clinical_text,
        )
        if row is None:
            return Motor2StrategyAssessment(
                row=None,
                dose_status="missing_motor2_row",
                suggested_action="optimize_current",
                strategy_text=(
                    "Revisar tratamento atual: Motor 2 ainda nao possui linha "
                    "para este medicamento."
                ),
                reason="motor2_row_missing",
            )
        if (
            not row.has_condition_range()
            and not row.has_dose_effect_range()
            and not row.has_dose_effect_text()
        ):
            return Motor2StrategyAssessment(
                row=row,
                dose_status="condition_range_missing",
                suggested_action="optimize_current",
                strategy_text=(
                    f"Revisar {row.medication_name}: faixa por quadro nao "
                    "cadastrada; usar dose-efeito como contexto e nao afirmar "
                    "otimizacao ate cadastrar a faixa por quadro."
                ),
                reason=row.strategy_if_range_missing,
            )
        if not row.has_condition_range() and not row.has_dose_effect_range():
            return Motor2StrategyAssessment(
                row=row,
                dose_status="qualitative_dose_effect_range",
                suggested_action="optimize_current",
                strategy_text=(
                    f"Revisar {row.medication_name}: faixa numerica por quadro "
                    "nao cadastrada; usar dose-efeito contextual, resposta, "
                    "seguranca e via/formulacao antes de ajustar."
                ),
                reason=row.strategy_if_range_missing,
            )
        range_basis = "condition_range" if row.has_condition_range() else "dose_effect_range"
        status = self._dose_status(current_dose, row, range_basis=range_basis)
        response = self._normalize(response_state)
        range_label = (
            f"faixa por quadro {row.condition_range}"
            if row.has_condition_range()
            else f"faixa por dose-efeito {row.dose_effect_min}-{row.dose_effect_max} mg/dia"
        )
        if status in {"below_registered_range", "below_dose_effect_range"}:
            return Motor2StrategyAssessment(
                row=row,
                dose_status=status,
                suggested_action="increase_dose",
                strategy_text=(
                    f"Considerar otimizacao de {row.medication_name} para "
                    f"{range_label}."
                ),
                reason=row.strategy_if_below_range,
            )
        if status in {"above_registered_range", "above_dose_effect_range"}:
            return Motor2StrategyAssessment(
                row=row,
                dose_status=status,
                suggested_action="optimize_current",
                strategy_text=(
                    f"Revisar {row.medication_name}: dose atual acima da "
                    f"{range_label}; checar seguranca antes "
                    "de manter ou ajustar."
                ),
                reason=row.strategy_if_above_range,
            )
        if "sem resposta" in response:
            return Motor2StrategyAssessment(
                row=row,
                dose_status=status,
                suggested_action="substitute",
                strategy_text=(
                    f"Discutir troca ou revisao diagnostica: {row.medication_name} "
                    f"ja esta na {range_label}."
                ),
                reason=row.strategy_if_within_range_no_response,
            )
        return Motor2StrategyAssessment(
            row=row,
            dose_status=status,
            suggested_action="optimize_current",
            strategy_text=(
                f"Revisar resposta parcial: {row.medication_name} ja esta na "
                f"{range_label}; checar tempo, adesao e tolerabilidade, e confirmar "
                "quais sintomas ou prejuizos permanecem antes de discutir troca ou associacao."
            ),
            reason=row.strategy_if_within_range_partial_response,
        )

    def _best_row(
        self,
        *,
        medication_name: str,
        clinical_text: str,
    ) -> Motor2StrategyRow | None:
        candidates = self.rows_for(medication_name)
        if not candidates:
            return None
        normalized_context = self._normalize(clinical_text)
        scored: list[tuple[int, Motor2StrategyRow]] = []
        for row in candidates:
            score = 0
            condition_text = self._normalize(
                f"{row.condition_or_context} {row.condition_key}"
            )
            for token in condition_text.split():
                if len(token) > 3 and token in normalized_context:
                    score += 1
            if row.has_condition_range():
                score += 2
            if row.range_source and row.range_source != "PENDENTE_PESQUISAR":
                score += 1
            scored.append((score, row))
        scored.sort(key=lambda item: item[0], reverse=True)
        return scored[0][1]

    @staticmethod
    def _dose_status(
        current_dose: str,
        row: Motor2StrategyRow,
        *,
        range_basis: str = "condition_range",
    ) -> str:
        dose = Motor2StrategyMatrix._first_number(current_dose)
        if range_basis == "dose_effect_range":
            low = Motor2StrategyMatrix._first_number(row.dose_effect_min)
            high = Motor2StrategyMatrix._first_number(row.dose_effect_max)
            below = "below_dose_effect_range"
            above = "above_dose_effect_range"
            within = "within_dose_effect_range"
        else:
            low = Motor2StrategyMatrix._first_number(row.condition_range_min)
            high = Motor2StrategyMatrix._first_number(row.condition_range_max)
            below = "below_registered_range"
            above = "above_registered_range"
            within = "within_registered_range"
        if dose is None or low is None or high is None:
            return "dose_indeterminate"
        if dose < low:
            return below
        if dose > high:
            return above
        return within

    def _load_rows(self) -> tuple[Motor2StrategyRow, ...]:
        if not self._csv_path.exists():
            return ()
        with self._csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            return tuple(
                Motor2StrategyRow(**{field: row.get(field, "").strip() for field in Motor2StrategyRow.__dataclass_fields__})
                for row in csv.DictReader(handle)
                if row.get("medication_name", "").strip()
            )

    @staticmethod
    def _first_number(value: str) -> float | None:
        match = re.search(r"\d+(?:[.,]\d+)?", str(value or ""))
        if not match:
            return None
        return float(match.group(0).replace(",", "."))

    @staticmethod
    def _normalize(value: str) -> str:
        text = normalize("NFKD", str(value or "").lower()).encode("ascii", "ignore")
        return text.decode("ascii")

    @classmethod
    def _normalize_medication(cls, value: str) -> str:
        normalized = cls._normalize(value)
        normalized = normalized.replace(" xr", "").replace(" xl", "")
        return "".join(char for char in normalized if char.isalnum())
