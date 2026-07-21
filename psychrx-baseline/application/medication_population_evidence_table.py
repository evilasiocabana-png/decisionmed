"""Official age-population source excerpts for medication review."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from unicodedata import normalize


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POPULATION_EVIDENCE_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "medication_population_evidence.csv"
)


@dataclass(frozen=True)
class MedicationPopulationEvidence:
    """One source-transparent medication and age-band evidence row."""

    medication_name: str
    age_band: str
    population_summary: str
    dosage_summary: str
    source_abbreviation: str
    source_title: str
    source_url: str
    population_anchor: str
    evidence_status: str
    display_eligible: bool
    therapeutic_runtime_eligible: bool

    def display_line(self) -> str:
        """Return an informational line without creating a dose decision."""
        dosage = (
            f" Faixa/informacao por idade: {self.dosage_summary}"
            if self.dosage_summary
            else " Faixa/informacao por idade: nao localizada na fonte."
        )
        return (
            f"{self.medication_name} | {self.age_band}: "
            f"{self.population_summary}{dosage} ({self.source_abbreviation})"
        )


class MedicationPopulationEvidenceTable:
    """Read official population excerpts without authorizing therapeutic use."""

    def __init__(self, csv_path: Path | None = None) -> None:
        self._csv_path = csv_path or DEFAULT_POPULATION_EVIDENCE_PATH
        self._rows: tuple[MedicationPopulationEvidence, ...] | None = None

    def for_medication(
        self, medication_name: str, age_band: str
    ) -> MedicationPopulationEvidence | None:
        medication_key = self._normalize(medication_name)
        band = str(age_band or "UNKNOWN").strip().upper()
        for row in self._load():
            if (
                self._normalize(row.medication_name) == medication_key
                and row.age_band == band
                and row.display_eligible
            ):
                return row
        return None

    def for_medications(
        self, medication_names: tuple[str, ...], age_band: str, limit: int = 5
    ) -> tuple[MedicationPopulationEvidence, ...]:
        results = []
        seen = set()
        for name in medication_names:
            key = self._normalize(name)
            if not key or key in seen:
                continue
            seen.add(key)
            row = self.for_medication(name, age_band)
            if row:
                results.append(row)
            if len(results) >= limit:
                break
        return tuple(results)

    def _load(self) -> tuple[MedicationPopulationEvidence, ...]:
        if self._rows is not None:
            return self._rows
        if not self._csv_path.exists():
            self._rows = ()
            return self._rows
        with self._csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            self._rows = tuple(
                MedicationPopulationEvidence(
                    medication_name=row.get("medication_name", "").strip(),
                    age_band=row.get("age_band", "").strip().upper(),
                    population_summary=row.get("population_summary", "").strip(),
                    dosage_summary=row.get("dosage_summary", "").strip(),
                    source_abbreviation=row.get("source_abbreviation", "").strip()
                    or "PENDENTE",
                    source_title=row.get("source_title", "").strip(),
                    source_url=row.get("source_url", "").strip(),
                    population_anchor=row.get("population_anchor", "").strip(),
                    evidence_status=row.get("evidence_status", "").strip(),
                    display_eligible=row.get("display_eligible", "").lower() == "true",
                    therapeutic_runtime_eligible=(
                        row.get("therapeutic_runtime_eligible", "").lower() == "true"
                    ),
                )
                for row in csv.DictReader(handle)
                if row.get("medication_name", "").strip()
            )
        return self._rows

    @staticmethod
    def _normalize(value: str) -> str:
        text = normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode("ascii")
        return " ".join(text.lower().split())
