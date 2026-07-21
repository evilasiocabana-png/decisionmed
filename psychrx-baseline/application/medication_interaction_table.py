"""Medication interaction screening for the local decision-support motor."""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass

from application.clinical_decision_support_contract import CurrentMedicationPayload


@dataclass(frozen=True)
class InteractionFinding:
    """Display-safe interaction finding for physician review."""

    title: str
    risk: str
    review_action: str
    sources: tuple[str, ...]

    def display_line(self) -> str:
        source_text = "/".join(self.sources)
        return (
            f"{self.title}: {self.risk}. Revisar: {self.review_action}. "
            f"Fonte: {source_text}."
        )


@dataclass(frozen=True)
class MedicationInteractionProfile:
    """Interaction attributes used by the local table."""

    name: str
    drug_class: str
    serotonergic: bool = False
    cns_depressant: bool = False
    qt_risk: bool = False
    cyp2d6_inhibitor: bool = False
    cyp2d6_substrate_sensitive: bool = False
    cyp3a4_substrate: bool = False
    cyp3a4_inducer: bool = False
    valproate: bool = False
    lamotrigine: bool = False
    lithium: bool = False
    seizure_threshold: bool = False
    sources: tuple[str, ...] = ("DM",)


class MedicationInteractionTable:
    """Small official-source interaction table used by the app."""

    _PROFILES: tuple[MedicationInteractionProfile, ...] = (
        MedicationInteractionProfile("Fluoxetina", "ISRS", serotonergic=True, cyp2d6_inhibitor=True, qt_risk=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Sertralina", "ISRS", serotonergic=True, cyp2d6_inhibitor=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Escitalopram", "ISRS", serotonergic=True, qt_risk=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Citalopram", "ISRS", serotonergic=True, qt_risk=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Paroxetina", "ISRS", serotonergic=True, cyp2d6_inhibitor=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Fluvoxamina", "ISRS", serotonergic=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Venlafaxina", "IRSN", serotonergic=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Desvenlafaxina", "IRSN", serotonergic=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Duloxetina", "IRSN", serotonergic=True, cyp2d6_inhibitor=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Amitriptilina", "Triciclico", serotonergic=True, cyp2d6_substrate_sensitive=True, qt_risk=True, cns_depressant=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Nortriptilina", "Triciclico", serotonergic=True, cyp2d6_substrate_sensitive=True, qt_risk=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Clomipramina", "Triciclico", serotonergic=True, cyp2d6_substrate_sensitive=True, qt_risk=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Imipramina", "Triciclico", serotonergic=True, cyp2d6_substrate_sensitive=True, qt_risk=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Trazodona", "SARI", serotonergic=True, cns_depressant=True, qt_risk=True, cyp3a4_substrate=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Mirtazapina", "NaSSA", cns_depressant=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Quetiapina", "Antipsicotico atipico", cns_depressant=True, qt_risk=True, cyp3a4_substrate=True, sources=("DM", "BNF", "ST-PG", "GG")),
        MedicationInteractionProfile("Risperidona", "Antipsicotico atipico", qt_risk=True, cyp2d6_substrate_sensitive=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Olanzapina", "Antipsicotico atipico", cns_depressant=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Aripiprazol", "Antipsicotico atipico", cyp2d6_substrate_sensitive=True, cyp3a4_substrate=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Haloperidol", "Antipsicotico tipico", qt_risk=True, cyp2d6_substrate_sensitive=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Clonazepam", "Benzodiazepinico", cns_depressant=True, sources=("DM", "ST-PG")),
        MedicationInteractionProfile("Bromazepam", "Benzodiazepinico", cns_depressant=True, sources=("ST-PG", "GG")),
        MedicationInteractionProfile("Alprazolam", "Benzodiazepinico", cns_depressant=True, cyp3a4_substrate=True, sources=("DM", "ST-PG")),
        MedicationInteractionProfile("Diazepam", "Benzodiazepinico", cns_depressant=True, sources=("DM", "ST-PG")),
        MedicationInteractionProfile("Lorazepam", "Benzodiazepinico", cns_depressant=True, sources=("DM", "ST-PG")),
        MedicationInteractionProfile("Zolpidem", "Hipnotico Z", cns_depressant=True, sources=("DM", "ST-PG")),
        MedicationInteractionProfile("Litio", "Estabilizador", serotonergic=True, lithium=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Divalproato", "Anticonvulsivante/estabilizador", valproate=True, cns_depressant=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Valproato", "Anticonvulsivante/estabilizador", valproate=True, cns_depressant=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Lamotrigina", "Anticonvulsivante/estabilizador", lamotrigine=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Carbamazepina", "Anticonvulsivante/estabilizador", cyp3a4_inducer=True, cns_depressant=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Fenitoina", "Anticonvulsivante", cyp3a4_inducer=True, cns_depressant=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Fenobarbital", "Barbiturico", cyp3a4_inducer=True, cns_depressant=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Bupropiona", "NDRI", cyp2d6_inhibitor=True, seizure_threshold=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Bupropiona XL", "NDRI", cyp2d6_inhibitor=True, seizure_threshold=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Buspirona", "Ansiolitico nao benzodiazepinico", serotonergic=True, sources=("DM", "ST-PG", "GG")),
        MedicationInteractionProfile("Naltrexona", "Dependencia quimica", sources=("DM", "ST-PG")),
        MedicationInteractionProfile("Acamprosato", "Dependencia quimica", sources=("DM", "ST-PG")),
    )

    _ALIASES = {
        "venlafaxina xr": "venlafaxina",
        "desvenlafaxina er": "desvenlafaxina",
        "bupropiona xl": "bupropiona xl",
        "divalproato de sodio": "divalproato",
        "valproato de sodio": "valproato",
        "carbonato de litio": "litio",
    }

    def __init__(self) -> None:
        self._by_key = {self._key(profile.name): profile for profile in self._PROFILES}

    def profiles(self) -> tuple[MedicationInteractionProfile, ...]:
        """Return canonical profiles for coverage auditing."""
        return self._PROFILES

    def aliases(self) -> dict[str, str]:
        """Return explicit non-clinical name aliases."""
        return dict(self._ALIASES)

    def profile_for(self, name: str) -> MedicationInteractionProfile | None:
        """Resolve a canonical profile using explicit aliases before fallback."""
        return self._profile_for(name)

    def findings(
        self,
        medications: tuple[CurrentMedicationPayload, ...],
        *,
        comorbidities: tuple[str, ...] = (),
        safety: dict[str, str] | None = None,
    ) -> tuple[InteractionFinding, ...]:
        profiles: list[MedicationInteractionProfile] = []
        unknown_names: list[str] = []
        for medication in medications:
            profile = self._profile_for(medication.name)
            if profile is None:
                unknown_names.append(medication.name)
            else:
                profiles.append(profile)
        findings: list[InteractionFinding] = []
        findings.extend(self._pair_findings(tuple(profiles)))
        findings.extend(self._context_findings(tuple(profiles), comorbidities, safety or {}))
        findings.extend(self._unknown_medication_findings(tuple(unknown_names), tuple(profiles)))
        if not findings and len(medications) >= 2:
            findings.append(
                InteractionFinding(
                    title="Receita combinada",
                    risk="sem interacao prioritaria cadastrada entre os medicamentos informados",
                    review_action="manter revisao clinica usual e conferir bula se houver nova medicacao",
                    sources=("TM", "PENDENTE"),
                )
            )
        return tuple(dict.fromkeys(findings))

    @staticmethod
    def _unknown_medication_findings(
        unknown_names: tuple[str, ...],
        known_profiles: tuple[MedicationInteractionProfile, ...],
    ) -> tuple[InteractionFinding, ...]:
        if not unknown_names:
            return ()
        names = ", ".join(unknown_names)
        risk = "medicamento fora da base local de interacoes; interacao nao pode ser descartada"
        if known_profiles:
            known = ", ".join(profile.name for profile in known_profiles[:4])
            risk = (
                f"{risk} no cruzamento com {known}"
                f"{'...' if len(known_profiles) > 4 else ''}"
            )
        return (
            InteractionFinding(
                title=f"Medicamento nao cadastrado: {names}",
                risk=risk,
                review_action=(
                    "consultar bula oficial/monografia e cadastrar classe, vias CYP, QT, "
                    "serotoninergico, sedacao e cautelas antes de concluir interacao"
                ),
                sources=("PENDENTE", "DM", "ANVISA", "EMA"),
            ),
        )

    def _profile_for(self, name: str) -> MedicationInteractionProfile | None:
        key = self._key(name)
        key = self._ALIASES.get(key, key)
        if key in self._by_key:
            return self._by_key[key]
        for profile_key, profile in self._by_key.items():
            if profile_key in key or key in profile_key:
                return profile
        return None

    def _pair_findings(
        self, profiles: tuple[MedicationInteractionProfile, ...]
    ) -> tuple[InteractionFinding, ...]:
        findings: list[InteractionFinding] = []
        for index, left in enumerate(profiles):
            for right in profiles[index + 1 :]:
                names = f"{left.name} + {right.name}"
                sources = self._merge_sources(left, right)
                if left.serotonergic and right.serotonergic:
                    findings.append(
                        InteractionFinding(
                            title=names,
                            risk="somacao serotoninergica; revisar risco de sindrome serotoninergica",
                            review_action="checar indicacao da combinacao, sintomas autonomicos/neuromusculares e necessidade de monitorizacao",
                            sources=sources,
                        )
                    )
                if left.cns_depressant and right.cns_depressant:
                    findings.append(
                        InteractionFinding(
                            title=names,
                            risk="somacao depressora do SNC; pode aumentar sedacao, quedas e prejuizo psicomotor",
                            review_action="revisar dose, horario, alcool/opioides e risco de depressao respiratoria quando aplicavel",
                            sources=sources,
                        )
                    )
                if left.qt_risk and right.qt_risk:
                    findings.append(
                        InteractionFinding(
                            title=names,
                            risk="somacao de risco QT",
                            review_action="revisar ECG, eletrolitos, dose e outros fatores de risco antes de combinar ou escalar",
                            sources=sources,
                        )
                    )
                if self._has_cyp2d6_exposure_pair(left, right):
                    findings.append(
                        InteractionFinding(
                            title=names,
                            risk="inibicao CYP2D6 pode elevar exposicao de substrato sensivel",
                            review_action="revisar efeitos adversos, dose e alternativa com menor interacao se necessario",
                            sources=sources,
                        )
                    )
                if self._has_cyp3a4_pair(left, right):
                    findings.append(
                        InteractionFinding(
                            title=names,
                            risk="inducao/inibicao CYP3A4 pode alterar exposicao do medicamento",
                            review_action="revisar necessidade de ajuste, eficacia, toxicidade e bula do par",
                            sources=sources,
                        )
                    )
                if (left.valproate and right.lamotrigine) or (left.lamotrigine and right.valproate):
                    findings.append(
                        InteractionFinding(
                            title=names,
                            risk="valproato aumenta exposicao/risco cutaneo da lamotrigina",
                            review_action="revisar titulacao, rash, dose inicial e monitorizacao",
                            sources=sources,
                        )
                    )
                if left.lithium and right.serotonergic or right.lithium and left.serotonergic:
                    findings.append(
                        InteractionFinding(
                            title=names,
                            risk="litio com agente serotoninergico aumenta necessidade de vigiar sindrome serotoninergica",
                            review_action="monitorar sinais clinicos e reavaliar combinacao se sintomas surgirem",
                            sources=sources,
                        )
                    )
        return tuple(findings)

    def _context_findings(
        self,
        profiles: tuple[MedicationInteractionProfile, ...],
        comorbidities: tuple[str, ...],
        safety: dict[str, str],
    ) -> tuple[InteractionFinding, ...]:
        text = self._key(" ".join((*comorbidities, *safety.values())))
        findings: list[InteractionFinding] = []
        if ("alcool" in text or "substancia" in text or "droga" in text) and any(
            profile.cns_depressant for profile in profiles
        ):
            findings.append(
                InteractionFinding(
                    title="Alcool/substancias + sedativos",
                    risk="risco aumentado de sedacao, queda, prejuizo psicomotor e depressao respiratoria conforme combinacao",
                    review_action="avaliar uso real, padrao de consumo e seguranca antes de intensificar sedativos",
                    sources=("DM", "ST-PG", "GG"),
                )
            )
        if "fitoterapico" in text or "suplemento" in text:
            findings.append(
                InteractionFinding(
                    title="Fitoterapicos/suplementos",
                    risk="interacao nao especificada pela receita; erva-de-sao-joao e outros produtos podem alterar risco serotoninergico/metabolico",
                    review_action="identificar produto, dose e frequencia antes de interpretar o ranking",
                    sources=("DM", "ST-PG", "PENDENTE"),
                )
            )
        if "qt" in text and any(profile.qt_risk for profile in profiles):
            findings.append(
                InteractionFinding(
                    title="Risco QT informado + medicamento com cautela QT",
                    risk="risco eletrico precisa ser revisado antes de aumentar dose ou associar outro farmaco com QT",
                    review_action="checar ECG, eletrolitos, dose, idade e medicamentos concomitantes",
                    sources=("DM", "BNF", "ST-PG"),
                )
            )
        return tuple(findings)

    @staticmethod
    def _has_cyp2d6_exposure_pair(
        left: MedicationInteractionProfile, right: MedicationInteractionProfile
    ) -> bool:
        return (
            left.cyp2d6_inhibitor
            and right.cyp2d6_substrate_sensitive
            or right.cyp2d6_inhibitor
            and left.cyp2d6_substrate_sensitive
        )

    @staticmethod
    def _has_cyp3a4_pair(
        left: MedicationInteractionProfile, right: MedicationInteractionProfile
    ) -> bool:
        return (
            left.cyp3a4_inducer
            and right.cyp3a4_substrate
            or right.cyp3a4_inducer
            and left.cyp3a4_substrate
        )

    @staticmethod
    def _merge_sources(
        left: MedicationInteractionProfile, right: MedicationInteractionProfile
    ) -> tuple[str, ...]:
        return tuple(dict.fromkeys((*left.sources, *right.sources)))

    @staticmethod
    def _key(value: str) -> str:
        text = unicodedata.normalize("NFKD", str(value or "").lower())
        return text.encode("ascii", "ignore").decode("ascii")
