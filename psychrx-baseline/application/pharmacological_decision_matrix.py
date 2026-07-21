"""Pharmacological profile ranking for the local PsychRx app.

This module consumes a curated local decision matrix. It does not prescribe,
does not choose a medication autonomously, and does not replace clinical
judgment. It ranks options for physician review based on a desired
pharmacological profile and explicit cautions.
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
    / "pharmacological_decision_matrix.csv"
)

AXIS_LABELS = {
    "energy": "energia / fadiga / anedonia",
    "anxiety": "ansiedade / tensão / obsessividade",
    "sleep": "sono / insônia / sedação",
    "pain": "dor / sintomas somáticos",
    "weight_neutral": "baixo impacto em peso/metabolismo",
    "libido": "preservação de libido/função sexual",
    "mood_stabilization": "estabilização do humor",
    "psychosis": "sintomas psicóticos/desorganização",
    "impulsivity": "impulsividade/agitação",
}


@dataclass(frozen=True)
class PharmacologicalDecisionOption:
    """One ranked medication option for physician review."""

    drug_id: str
    name: str
    drug_class: str
    score: int
    matched_targets: tuple[str, ...]
    caution_hits: tuple[str, ...]
    reason: str
    source_tabs: str
    evidence_status: str
    citation: EvidenceCitationPayload


@dataclass(frozen=True)
class PharmacologicalDecisionRow:
    """One row from the local pharmacological decision matrix."""

    drug_id: str
    drug_name: str
    drug_class: str
    therapeutic_targets: tuple[str, ...]
    fit_energy: int
    fit_anxiety: int
    fit_sleep: int
    fit_pain: int
    fit_weight_neutral: int
    fit_libido: int
    fit_mood_stabilization: int
    fit_psychosis: int
    fit_impulsivity: int
    cautions: tuple[str, ...]
    preferred_contexts: tuple[str, ...]
    source_tabs: str
    status: str

    def citation(self) -> EvidenceCitationPayload:
        """Return a traceable local table citation."""
        return EvidenceCitationPayload(
            source_id=f"PSYCHRX-PHARMACOLOGICAL-MATRIX-{self.drug_id}",
            title="PsychRx Pharmacological Decision Matrix",
            organization="PsychRx",
            year="2026",
            section=f"pharmacological_decision_matrix.csv / {self.drug_name}",
            excerpt_anchor=self.drug_id,
            evidence_type="curated_local_decision_matrix",
            quality=self.status or "status_not_recorded",
            applicability="physician_review_only",
            limitations=(
                f"Status da linha: {self.status or 'nao informado'}. "
                "Matriz local de suporte a decisao; requer revisao medica, "
                "bula, diretriz, contraindicoes e contexto individual."
            ),
        )


class PharmacologicalDecisionMatrix:
    """Scores local medication rows against a desired clinical profile."""

    def __init__(self, matrix_path: Path | None = None) -> None:
        self._matrix_path = matrix_path or DEFAULT_MATRIX_PATH
        self._rows: tuple[PharmacologicalDecisionRow, ...] | None = None

    def rank(
        self,
        *,
        presentation: str = "",
        symptoms: tuple[str, ...] = (),
        pharmacological_profile: tuple[str, ...] = (),
        impairment_domains: tuple[str, ...] = (),
        restrictions: tuple[str, ...] = (),
        current_medications: tuple[str, ...] = (),
        limit: int = 5,
    ) -> tuple[PharmacologicalDecisionOption, ...]:
        """Return ranked options for physician review."""
        desired_axes = self._desired_axes(
            presentation=presentation,
            symptoms=symptoms,
            pharmacological_profile=pharmacological_profile,
            impairment_domains=impairment_domains,
        )
        current = {self._normalize(name) for name in current_medications if name}
        scored: list[PharmacologicalDecisionOption] = []
        for row in self.rows():
            if self._normalize(row.drug_name) in current:
                continue
            score, matched_targets = self._score_row(row, desired_axes)
            caution_hits = self._caution_hits(row, restrictions)
            score -= len(caution_hits) * 2
            if score <= 0 and not matched_targets:
                continue
            display_targets = tuple(
                AXIS_LABELS.get(target, target) for target in matched_targets
            )
            scored.append(
                PharmacologicalDecisionOption(
                    drug_id=row.drug_id,
                    name=row.drug_name,
                    drug_class=row.drug_class,
                    score=score,
                    matched_targets=display_targets,
                    caution_hits=caution_hits,
                    reason=self._reason(row, display_targets, caution_hits),
                    source_tabs=row.source_tabs,
                    evidence_status=row.status,
                    citation=row.citation(),
                )
            )
        return tuple(
            sorted(scored, key=lambda option: option.score, reverse=True)[:limit]
        )

    def rows(self) -> tuple[PharmacologicalDecisionRow, ...]:
        """Return all local matrix rows."""
        if self._rows is None:
            self._rows = self._load_rows()
        return self._rows

    def _load_rows(self) -> tuple[PharmacologicalDecisionRow, ...]:
        if not self._matrix_path.exists():
            return ()
        with self._matrix_path.open("r", encoding="utf-8", newline="") as handle:
            rows = []
            for item in csv.DictReader(handle):
                rows.append(
                    PharmacologicalDecisionRow(
                        drug_id=item["drug_id"],
                        drug_name=item["drug_name"],
                        drug_class=item["drug_class"],
                        therapeutic_targets=self._split(item["therapeutic_targets"]),
                        fit_energy=self._to_int(item["fit_energy"]),
                        fit_anxiety=self._to_int(item["fit_anxiety"]),
                        fit_sleep=self._to_int(item["fit_sleep"]),
                        fit_pain=self._to_int(item["fit_pain"]),
                        fit_weight_neutral=self._to_int(item["fit_weight_neutral"]),
                        fit_libido=self._to_int(item["fit_libido"]),
                        fit_mood_stabilization=self._to_int(
                            item["fit_mood_stabilization"]
                        ),
                        fit_psychosis=self._to_int(item["fit_psychosis"]),
                        fit_impulsivity=self._to_int(item["fit_impulsivity"]),
                        cautions=self._split(item["cautions"]),
                        preferred_contexts=self._split(item["preferred_contexts"]),
                        source_tabs=item["source_tabs"],
                        status=item["status"],
                    )
                )
            return tuple(rows)

    def _desired_axes(
        self,
        *,
        presentation: str,
        symptoms: tuple[str, ...],
        pharmacological_profile: tuple[str, ...],
        impairment_domains: tuple[str, ...],
    ) -> tuple[str, ...]:
        text = self._normalize(
            " ".join((presentation, *symptoms, *pharmacological_profile, *impairment_domains))
        )
        axes: list[str] = []
        if any(term in text for term in ("energia", "fadiga", "apatia", "anedonia", "funcional")):
            axes.append("energy")
        if any(term in text for term in ("ansiedade", "panico", "tensao", "toc", "trauma")):
            axes.append("anxiety")
        if any(term in text for term in ("sono", "insonia", "sedacao", "despertares")):
            axes.append("sleep")
        if any(term in text for term in ("dor", "somatica", "somatico")):
            axes.append("pain")
        if any(term in text for term in ("peso", "obesidade", "diabetes", "metabolico")):
            axes.append("weight_neutral")
        if any(term in text for term in ("libido", "sexual")):
            axes.append("libido")
        if any(term in text for term in ("bipolar", "mania", "hipomania", "estabilizacao", "recaida")):
            axes.append("mood_stabilization")
        if any(term in text for term in ("psicose", "psicotica", "alucin", "delir", "desorganiz")):
            axes.append("psychosis")
        if any(
            term in text
            for term in (
                "impuls",
                "agitacao",
                "irritabilidade",
                "agressividade",
                "alcool",
                "dependencia",
                "substancia",
                "fissura",
                "recaida",
                "compulsao",
            )
        ):
            axes.append("impulsivity")
        return tuple(dict.fromkeys(axes)) or ("anxiety", "energy")

    def _score_row(
        self, row: PharmacologicalDecisionRow, axes: tuple[str, ...]
    ) -> tuple[int, tuple[str, ...]]:
        score = 0
        matched: list[str] = []
        for axis in axes:
            value = getattr(row, f"fit_{axis}")
            if value > 0:
                score += value
                matched.append(axis)
        return score, tuple(matched)

    def _caution_hits(
        self, row: PharmacologicalDecisionRow, restrictions: tuple[str, ...]
    ) -> tuple[str, ...]:
        text = self._normalize(" ".join(row.cautions))
        hits = []
        for restriction in restrictions:
            normalized = self._normalize(restriction)
            if not normalized:
                continue
            if "obesidade" in normalized or "diabetes" in normalized:
                if "peso" in text or "metabolico" in text:
                    hits.append(restriction)
            elif "sexual" in normalized:
                if "sexual" in text or "libido" in text:
                    hits.append(restriction)
            elif "qt" in normalized and "qt" in text:
                hits.append(restriction)
            elif "epilepsia" in normalized and "convulsao" in text:
                hits.append(restriction)
            elif "gestacao" in normalized and "gestacao" in text:
                hits.append(restriction)
            elif "renal" in normalized and "renal" in text:
                hits.append(restriction)
            elif "hepatica" in normalized and "hepatico" in text:
                hits.append(restriction)
        return tuple(dict.fromkeys(hits))

    def _reason(
        self,
        row: PharmacologicalDecisionRow,
        matched_targets: tuple[str, ...],
        caution_hits: tuple[str, ...],
    ) -> str:
        targets = ", ".join(matched_targets) if matched_targets else "perfil parcial"
        caution = (
            f" Penalizacao por cautelas: {', '.join(caution_hits)}."
            if caution_hits
            else " Sem cautela selecionada contra esse perfil."
        )
        return (
            f"{row.drug_name} pontuou por {targets}. Classe: {row.drug_class}. "
            f"Alvos da matriz: {', '.join(row.therapeutic_targets)}.{caution} "
            f"Fonte local: {row.source_tabs}."
        )

    def _split(self, value: str) -> tuple[str, ...]:
        return tuple(part.strip() for part in value.split("|") if part.strip())

    def _to_int(self, value: str) -> int:
        try:
            return int(value)
        except ValueError:
            return 0

    def _normalize(self, value: str) -> str:
        without_accents = normalize("NFKD", value.lower()).encode("ascii", "ignore")
        normalized = without_accents.decode("ascii")
        return " ".join(normalized.replace("/", " ").replace("|", " ").split())
