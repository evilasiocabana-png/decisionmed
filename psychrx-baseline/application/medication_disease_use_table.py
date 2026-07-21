"""Read medication disease-use roles for decision-support display."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from unicodedata import normalize


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DISEASE_USE_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "medication_disease_use_matrix.csv"
)
DEFAULT_EVIDENCE_REVIEW_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "medication_disease_use_evidence_review.csv"
)


@dataclass(frozen=True)
class MedicationDiseaseUse:
    """One medication-to-disease/context role."""

    medication_name: str
    disease_or_context: str
    role: str
    status: str
    phase: str
    notes: str
    source_reference: str
    review_status: str
    source_abbreviation: str = "PENDENTE"

    def display_line(self) -> str:
        """Return a compact display-safe use line."""
        parts = [
            self.disease_or_context,
            self.role.replace("_", " "),
            self.status.replace("_", " "),
        ]
        if self.phase:
            parts.append(self.phase.replace("_", " "))
        content = " | ".join(part for part in parts if part)
        return f"{content} ({self.source_abbreviation})"


class MedicationDiseaseUseTable:
    """Lookup medication disease-use roles from the local motor table."""

    def __init__(
        self,
        csv_path: Path | None = None,
        evidence_review_path: Path | None = None,
    ) -> None:
        self._csv_path = csv_path or DEFAULT_DISEASE_USE_PATH
        self._evidence_review_path = evidence_review_path or DEFAULT_EVIDENCE_REVIEW_PATH
        self._uses: tuple[MedicationDiseaseUse, ...] | None = None

    def uses_for(self, medication_name: str, limit: int = 4) -> tuple[MedicationDiseaseUse, ...]:
        """Return disease-use rows for the given medication."""
        matched = self.all_uses_for(medication_name)
        return tuple(matched[:limit])

    def all_uses_for(self, medication_name: str) -> tuple[MedicationDiseaseUse, ...]:
        """Return every disease-use row for the given medication."""
        normalized = self._normalize(medication_name)
        if not normalized:
            return ()
        matched = [
            item
            for item in self.uses()
            if self._normalize(item.medication_name) == normalized
        ]
        return tuple(matched)

    def summary_for(self, medication_name: str, limit: int = 4) -> tuple[str, ...]:
        """Return compact disease-use summary lines."""
        uses = self.uses_for(medication_name, limit=limit)
        if not uses:
            return (f"{medication_name or 'Medicamento'}: uso por doenca nao cadastrado.",)
        return tuple(item.display_line() for item in uses)

    def uses(self) -> tuple[MedicationDiseaseUse, ...]:
        """Return all configured disease-use rows."""
        if self._uses is None:
            self._uses = self._load_uses()
        return self._uses

    def _load_uses(self) -> tuple[MedicationDiseaseUse, ...]:
        if not self._csv_path.exists():
            return ()
        evidence_rows = self._evidence_rows()
        evidence_by_key = {
            self._key(
                row.get("medication_name", ""),
                row.get("disease_or_context", ""),
            ): row
            for row in evidence_rows
        }
        with self._csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = csv.DictReader(handle)
            uses = []
            for row in rows:
                medication_name = row.get("medication_name", "").strip()
                disease_or_context = row.get("disease_or_context", "").strip()
                if not medication_name:
                    continue
                evidence = evidence_by_key.get(
                    self._key(medication_name, disease_or_context), {}
                )
                uses.append(
                    MedicationDiseaseUse(
                        medication_name=medication_name,
                        disease_or_context=disease_or_context,
                        role=row.get("role", "").strip(),
                        status=row.get("status", "").strip(),
                        phase=row.get("phase", "").strip(),
                        notes=row.get("notes", "").strip(),
                        source_reference=row.get("source_reference", "").strip(),
                        review_status=row.get("review_status", "").strip(),
                        source_abbreviation=self._source_abbreviation(evidence, row),
                    )
                )
            return tuple(uses)

    def _evidence_rows(self) -> list[dict[str, str]]:
        if not self._evidence_review_path.exists():
            return []
        with self._evidence_review_path.open(
            "r", encoding="utf-8-sig", newline=""
        ) as handle:
            return list(csv.DictReader(handle))

    def _source_abbreviation(
        self, evidence: dict[str, str], row: dict[str, str]
    ) -> str:
        evidence_status = evidence.get("evidence_review_status", "")
        official_anchor = evidence.get("official_source_anchor", "")
        if evidence_status == "official_label_indication_match":
            return self._abbreviation_for(official_anchor) or "OFICIAL"
        reference = row.get("source_reference", "")
        mapped = self._abbreviation_for(reference)
        if mapped:
            return f"{mapped}/PENDENTE"
        return "PENDENTE"

    @staticmethod
    def _abbreviation_for(value: str) -> str:
        normalized = str(value or "").lower()
        if "dailymed.nlm.nih.gov" in normalized or "dailymed" in normalized:
            return "DM"
        if "ema.europa.eu" in normalized or " ema" in f" {normalized}":
            return "EMA"
        if "nice.org.uk" in normalized or "nice " in normalized:
            return "NICE"
        if "canada.ca" in normalized or "health canada" in normalized:
            return "HC"
        if "anvisa" in normalized:
            return "ANVISA"
        return ""

    def _key(self, medication_name: str, disease_or_context: str) -> tuple[str, str]:
        return self._normalize(medication_name), self._normalize(disease_or_context)

    @staticmethod
    def _normalize(value: str) -> str:
        text = normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii")
        return " ".join(text.lower().replace("/", " ").replace("-", " ").split())
