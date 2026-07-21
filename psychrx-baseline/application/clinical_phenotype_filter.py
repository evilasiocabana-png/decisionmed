"""Clinical phenotype detection for the local PsychRx motor.

The filter organizes the presentation as a syndrome/fenotype for decision
support. It deliberately does not convert phenotype into a definitive diagnosis.
"""

from __future__ import annotations

from dataclasses import dataclass
from unicodedata import normalize


@dataclass(frozen=True)
class PhenotypeAssessment:
    """Syndromic assessment derived from structured consultation fields."""

    primary_phenotype: str
    secondary_phenotypes: tuple[str, ...]
    supporting_features: tuple[str, ...]
    confidence: str
    warnings: tuple[str, ...] = ()

    def display_lines(self) -> tuple[str, ...]:
        """Return compact UI/audit lines."""
        base = [
            f"Fenotipo principal: {self.primary_phenotype}",
            f"Secundarios: {', '.join(self.secondary_phenotypes) if self.secondary_phenotypes else 'nenhum'}",
            f"Confianca: {self.confidence}",
        ]
        if self.supporting_features:
            base.append(f"Sustentado por: {', '.join(self.supporting_features[:5])}")
        base.extend(f"Aviso: {item}" for item in self.warnings)
        return tuple(base)


class ClinicalPhenotypeFilter:
    """Detect syndromic phenotype without asserting a diagnosis."""

    PHENOTYPES = {
        "DEPRESSIVE_SYNDROME": (
            "depress",
            "humor deprimido",
            "anedonia",
            "fadiga",
            "baixa energia",
            "lentificacao",
        ),
        "ANXIOUS_SYNDROME": ("ansiedade", "ansioso", "tensao", "panico", "fobia"),
        "MANIFORM_SYNDROME": (
            "mania",
            "hipomania",
            "humor elevado",
            "fala pressionada",
            "ativacao",
            "bipolar",
        ),
        "PSYCHOTIC_SYNDROME": (
            "psicose",
            "psicotico",
            "delirio",
            "alucin",
            "desorganiz",
        ),
        "OBSESSIVE_COMPULSIVE_SYNDROME": ("toc", "compuls", "obsess"),
        "AGITATION_SYNDROME": ("agitacao", "irritabilidade", "agressividade", "impuls"),
        "INSOMNIA_PREDOMINANT": ("insonia", "sono", "despertar"),
        "COGNITIVE_SYNDROME": ("cognicao", "concentracao", "memoria"),
        "SUBSTANCE_WITHDRAWAL_OR_USE_SYNDROME": (
            "substancia",
            "alcool",
            "opioide",
            "abstinencia",
        ),
    }

    def assess(
        self,
        *,
        clinical_presentation: str = "",
        diagnostic_context: str = "",
        symptoms: tuple[str, ...] = (),
        observed_signs: tuple[str, ...] = (),
        pharmacological_profile: tuple[str, ...] = (),
        safety: dict[str, str] | None = None,
    ) -> PhenotypeAssessment:
        """Return the main and secondary phenotype from available data."""
        safety = safety or {}
        source_items = (
            clinical_presentation,
            diagnostic_context,
            *symptoms,
            *observed_signs,
            *pharmacological_profile,
        )
        text = self._normalize(" ".join(source_items))
        scores: dict[str, int] = {}
        features: dict[str, list[str]] = {}
        for phenotype, terms in self.PHENOTYPES.items():
            for term in terms:
                normalized = self._normalize(term)
                if normalized and normalized in text:
                    scores[phenotype] = scores.get(phenotype, 0) + 1
                    features.setdefault(phenotype, []).append(term)

        if str(safety.get("mania_or_hypomania", "")).lower() == "presente":
            scores["MANIFORM_SYNDROME"] = scores.get("MANIFORM_SYNDROME", 0) + 3
            features.setdefault("MANIFORM_SYNDROME", []).append("seguranca: mania/hipomania presente")
        if str(safety.get("substances", "")).lower() == "presente":
            scores["SUBSTANCE_WITHDRAWAL_OR_USE_SYNDROME"] = (
                scores.get("SUBSTANCE_WITHDRAWAL_OR_USE_SYNDROME", 0) + 2
            )
            features.setdefault("SUBSTANCE_WITHDRAWAL_OR_USE_SYNDROME", []).append(
                "seguranca: uso de substancias presente"
            )

        if not scores:
            return PhenotypeAssessment(
                primary_phenotype="UNSPECIFIED_OR_INSUFFICIENT_DATA",
                secondary_phenotypes=(),
                supporting_features=(),
                confidence="low",
                warnings=("dados insuficientes para ranking farmacologico confiavel",),
            )

        ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        primary = ordered[0][0]
        secondary = tuple(item[0] for item in ordered[1:] if item[1] > 0)
        warnings: list[str] = []
        if primary == "MANIFORM_SYNDROME" or "MANIFORM_SYNDROME" in secondary:
            warnings.append(
                "nao apresentar antidepressivo em monoterapia no ranking principal sem esclarecer bipolaridade/mania"
            )
        if primary == "INSOMNIA_PREDOMINANT" and not {
            "PSYCHOTIC_SYNDROME",
            "MANIFORM_SYNDROME",
        }.intersection(secondary):
            warnings.append(
                "insonia isolada nao deve ser convertida automaticamente em indicacao de antipsicotico"
            )
        confidence = "high" if ordered[0][1] >= 3 else "moderate"
        return PhenotypeAssessment(
            primary_phenotype=primary,
            secondary_phenotypes=secondary,
            supporting_features=tuple(dict.fromkeys(features.get(primary, []))),
            confidence=confidence,
            warnings=tuple(warnings),
        )

    @staticmethod
    def _normalize(value: str) -> str:
        text = normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii")
        return " ".join(text.lower().replace("/", " ").replace("-", " ").split())
