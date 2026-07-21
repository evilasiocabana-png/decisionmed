"""Disease/context eligibility filter for the local PsychRx motor."""

from __future__ import annotations

from dataclasses import dataclass
from unicodedata import normalize

from application.clinical_phenotype_filter import PhenotypeAssessment
from application.medication_disease_use_table import MedicationDiseaseUse, MedicationDiseaseUseTable


@dataclass(frozen=True)
class MedicationEligibility:
    """Eligibility decision before final ranking display."""

    medication_name: str
    eligible: bool
    therapeutic_role: str
    status: str
    matched_context: str
    exclusion_reason: str = ""
    penalty: int = 0
    evidence_status: str = ""
    source_reference: str = ""

    def display_line(self) -> str:
        """Return a compact audit/display line."""
        verdict = "elegivel" if self.eligible else f"excluido: {self.exclusion_reason}"
        context = self.matched_context or "sem contexto mapeado"
        source = f" Fonte: {self.source_reference}." if self.source_reference else ""
        evidence = f" Revisao: {self.evidence_status or 'nao informada'}."
        return (
            f"{self.medication_name}: {verdict}; papel {self.therapeutic_role or 'nao mapeado'}; "
            f"contexto {context}; status {self.status or 'nao mapeado'}.{evidence}{source}"
        )


class DiseaseUseFilter:
    """Apply disease/phenotype role rules before medication candidates are shown."""

    NOT_RECOMMENDED_MARKERS = ("nao_recomendado", "nao_ranking", "nao_tratamento")
    RESTRICTED_MARKERS = ("restrito", "bloquear")
    OFF_LABEL_MARKERS = ("off_label",)
    LIMITED_MARKERS = ("evidencia_limitada", "contextual")
    AUGMENT_ROLES = ("potencializacao", "adjuvante", "associacao")
    SHORT_TERM_ROLES = (
        "curto_prazo",
        "resgate",
        "ponte_terapeutica",
        "sintomatico",
        "temporario",
    )
    PRIMARY_ROLES = (
        "tratamento_principal",
        "tratamento_ansiedade",
        "tratamento_toc",
        "tratamento_depressao",
        "tratamento_mania",
        "tratamento_antipsicotico",
        "manejo_agitacao",
        "tratamento_dor",
        "tratamento_dependencia",
        "cessacao_tabagismo",
    )
    MAINTENANCE_ROLES = ("manutencao", "prevencao")
    ANTIDEPRESSANT_CLASSES = (
        "ssri",
        "snri",
        "ndri",
        "triciclico",
        "maoi",
        "nassa",
        "sari",
        "antidepressivo",
        "tetraciclico",
    )

    def __init__(self, disease_use_table: MedicationDiseaseUseTable | None = None) -> None:
        self._table = disease_use_table or MedicationDiseaseUseTable()

    def filter_ranked_options(
        self,
        ranked_options,
        *,
        diagnostic_context: str,
        strategy: str,
        phenotype: PhenotypeAssessment,
    ):
        """Return ranked options filtered by disease/context eligibility."""
        eligibilities: list[MedicationEligibility] = []
        kept = []
        for option in ranked_options:
            eligibility = self.evaluate_option(
                medication_name=option.name,
                drug_class=getattr(option, "drug_class", ""),
                diagnostic_context=diagnostic_context,
                strategy=strategy,
                phenotype=phenotype,
            )
            eligibilities.append(eligibility)
            if eligibility.eligible:
                kept.append((option, eligibility.penalty))

        if kept:
            reordered = sorted(kept, key=lambda item: item[0].score - item[1], reverse=True)
            return tuple(item[0] for item in reordered), tuple(eligibilities)
        return (), tuple(eligibilities)

    def evaluate_option(
        self,
        *,
        medication_name: str,
        drug_class: str,
        diagnostic_context: str,
        strategy: str,
        phenotype: PhenotypeAssessment,
    ) -> MedicationEligibility:
        """Evaluate one medication against diagnosis/phenotype and strategy."""
        uses = self._table.all_uses_for(medication_name)
        if self._blocks_antidepressant_monotherapy(drug_class, strategy, phenotype):
            return MedicationEligibility(
                medication_name=medication_name,
                eligible=False,
                therapeutic_role="NOT_RECOMMENDED",
                status="blocked_by_phenotype",
                matched_context=phenotype.primary_phenotype,
                exclusion_reason="antidepressivo em monoterapia bloqueado diante de fenotipo maniforme/suspeita bipolar",
                evidence_status="phenotype_safety_rule",
            )
        if not uses:
            return MedicationEligibility(
                medication_name=medication_name,
                eligible=False,
                therapeutic_role="NO_MAPPING",
                status="NO_MAPPING",
                matched_context="",
                exclusion_reason="sem mapeamento de uso por doenca/quadro",
                evidence_status="no_mapping",
            )

        contexts = self._target_contexts(diagnostic_context, phenotype)
        matched = self._matching_uses(uses, contexts) or self._fallback_profile_uses(uses, phenotype)
        if not matched:
            return MedicationEligibility(
                medication_name=medication_name,
                eligible=False,
                therapeutic_role="NO_MAPPING",
                status="NO_MAPPING",
                matched_context=", ".join(contexts[:3]),
                exclusion_reason="sem papel terapeutico mapeado para o diagnostico ou fenotipo atual",
                evidence_status="no_context_mapping",
            )
        return self._eligibility_from_best_use(medication_name, matched, strategy)

    def summary_for(
        self,
        medication_name: str,
        *,
        diagnostic_context: str,
        phenotype: PhenotypeAssessment,
        limit: int = 4,
    ) -> tuple[str, ...]:
        """Return context-filtered disease/phenotype use lines."""
        uses = self._table.all_uses_for(medication_name)
        contexts = self._target_contexts(diagnostic_context, phenotype)
        matched = self._matching_uses(uses, contexts) or self._fallback_profile_uses(uses, phenotype)
        selected = matched or uses[:limit]
        if not selected:
            return (f"{medication_name or 'Medicamento'}: uso por doenca/quadro nao cadastrado.",)
        if self._is_diagnostic_uncertain(diagnostic_context):
            return tuple(
                self._phenotype_display_line(item, phenotype)
                for item in selected[:limit]
            )
        return tuple(item.display_line() for item in selected[:limit])

    def _eligibility_from_best_use(
        self,
        medication_name: str,
        uses: tuple[MedicationDiseaseUse, ...],
        strategy: str,
    ) -> MedicationEligibility:
        hard_blocks = [item for item in uses if self._is_hard_block(item)]
        if hard_blocks:
            block = hard_blocks[0]
            return MedicationEligibility(
                medication_name=medication_name,
                eligible=False,
                therapeutic_role=self._role_category(block.role),
                status=self._status_category(block.status),
                matched_context=block.disease_or_context,
                exclusion_reason="uso nao recomendado/restrito para o contexto atual",
                evidence_status=block.review_status,
                source_reference=block.source_reference,
            )
        compatible = [item for item in uses if self._role_compatible(item.role, strategy) and not self._is_hard_block(item)]
        if not compatible:
            block = uses[0]
            reason = "papel terapeutico incompativel com a estrategia antes do ranking"
            if self._is_hard_block(block):
                reason = "uso nao recomendado/restrito para o contexto atual"
            return MedicationEligibility(
                medication_name=medication_name,
                eligible=False,
                therapeutic_role=self._role_category(block.role),
                status=self._status_category(block.status),
                matched_context=block.disease_or_context,
                exclusion_reason=reason,
                evidence_status=block.review_status,
                source_reference=block.source_reference,
            )
        best = compatible[0]
        penalty = 0
        if self._contains_any(best.status, self.OFF_LABEL_MARKERS):
            penalty += 3
        if self._contains_any(best.status, self.LIMITED_MARKERS):
            penalty += 2
        if self._contains_any(best.role, self.SHORT_TERM_ROLES):
            penalty += 4
        return MedicationEligibility(
            medication_name=medication_name,
            eligible=True,
            therapeutic_role=self._role_category(best.role),
            status=self._status_category(best.status),
            matched_context=best.disease_or_context,
            penalty=penalty,
            evidence_status=best.review_status,
            source_reference=best.source_reference,
        )

    def _target_contexts(
        self, diagnostic_context: str, phenotype: PhenotypeAssessment
    ) -> tuple[str, ...]:
        diagnosis = self._normalize(diagnostic_context)
        contexts: list[str] = []
        if diagnosis and not self._is_diagnostic_uncertain(diagnostic_context):
            contexts.append(diagnostic_context)
            if "depress" in diagnosis:
                contexts.append("Transtorno depressivo maior")
            if "ansiedade" in diagnosis:
                contexts.extend(("Transtorno de ansiedade generalizada", "Transtorno do panico"))
            if "bipolar" in diagnosis:
                contexts.extend(
                    (
                        "Transtorno bipolar - antidepressivo isolado",
                        "Transtorno bipolar - mania/hipomania",
                        "Transtorno bipolar - episodio depressivo",
                        "Transtorno bipolar - manutencao",
                    )
                )
            if "psicose" in diagnosis or "psicot" in diagnosis:
                contexts.extend(("Esquizofrenia e transtornos psicoticos", "Agitacao ou psicose aguda"))
            if "tdah" in diagnosis:
                contexts.append("TDAH")

        phenotype_contexts = {
            "DEPRESSIVE_SYNDROME": (
                "Transtorno depressivo maior",
                "Depressao com fadiga/hipersonia/baixa energia",
                "Depressao com insonia/baixa ingestao/perda de peso",
            ),
            "ANXIOUS_SYNDROME": (
                "Transtorno de ansiedade generalizada",
                "Transtorno do panico",
                "Ansiedade social",
            ),
            "MANIFORM_SYNDROME": (
                "Transtorno bipolar - antidepressivo isolado",
                "Transtorno bipolar - mania/hipomania",
            ),
            "PSYCHOTIC_SYNDROME": (
                "Esquizofrenia e transtornos psicoticos",
                "Agitacao ou psicose aguda",
            ),
            "OBSESSIVE_COMPULSIVE_SYNDROME": ("Transtorno obsessivo-compulsivo", "TOC resistente"),
            "AGITATION_SYNDROME": ("Agitacao ou psicose aguda",),
            "INSOMNIA_PREDOMINANT": ("Insonia",),
            "SUBSTANCE_WITHDRAWAL_OR_USE_SYNDROME": (
                "Transtorno por uso de alcool",
                "Transtorno por uso de opioides",
                "Tabagismo",
            ),
        }
        contexts.extend(phenotype_contexts.get(phenotype.primary_phenotype, ()))
        for secondary in phenotype.secondary_phenotypes:
            contexts.extend(phenotype_contexts.get(secondary, ()))
        return tuple(dict.fromkeys(contexts))

    def _matching_uses(
        self, uses: tuple[MedicationDiseaseUse, ...], contexts: tuple[str, ...]
    ) -> tuple[MedicationDiseaseUse, ...]:
        normalized_contexts = tuple(self._normalize(item) for item in contexts)
        matched: list[tuple[int, MedicationDiseaseUse]] = []
        for item in uses:
            disease = self._normalize(item.disease_or_context)
            for index, context in enumerate(normalized_contexts):
                if context and (context in disease or disease in context):
                    matched.append((index, item))
                    break
        return tuple(item for _, item in sorted(matched, key=lambda pair: pair[0]))

    def _phenotype_display_line(
        self, item: MedicationDiseaseUse, phenotype: PhenotypeAssessment
    ) -> str:
        phenotype_labels = {
            "DEPRESSIVE_SYNDROME": "Quadro depressivo sem diagnostico fechado",
            "ANXIOUS_SYNDROME": "Quadro ansioso sem diagnostico fechado",
            "MANIFORM_SYNDROME": "Quadro maniforme/suspeita bipolar sem diagnostico fechado",
            "PSYCHOTIC_SYNDROME": "Quadro psicotico sem diagnostico fechado",
            "OBSESSIVE_COMPULSIVE_SYNDROME": "Quadro obsessivo-compulsivo sem diagnostico fechado",
            "AGITATION_SYNDROME": "Agitacao/impulsividade sem diagnostico fechado",
            "INSOMNIA_PREDOMINANT": "Insonia predominante sem diagnostico fechado",
            "SUBSTANCE_WITHDRAWAL_OR_USE_SYNDROME": "Uso/abstinencia de substancias sem diagnostico fechado",
        }
        label = phenotype_labels.get(
            phenotype.primary_phenotype,
            "Quadro clinico sem diagnostico fechado",
        )
        return (
            f"{label} | papel inferido da tabela: {item.role.replace('_', ' ')} | "
            f"status {item.status.replace('_', ' ')} ({item.source_abbreviation})"
        )

    def _fallback_profile_uses(
        self, uses: tuple[MedicationDiseaseUse, ...], phenotype: PhenotypeAssessment
    ) -> tuple[MedicationDiseaseUse, ...]:
        if phenotype.primary_phenotype in {
            "DEPRESSIVE_SYNDROME",
            "ANXIOUS_SYNDROME",
            "INSOMNIA_PREDOMINANT",
            "AGITATION_SYNDROME",
        }:
            return tuple(
                item
                for item in uses
                if item.role in {"adequacao_ao_perfil_sintomatico", "uso_por_efeito_sedativo"}
            )
        return ()

    def _role_compatible(self, role: str, strategy: str) -> bool:
        normalized_role = self._normalize(role)
        if strategy in {"SWITCH_MONOTHERAPY", "INITIAL_MONOTHERAPY"}:
            return (
                self._contains_any(normalized_role, self.PRIMARY_ROLES + self.SHORT_TERM_ROLES)
                and not self._contains_any(normalized_role, self.AUGMENT_ROLES)
            )
        if strategy == "AUGMENT":
            return self._contains_any(normalized_role, self.AUGMENT_ROLES)
        if strategy in {"KEEP_CURRENT", "OPTIMIZE_DOSE"}:
            return not self._contains_any(normalized_role, self.NOT_RECOMMENDED_MARKERS)
        return not self._contains_any(normalized_role, self.NOT_RECOMMENDED_MARKERS)

    def _is_hard_block(self, use: MedicationDiseaseUse) -> bool:
        text = self._normalize(f"{use.role} {use.status}")
        return self._contains_any(text, self.NOT_RECOMMENDED_MARKERS + self.RESTRICTED_MARKERS)

    def _blocks_antidepressant_monotherapy(
        self, drug_class: str, strategy: str, phenotype: PhenotypeAssessment
    ) -> bool:
        if strategy not in {"SWITCH_MONOTHERAPY", "INITIAL_MONOTHERAPY"}:
            return False
        if phenotype.primary_phenotype != "MANIFORM_SYNDROME" and "MANIFORM_SYNDROME" not in phenotype.secondary_phenotypes:
            return False
        return self._contains_any(self._normalize(drug_class), self.ANTIDEPRESSANT_CLASSES)

    def _role_category(self, role: str) -> str:
        normalized = self._normalize(role)
        if self._contains_any(normalized, self.AUGMENT_ROLES):
            return "AUGMENTATION"
        if self._contains_any(normalized, self.MAINTENANCE_ROLES):
            return "MAINTENANCE"
        if self._contains_any(normalized, self.SHORT_TERM_ROLES):
            return "SHORT_TERM_SYMPTOMATIC"
        if self._contains_any(normalized, self.NOT_RECOMMENDED_MARKERS):
            return "NOT_RECOMMENDED"
        if self._contains_any(normalized, self.PRIMARY_ROLES):
            return "PRIMARY_TREATMENT"
        if "off_label" in normalized:
            return "OFF_LABEL_WITH_EVIDENCE"
        return role or "NO_MAPPING"

    def _is_diagnostic_uncertain(self, diagnostic_context: str) -> bool:
        diagnosis = self._normalize(diagnostic_context)
        return not diagnosis or "investigacao" in diagnosis or "nao informado" in diagnosis

    def _status_category(self, status: str) -> str:
        normalized = self._normalize(status)
        if self._contains_any(normalized, self.RESTRICTED_MARKERS):
            return "RESTRICTED"
        if self._contains_any(normalized, self.NOT_RECOMMENDED_MARKERS):
            return "NOT_RECOMMENDED"
        if self._contains_any(normalized, self.OFF_LABEL_MARKERS):
            return "OFF_LABEL_WITH_EVIDENCE"
        if self._contains_any(normalized, self.LIMITED_MARKERS):
            return "LIMITED_EVIDENCE"
        return status or "NO_MAPPING"

    @staticmethod
    def _contains_any(text: str, markers: tuple[str, ...]) -> bool:
        return any(marker in text for marker in markers)

    @staticmethod
    def _normalize(value: str) -> str:
        text = normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii")
        return " ".join(text.lower().replace("/", " ").replace("-", " ").split())
