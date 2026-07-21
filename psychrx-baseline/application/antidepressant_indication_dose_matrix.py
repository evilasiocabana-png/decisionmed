"""Dose-range lookup from the audited antidepressant indication matrix.

The table represents the user's reviewed Aba 1: medication x condition.  This
module only returns registered ranges. It never invents a range when a
medication/condition pair is absent.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from unicodedata import normalize

from application.clinical_decision_support_contract import EvidenceCitationPayload


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "antidepressant_indication_matrix_table1.csv"
)

CONDITION_LABELS = {
    "TAG": "TAG",
    "panico": "panico",
    "transtorno_de_estresse": "transtorno de estresse",
    "fobias": "fobias",
    "fobia_social": "fobia social",
    "TOC": "TOC",
    "depressao_melancolica": "depressao melancolica",
    "depressao_ansiosa": "depressao ansiosa",
    "depressao_com_agitacao_agressiva": "depressao com agitacao/agressividade",
    "depressao_atipica": "depressao atipica",
    "dor": "dor",
    "vicios": "vicios",
    "tabagismo": "tabagismo",
    "compulsao": "compulsao",
    "bulimia_anorexia": "bulimia/anorexia",
    "TDPM": "TDPM",
    "ideacao_suicida": "ideacao suicida",
}


@dataclass(frozen=True)
class IndicationDoseRange:
    """Registered range for one medication-condition pair."""

    medication: str
    condition_key: str
    condition_label: str
    range_text: str
    source: EvidenceCitationPayload


class AntidepressantIndicationDoseMatrix:
    """Looks up ranges in the reviewed medication x condition matrix."""

    def __init__(self, matrix_path: Path | None = None) -> None:
        self._matrix_path = matrix_path or DEFAULT_MATRIX_PATH
        self._rows: tuple[dict[str, str], ...] | None = None

    def range_for(
        self,
        *,
        medication_name: str,
        clinical_presentation: str = "",
        symptoms: tuple[str, ...] = (),
        pharmacological_profile: tuple[str, ...] = (),
        impairment_domains: tuple[str, ...] = (),
        diagnostic_context: str = "",
        therapeutic_objective: str = "",
    ) -> IndicationDoseRange | None:
        """Return a registered range or None when the pair is absent."""
        row = self._find_row(medication_name)
        if not row:
            return None
        for key in self._candidate_conditions(
            clinical_presentation=clinical_presentation,
            symptoms=symptoms,
            pharmacological_profile=pharmacological_profile,
            impairment_domains=impairment_domains,
            diagnostic_context=diagnostic_context,
            therapeutic_objective=therapeutic_objective,
        ):
            value = row.get(key, "").strip()
            if self._is_registered_range(value):
                return IndicationDoseRange(
                    medication=row["medicamento"],
                    condition_key=key,
                    condition_label=CONDITION_LABELS.get(key, key),
                    range_text=value,
                    source=self._citation(row["medicamento"], key),
                )
        return None

    def _find_row(self, medication_name: str) -> dict[str, str] | None:
        normalized = self._normalize_medication(medication_name)
        if not normalized:
            return None
        for row in self._load_rows():
            row_name = self._normalize_medication(row.get("medicamento", ""))
            if row_name and (row_name in normalized or normalized in row_name):
                return row
        return None

    def _load_rows(self) -> tuple[dict[str, str], ...]:
        if self._rows is None:
            if not self._matrix_path.exists():
                self._rows = ()
            else:
                with self._matrix_path.open("r", encoding="utf-8", newline="") as handle:
                    self._rows = tuple(csv.DictReader(handle))
        return self._rows

    def _candidate_conditions(
        self,
        *,
        clinical_presentation: str,
        symptoms: tuple[str, ...],
        pharmacological_profile: tuple[str, ...],
        impairment_domains: tuple[str, ...],
        diagnostic_context: str,
        therapeutic_objective: str,
    ) -> tuple[str, ...]:
        text = self._normalize(
            " ".join(
                (
                    clinical_presentation,
                    diagnostic_context,
                    therapeutic_objective,
                    *symptoms,
                    *pharmacological_profile,
                    *impairment_domains,
                )
            )
        )
        keys: list[str] = []
        if "ideacao" in text or "suicid" in text:
            keys.append("ideacao_suicida")
        if "tabag" in text:
            keys.append("tabagismo")
        if "vicio" in text or "substancia" in text or "alcool" in text or "dependencia" in text:
            keys.append("vicios")
        if "bulimia" in text or "anorexia" in text or "alimentar" in text:
            keys.append("bulimia_anorexia")
        if "tdpm" in text:
            keys.append("TDPM")
        if "toc" in text or "obsess" in text:
            keys.append("TOC")
        if "compuls" in text:
            keys.append("compulsao")
        if "dor" in text or "somatic" in text:
            keys.append("dor")
        if "panico" in text:
            keys.append("panico")
        if "fobia social" in text:
            keys.append("fobia_social")
        if "fobia" in text:
            keys.append("fobias")
        if "estresse" in text or "trauma" in text:
            keys.append("transtorno_de_estresse")
        if "agitacao" in text or "agressiv" in text or "irritabilidade" in text:
            keys.append("depressao_com_agitacao_agressiva")
        if "atipic" in text:
            keys.append("depressao_atipica")
        if "melancol" in text:
            keys.append("depressao_melancolica")
        if "depress" in text and "ansiedad" in text:
            keys.append("depressao_ansiosa")
        if "ansiedad" in text or "tensao" in text:
            keys.append("TAG")
        if "depress" in text or "humor" in text or "anedonia" in text:
            keys.append("depressao_ansiosa")
        return tuple(dict.fromkeys(keys))

    @staticmethod
    def _is_registered_range(value: str) -> bool:
        normalized = value.strip().upper()
        return bool(value.strip()) and normalized != "X"

    def _citation(self, medication: str, condition_key: str) -> EvidenceCitationPayload:
        return EvidenceCitationPayload(
            source_id=f"PSYCHRX-ABA1-DOSE-{self._normalize_medication(medication).upper()}-{condition_key.upper()}",
            title="Aba 1 - Matriz antidepressivo medicamento x doenca",
            organization="PsychRx",
            year="2026",
            section=f"{medication} / {CONDITION_LABELS.get(condition_key, condition_key)}",
            excerpt_anchor=f"{self._normalize_medication(medication)}:{condition_key}",
            evidence_type="curated_local_dose_matrix",
            quality="local_reviewed_table",
            applicability="physician_review_only",
            limitations=(
                "Faixa transcrita da matriz local; nao substitui bula, diretriz, "
                "contraindicacoes, individualizacao de dose ou julgamento medico."
            ),
        )

    @staticmethod
    def _normalize(value: str) -> str:
        without_accents = normalize("NFKD", value.lower()).encode("ascii", "ignore")
        return without_accents.decode("ascii")

    def _normalize_medication(self, value: str) -> str:
        normalized = self._normalize(value)
        normalized = normalized.replace(" xr", "")
        normalized = normalized.replace(" xl", "")
        for token in ("50-100", "60-120", "20-40", "10-20", "150-300"):
            normalized = normalized.replace(token, "")
        return "".join(char for char in normalized if char.isalnum())
