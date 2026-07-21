"""Source-governed, non-prescriptive monitoring knowledge.

The service publishes only monitoring rules that passed the scientific,
editorial and runtime gates defined by ADR 0051. It does not diagnose, prescribe,
change medication or calculate a dose/taper.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
from unicodedata import normalize


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_THEORY_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "theory_to_practice_matrix.csv"
)
DEFAULT_RUNTIME_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "monitoring_runtime_rules.csv"
)
DEFAULT_MEDICATION_MATRIX_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "pharmacological_decision_matrix.csv"
)

MONITORING_RULE_IDS = ("TPC-005", "TPC-012", "TPC-014", "TPC-015")
ANTIDEPRESSANT_CLASS_MARKERS = (
    "antidepressivo",
    "ssri",
    "snri",
    "ndri",
    "triciclico",
    "tetraciclico",
    "sari",
    "nassa",
)


class MedicationLike(Protocol):
    """Minimum medication shape required by monitoring trigger matching."""

    name: str


@dataclass(frozen=True)
class MonitoringEvidence:
    rule_id: str
    source_id: str
    section: str
    url: str
    boundary: str

    def display_line(self) -> str:
        return (
            f"{self.rule_id}: {self.source_id}, {self.section}. "
            f"Limite: {self.boundary}. Fonte: {self.url}"
        )


@dataclass(frozen=True)
class MonitoringGovernanceAssessment:
    generic_targets: tuple[str, ...]
    specific_targets: tuple[str, ...]
    runtime_eligible_rule_ids: tuple[str, ...]
    activated_rule_ids: tuple[str, ...]
    pending_runtime_rule_ids: tuple[str, ...]
    evidence: tuple[MonitoringEvidence, ...]

    @property
    def targets(self) -> tuple[str, ...]:
        """Return generic and context-activated targets without duplicates."""
        return tuple(dict.fromkeys((*self.generic_targets, *self.specific_targets)))

    def display_lines(self) -> tuple[str, ...]:
        activated = ", ".join(self.activated_rule_ids) or "nenhuma neste contexto"
        return (
            f"Monitorizacao estrutural generica: {', '.join(self.generic_targets)}.",
            f"Regras especificas publicadas: {len(self.runtime_eligible_rule_ids)}.",
            f"Regras acionadas pelo estado informado: {activated}.",
            f"Regras de monitorizacao ainda nao promovidas: {', '.join(self.pending_runtime_rule_ids) or 'nenhuma'}.",
            *(item.display_line() for item in self.evidence),
            (
                "Limite operacional: checklist informativo para revisao medica; "
                "nao diagnostica, prescreve, altera medicamento ou calcula dose/retirada."
            ),
        )


@dataclass(frozen=True)
class _PublishedMonitoringRule:
    rule_id: str
    trigger_type: str
    trigger_value: str
    targets: tuple[str, ...]
    evidence: MonitoringEvidence


class MonitoringGovernanceService:
    """Apply only dual-gated published monitoring prompts to patient state."""

    def __init__(
        self,
        theory_path: Path | None = None,
        runtime_path: Path | None = None,
        medication_matrix_path: Path | None = None,
    ) -> None:
        self._theory_path = theory_path or DEFAULT_THEORY_PATH
        self._runtime_path = runtime_path or DEFAULT_RUNTIME_PATH
        self._medication_matrix_path = (
            medication_matrix_path or DEFAULT_MEDICATION_MATRIX_PATH
        )

    def assess(
        self,
        *,
        symptoms: tuple[str, ...],
        action: str = "",
        medications: tuple[MedicationLike, ...] = (),
    ) -> MonitoringGovernanceAssessment:
        generic = ["resposta clinica", "adesao", "tolerabilidade", "prejuizo funcional"]
        if "Insonia inicial" in symptoms or "Insonia terminal" in symptoms:
            generic.append("sono")
        if "Ansiedade" in symptoms:
            generic.append("ansiedade")

        theory = {row.get("concern_id", ""): row for row in self._read(self._theory_path)}
        runtime_rows = {
            row.get("rule_id", ""): row for row in self._read(self._runtime_path)
        }
        eligible_ids = tuple(
            rule_id
            for rule_id in MONITORING_RULE_IDS
            if self._is_dual_gate_eligible(theory.get(rule_id), runtime_rows.get(rule_id))
        )
        pending_ids = tuple(
            rule_id for rule_id in MONITORING_RULE_IDS if rule_id not in eligible_ids
        )
        classes = self._medication_classes()
        names = tuple(self._normalize(item.name) for item in medications if item.name)
        activated: list[_PublishedMonitoringRule] = []
        for rule_id in eligible_ids:
            row = runtime_rows[rule_id]
            rule = self._published_rule(row)
            if self._matches(rule, action=action, names=names, classes=classes):
                activated.append(rule)

        return MonitoringGovernanceAssessment(
            generic_targets=tuple(dict.fromkeys(generic)),
            specific_targets=tuple(
                dict.fromkeys(target for rule in activated for target in rule.targets)
            ),
            runtime_eligible_rule_ids=eligible_ids,
            activated_rule_ids=tuple(rule.rule_id for rule in activated),
            pending_runtime_rule_ids=pending_ids,
            evidence=tuple(rule.evidence for rule in activated),
        )

    @staticmethod
    def _is_dual_gate_eligible(
        theory: dict[str, str] | None, runtime: dict[str, str] | None
    ) -> bool:
        if not theory or not runtime:
            return False
        return all(
            (
                theory.get("runtime_eligible", "").strip().lower() == "true",
                theory.get("validation_status", "") == "official_guideline_validated",
                runtime.get("runtime_eligible", "").strip().lower() == "true",
                runtime.get("scientific_review_status", "")
                == "verified_against_official_guideline",
                runtime.get("editorial_review_status", "")
                == "approved_for_non_prescriptive_runtime",
                runtime.get("publication_status", "")
                == "published_monitoring_knowledge_object",
                bool(runtime.get("official_source_id", "")),
                bool(runtime.get("official_source_section", "")),
                runtime.get("official_source_url", "").startswith("https://www.nice.org.uk/"),
            )
        )

    @staticmethod
    def _published_rule(row: dict[str, str]) -> _PublishedMonitoringRule:
        return _PublishedMonitoringRule(
            rule_id=row["rule_id"],
            trigger_type=row["trigger_type"],
            trigger_value=row["trigger_value"],
            targets=tuple(
                item.strip() for item in row["monitoring_targets"].split("|") if item.strip()
            ),
            evidence=MonitoringEvidence(
                rule_id=row["rule_id"],
                source_id=row["official_source_id"],
                section=row["official_source_section"],
                url=row["official_source_url"],
                boundary=row["boundary"],
            ),
        )

    def _matches(
        self,
        rule: _PublishedMonitoringRule,
        *,
        action: str,
        names: tuple[str, ...],
        classes: dict[str, str],
    ) -> bool:
        medication_classes = tuple(classes.get(name, "") for name in names)
        if rule.trigger_type == "medication_name":
            value = self._normalize(rule.trigger_value)
            return any(value in name for name in names)
        if rule.trigger_type == "medication_class":
            value = self._normalize(rule.trigger_value)
            return any(value in item for item in medication_classes)
        if rule.trigger_type == "action_and_class":
            expected_action, expected_class = rule.trigger_value.split("|", 1)
            return action == expected_action and self._has_category(
                expected_class, medication_classes
            )
        return False

    def _has_category(
        self, expected: str, medication_classes: tuple[str, ...]
    ) -> bool:
        expected = self._normalize(expected)
        if expected == "antidepressant":
            return any(
                marker in item
                for item in medication_classes
                for marker in ANTIDEPRESSANT_CLASS_MARKERS
            )
        return any(expected in item for item in medication_classes)

    def _medication_classes(self) -> dict[str, str]:
        return {
            self._normalize(row.get("drug_name", "")): self._normalize(
                row.get("drug_class", "")
            )
            for row in self._read(self._medication_matrix_path)
            if row.get("drug_name", "")
        }

    @staticmethod
    def _read(path: Path) -> list[dict[str, str]]:
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    @staticmethod
    def _normalize(value: str) -> str:
        without_accents = normalize("NFKD", str(value).lower()).encode("ascii", "ignore")
        return " ".join(without_accents.decode("ascii").replace("/", " ").split())
