"""Read dose-dependent medication profile notes for display support.

The table is a research backlog, not a prescribing source. It lets the app show
whether dose-dependent pharmacological logic exists for a medication, while
keeping missing fields explicit as pending research.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from unicodedata import normalize

from application.clinical_decision_support_contract import EvidenceCitationPayload


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "medication_explanation_profile_backlog.csv"
)


@dataclass(frozen=True)
class MedicationDoseProfile:
    """Dose-dependent profile row for a medication."""

    medication_id: str
    medication_name: str
    dose_band: str
    dominant_effect: str
    receptor_or_mechanism: str
    pharmacological_target: str
    source_required: str
    source_reference: str
    current_source_status: str

    def is_pending(self) -> bool:
        """Return true when the dose-dependent profile is not yet sourced."""
        pending_values = {
            "",
            "PENDENTE_PESQUISAR",
            "NAO CADASTRADO",
            "nao cadastrado",
        }
        return (
            self.dose_band in pending_values
            or self.dominant_effect in pending_values
            or self.receptor_or_mechanism in pending_values
        )

    def display_summary(self) -> str:
        """Return a compact, UI-safe profile summary."""
        if self.is_pending():
            return (
                f"Dose - efeito: pendente pesquisar para {self.medication_name}. "
                "Cadastrar faixa por dose, efeito dominante e mecanismo/receptor "
                "com fonte antes de usar como explicacao."
            )
        return (
            f"Dose - efeito: {self.medication_name}: {self.dose_band}. "
            f"Classificacao do motor: {self.dominant_effect}. "
            f"Mecanismo/alvo: {self.receptor_or_mechanism or self.pharmacological_target}."
        )

    def citation(self) -> EvidenceCitationPayload:
        """Return traceability to the local backlog row."""
        return EvidenceCitationPayload(
            source_id=f"PSYCHRX-DOSE-PROFILE-{self.medication_id.upper()}",
            title="Medication explanation profile backlog",
            organization="PsychRx",
            year="2026",
            section=f"Perfil por dose / {self.medication_name}",
            excerpt_anchor=self.medication_id,
            evidence_type="local_backlog_table",
            quality=self.current_source_status or "backlog",
            applicability="display_support_pending_research",
            limitations=(
                "Tabela de backlog para explicabilidade do motor. Campos pendentes "
                "devem ser preenchidos com fonte rastreavel antes de uso conclusivo. "
                f"Fonte requerida: {self.source_required or 'nao informada'}. "
                f"Referencia local: {self.source_reference or 'nao informada'}."
            ),
        )


class MedicationDoseProfileTable:
    """Lookup table for dose-dependent medication profiles."""

    def __init__(self, csv_path: Path | None = None) -> None:
        self._csv_path = csv_path or DEFAULT_PROFILE_PATH
        self._profiles: tuple[MedicationDoseProfile, ...] | None = None

    def find(self, medication_name: str) -> MedicationDoseProfile | None:
        """Find a dose profile by medication name."""
        normalized = self._normalize(medication_name)
        if not normalized:
            return None
        for profile in self.profiles():
            profile_name = self._normalize(profile.medication_name)
            if profile_name and (profile_name in normalized or normalized in profile_name):
                return profile
        return None

    def profiles(self) -> tuple[MedicationDoseProfile, ...]:
        """Return all configured profiles."""
        if self._profiles is None:
            self._profiles = self._load_profiles()
        return self._profiles

    def _load_profiles(self) -> tuple[MedicationDoseProfile, ...]:
        if not self._csv_path.exists():
            return ()
        with self._csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = csv.DictReader(handle)
            return tuple(
                MedicationDoseProfile(
                    medication_id=row.get("medication_id", "").strip(),
                    medication_name=row.get("medication_name", "").strip(),
                    dose_band=row.get("dose_band", "").strip(),
                    dominant_effect=row.get("dominant_effect", "").strip(),
                    receptor_or_mechanism=row.get("receptor_or_mechanism", "").strip(),
                    pharmacological_target=row.get("pharmacological_target", "").strip(),
                    source_required=row.get("source_required", "").strip(),
                    source_reference=row.get("source_reference", "").strip(),
                    current_source_status=row.get("current_source_status", "").strip(),
                )
                for row in rows
                if row.get("medication_name", "").strip()
            )

    @staticmethod
    def _normalize(value: str) -> str:
        text = normalize("NFKD", value or "")
        return "".join(char for char in text if not char.encode("ascii", "ignore") == b"").lower()
