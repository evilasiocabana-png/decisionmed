"""Local medication strategy table for PsychRx decision support.

The table is intentionally small and traceable. It provides candidate options
for physician review; it does not prescribe, rank drugs autonomously, or choose
a patient-specific medication.
"""

from __future__ import annotations

from dataclasses import dataclass
from unicodedata import normalize

from application.clinical_decision_support_contract import EvidenceCitationPayload
from application.motor_table_repository import MotorTableEntry, MotorTableRepository


@dataclass(frozen=True)
class MedicationStrategyEntry:
    """Medication facts used by the local strategy table."""

    name: str
    drug_class: str
    targets: tuple[str, ...]
    usual_adult_range: str
    source: EvidenceCitationPayload
    cautions: tuple[str, ...]
    substitution_fit: tuple[str, ...]
    association_fit: tuple[str, ...]


def _citation(source_id: str, title: str, section: str) -> EvidenceCitationPayload:
    return EvidenceCitationPayload(
        source_id=source_id,
        title=title,
        organization="DailyMed / U.S. National Library of Medicine",
        year="accessed 2026",
        section=section,
        excerpt_anchor=section.lower().replace(" ", "-"),
        evidence_type="prescribing_information",
        quality="official_label",
        applicability="dose_information_for_physician_review",
        limitations=(
            "Informational label range only; individual prescribing requires "
            "physician judgment, diagnosis, contraindications, interactions, "
            "local labeling, and patient context."
        ),
    )


MEDICATION_STRATEGY_TABLE: tuple[MedicationStrategyEntry, ...] = (
    MedicationStrategyEntry(
        name="Sertralina",
        drug_class="SSRI",
        targets=("ansiedade / serotoninergico", "humor / energia / antidepressivo"),
        usual_adult_range="MDD: 50 mg once daily; max 200 mg/day.",
        source=_citation("DM-SERTRALINE", "DailyMed Sertraline tablet", "Dosage and Administration - MDD"),
        cautions=("screen bipolar disorder", "serotonergic interactions", "sexual dysfunction", "GI effects"),
        substitution_fit=("ansiedade / serotoninergico",),
        association_fit=(),
    ),
    MedicationStrategyEntry(
        name="Escitalopram",
        drug_class="SSRI",
        targets=("ansiedade / serotoninergico", "humor / energia / antidepressivo"),
        usual_adult_range="MDD: 10 mg once daily; max 20 mg/day.",
        source=_citation("DM-ESCITALOPRAM", "DailyMed Escitalopram tablet", "Dosage and Administration - MDD"),
        cautions=("QT considerations", "serotonergic interactions", "sexual dysfunction"),
        substitution_fit=("ansiedade / serotoninergico",),
        association_fit=(),
    ),
    MedicationStrategyEntry(
        name="Venlafaxina XR",
        drug_class="SNRI",
        targets=("humor / energia / antidepressivo", "ansiedade / serotoninergico"),
        usual_adult_range=(
            "MDD: start 75 mg once daily; 37.5 mg once daily may be used for "
            "4-7 days in some patients; max 225 mg/day."
        ),
        source=_citation("DM-VENLAFAXINE-ER", "DailyMed Venlafaxine hydrochloride extended-release", "Dosage and Administration"),
        cautions=("blood pressure", "withdrawal symptoms", "serotonergic interactions"),
        substitution_fit=("humor / energia / antidepressivo", "ansiedade / serotoninergico"),
        association_fit=(),
    ),
    MedicationStrategyEntry(
        name="Duloxetina",
        drug_class="SNRI",
        targets=("humor / energia / antidepressivo", "ansiedade / serotoninergico", "dor / somatico"),
        usual_adult_range=(
            "MDD: 40 mg/day as 20 mg twice daily, or 60 mg/day once daily "
            "or as 30 mg twice daily."
        ),
        source=_citation("DM-DULOXETINE", "DailyMed Duloxetine delayed-release capsule", "Dosage for Treatment of MDD"),
        cautions=("hepatic impairment", "severe renal impairment", "blood pressure", "serotonergic interactions"),
        substitution_fit=("humor / energia / antidepressivo", "dor / somatico"),
        association_fit=(),
    ),
    MedicationStrategyEntry(
        name="Bupropiona XL",
        drug_class="NDRI",
        targets=("humor / energia / antidepressivo", "energia / apatia / fadiga"),
        usual_adult_range="MDD: start 150 mg once daily; target 300 mg once daily.",
        source=_citation("DM-BUPROPION-XL", "DailyMed Wellbutrin XL", "Dosage for Major Depressive Disorder"),
        cautions=("seizure risk", "eating disorder contraindication", "activation/insomnia", "hypertension"),
        substitution_fit=("humor / energia / antidepressivo", "energia / apatia / fadiga"),
        association_fit=("humor / energia / antidepressivo", "energia / apatia / fadiga"),
    ),
    MedicationStrategyEntry(
        name="Mirtazapina",
        drug_class="NaSSA",
        targets=("sono / sedacao / ativacao", "humor / energia / antidepressivo"),
        usual_adult_range="MDD: start 15 mg nightly; max 45 mg/day.",
        source=_citation("DM-MIRTAZAPINE", "DailyMed Mirtazapine tablet", "Recommended Dosage"),
        cautions=("sedation", "weight gain", "metabolic monitoring"),
        substitution_fit=("sono / sedacao / ativacao",),
        association_fit=("sono / sedacao / ativacao",),
    ),
)


class MedicationStrategyTable:
    """Finds medication candidates from local structured entries."""

    def __init__(self, motor_repository: MotorTableRepository | None = None) -> None:
        self._motor_repository = motor_repository or MotorTableRepository()

    def find_current(self, medication_name: str) -> MedicationStrategyEntry | None:
        motor_entry = self._motor_repository.find_current(medication_name)
        if motor_entry:
            return self._to_strategy_entry(motor_entry)

        normalized = self._normalize(medication_name)
        for entry in MEDICATION_STRATEGY_TABLE:
            if self._normalize(entry.name) in normalized or normalized in self._normalize(entry.name):
                return entry
        return None

    def substitution_candidates(
        self,
        target: str,
        current_names: tuple[str, ...],
    ) -> tuple[MedicationStrategyEntry, ...]:
        motor_candidates = self._motor_repository.substitution_candidates(
            target=target,
            current_names=current_names,
        )
        if motor_candidates:
            current_classes = {
                entry.drug_class
                for name in current_names
                if (entry := self._motor_repository.find_current(name))
            }
            sorted_candidates = sorted(
                motor_candidates,
                key=lambda entry: (
                    entry.drug_class in current_classes,
                    self._candidate_priority(entry),
                ),
            )
            sorted_candidates = self._avoid_cross_class_noise(sorted_candidates, target)
            return tuple(self._to_strategy_entry(entry) for entry in sorted_candidates[:3])

        current = {self._normalize(name) for name in current_names}
        candidates = [
            entry
            for entry in MEDICATION_STRATEGY_TABLE
            if target in entry.substitution_fit and self._normalize(entry.name) not in current
        ]
        return tuple(candidates[:2])

    def association_candidates(
        self,
        target: str,
        current_names: tuple[str, ...],
    ) -> tuple[MedicationStrategyEntry, ...]:
        motor_candidates = self._motor_repository.association_candidates(
            target=target,
            current_names=current_names,
        )
        if motor_candidates:
            filtered_candidates = self._avoid_cross_class_noise(motor_candidates, target)
            return tuple(self._to_strategy_entry(entry) for entry in filtered_candidates[:3])

        current = {self._normalize(name) for name in current_names}
        candidates = [
            entry
            for entry in MEDICATION_STRATEGY_TABLE
            if target in entry.association_fit and self._normalize(entry.name) not in current
        ]
        return tuple(candidates[:2])

    def current_dose_target(
        self,
        medication_name: str,
    ) -> tuple[str, EvidenceCitationPayload | None]:
        entry = self.find_current(medication_name)
        if not entry:
            return (
                "Medicacao atual nao encontrada na tabela local; checar monografia antes de definir dose alvo.",
                None,
            )
        return entry.usual_adult_range, entry.source

    def _to_strategy_entry(self, entry: MotorTableEntry) -> MedicationStrategyEntry:
        targets = tuple(
            item.strip()
            for item in entry.symptom_targets.replace("/", ",").split(",")
            if item.strip()
        ) or (entry.motor_use or "alvo pendente",)
        cautions = tuple(
            item.strip()
            for item in entry.cautions.replace(";", ",").split(",")
            if item.strip()
        )
        substitution_fit = (
            "humor / energia / antidepressivo",
            "ansiedade / serotoninergico",
            "sono / sedacao / ativacao",
            "dor / somatico",
        )
        association_fit = substitution_fit if "associ" in self._normalize(entry.allowed_actions) else ()
        official_entry = next(
            (
                item
                for item in MEDICATION_STRATEGY_TABLE
                if self._normalize(item.name)
                == self._normalize(self._display_name(entry.entity))
            ),
            None,
        )
        return MedicationStrategyEntry(
            name=self._display_name(entry.entity),
            drug_class=entry.drug_class or "classe nao informada",
            targets=targets,
            usual_adult_range=(
                official_entry.usual_adult_range
                if official_entry
                else self._format_dose_range(entry.dose_range)
                or "Faixa informativa pendente na Tabela Motor."
            ),
            source=(
                official_entry.source
                if official_entry
                else entry.citation("Tabela Motor / dose-faixa informativa")
            ),
            cautions=cautions,
            substitution_fit=substitution_fit,
            association_fit=association_fit,
        )

    def _candidate_priority(self, entry: MotorTableEntry) -> int:
        normalized_class = self._normalize(entry.drug_class)
        if normalized_class == "snri":
            return 0
        if normalized_class in {"ndri", "nassa"}:
            return 1
        if normalized_class == "ssri":
            return 2
        return 3

    def _avoid_cross_class_noise(
        self,
        candidates: tuple[MotorTableEntry, ...] | list[MotorTableEntry],
        target: str,
    ) -> tuple[MotorTableEntry, ...]:
        normalized_target = self._normalize(target)
        if any(term in normalized_target for term in ("psicose", "mania", "bipolar")):
            return tuple(candidates)
        non_antipsychotic = tuple(
            entry
            for entry in candidates
            if "antipsicotico" not in self._normalize(entry.drug_class)
        )
        return non_antipsychotic or tuple(candidates)

    def _display_name(self, name: str) -> str:
        normalized = self._normalize(name)
        aliases = {
            "venlafaxina": "Venlafaxina XR",
            "bupropiona": "Bupropiona XL",
        }
        return aliases.get(normalized, name)

    def _format_dose_range(self, dose_range: str) -> str:
        if not dose_range or "mg" not in dose_range.lower() or " / " not in dose_range:
            return dose_range
        base = dose_range.replace("mg", "").strip()
        parts = [part.strip() for part in base.split("/") if part.strip()]
        return " / ".join(f"{part} mg" for part in parts)

    def _normalize(self, value: str) -> str:
        without_accents = normalize("NFKD", value.lower()).encode("ascii", "ignore")
        return without_accents.decode("ascii").replace(" ", "")
