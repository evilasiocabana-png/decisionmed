"""Canonical 51-topic coverage taxonomy for the WeMeds comparison audit."""

from __future__ import annotations

import csv
import unicodedata
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = PROJECT_ROOT / "knowledge_base" / "coverage" / "wemeds_psychiatry_coverage_matrix.csv"
EXPECTED_COUNTS = {"covered": 17, "partial": 13, "relevant_gap": 12, "contextual_only": 9}


@dataclass(frozen=True)
class ClinicalCoverageTopic:
    topic_id: str
    wemeds_topic: str
    canonical_context: str
    coverage_class: str
    runtime_scope: str
    priority: str
    source_status: str
    notes: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ClinicalCoverageMatch:
    input_context: str
    topic: ClinicalCoverageTopic | None

    def display_line(self) -> str:
        if self.topic is None:
            return f"Cobertura auditada: contexto explicito fora da matriz de 51 temas ({self.input_context or 'nao informado'})."
        return (
            f"Cobertura auditada: {self.topic.canonical_context}; classe {self.topic.coverage_class}; "
            f"status de fonte {self.topic.source_status}."
        )


class ClinicalCoverageMatrix:
    _ALIASES = {
        "agitacao ou psicose aguda": "PSYCHOSIS",
        "depressao com fadiga hipersonia baixa energia": "MAJOR_DEPRESSIVE_DISORDER",
        "depressao com insonia baixa ingestao perda de peso": "MAJOR_DEPRESSIVE_DISORDER",
        "depressao resistente": "MAJOR_DEPRESSIVE_DISORDER",
        "esquizofrenia e transtornos psicoticos": "SCHIZOPHRENIA",
        "esquizofrenia resistente": "SCHIZOPHRENIA",
        "toc resistente": "OBSESSIVE_COMPULSIVE_DISORDER",
        "tabagismo": "NICOTINE_USE_DISORDER",
        "transtorno bipolar antidepressivo isolado": "BIPOLAR_DISORDER",
        "transtorno bipolar episodio depressivo": "BIPOLAR_DISORDER",
        "transtorno bipolar mania hipomania": "BIPOLAR_DISORDER",
        "transtorno bipolar manutencao": "BIPOLAR_DISORDER",
    }

    def __init__(self, csv_path: Path | None = None) -> None:
        self._csv_path = csv_path or DEFAULT_PATH
        self._topics: tuple[ClinicalCoverageTopic, ...] | None = None

    def topics(self) -> tuple[ClinicalCoverageTopic, ...]:
        if self._topics is None:
            with self._csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
                self._topics = tuple(ClinicalCoverageTopic(**row) for row in csv.DictReader(handle))
        return self._topics

    def summary(self) -> dict[str, int]:
        counts = Counter(item.coverage_class for item in self.topics())
        return {key: counts.get(key, 0) for key in EXPECTED_COUNTS}

    def validation_issues(self) -> tuple[str, ...]:
        issues: list[str] = []
        topics = self.topics()
        if len(topics) != 51:
            issues.append(f"topic_count:{len(topics)}")
        if len({item.topic_id for item in topics}) != len(topics):
            issues.append("duplicate_topic_id")
        if len({item.canonical_context for item in topics}) != len(topics):
            issues.append("duplicate_canonical_context")
        if self.summary() != EXPECTED_COUNTS:
            issues.append(f"classification_counts:{self.summary()}")
        return tuple(issues)

    def match(self, explicit_context: str) -> ClinicalCoverageMatch:
        normalized = self._normalize(explicit_context)
        canonical_alias = self._ALIASES.get(normalized, "")
        for topic in self.topics():
            if normalized in {
                self._normalize(topic.wemeds_topic),
                self._normalize(topic.canonical_context),
            } or topic.canonical_context == canonical_alias:
                return ClinicalCoverageMatch(explicit_context, topic)
        return ClinicalCoverageMatch(explicit_context, None)

    def as_payload(self) -> dict[str, object]:
        return {
            "summary": self.summary(),
            "topic_count": len(self.topics()),
            "validation_issues": self.validation_issues(),
            "topics": [item.to_dict() for item in self.topics()],
        }

    @staticmethod
    def _normalize(value: str) -> str:
        text = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode("ascii")
        return " ".join(text.lower().replace("/", " ").replace("-", " ").split())
