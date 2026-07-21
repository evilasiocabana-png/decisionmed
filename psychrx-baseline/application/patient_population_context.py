"""Patient population context used before local pharmacological comparison."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class PatientPopulationContext:
    age_years: int | None
    age_band: str
    sex_context: str
    weight_kg: str
    pregnancy_status: str
    lactation_status: str
    postpartum_status: str
    renal_status: str
    hepatic_status: str
    blocking_warnings: tuple[str, ...] = ()

    def display_line(self) -> str:
        age = str(self.age_years) if self.age_years is not None else "nao informada"
        return f"Populacao: {self.age_band}; idade: {age}"


class PatientPopulationContextService:
    """Derive an auditable age band without making a diagnosis or dose decision."""

    def assess(
        self,
        *,
        birth_date: str,
        sex_context: str = "not_informed",
        weight_kg: str = "",
        pregnancy_status: str = "not_assessed",
        lactation_status: str = "not_assessed",
        postpartum_status: str = "not_assessed",
        renal_status: str = "not_assessed",
        hepatic_status: str = "not_assessed",
        as_of: date | None = None,
    ) -> PatientPopulationContext:
        reference = as_of or date.today()
        age = self._age(birth_date, reference)
        warnings: list[str] = []
        if age is None:
            band = "UNKNOWN"
            warnings.append("Idade: Nao avaliada")
        elif age < 12:
            band = "CHILD"
            warnings.append("Populacao pediatrica: revisao especifica obrigatoria")
        elif age < 18:
            band = "ADOLESCENT"
            warnings.append("Populacao adolescente: revisao especifica obrigatoria")
        elif age < 65:
            band = "ADULT"
        else:
            band = "OLDER_ADULT"
            warnings.append("Pessoa idosa: revisao especifica obrigatoria")

        pregnancy = self._normalized_status(pregnancy_status)
        lactation = self._normalized_status(lactation_status)
        postpartum = self._normalized_status(postpartum_status)
        warnings.extend(self._perinatal_warnings("Gestacao", pregnancy))
        warnings.extend(self._perinatal_warnings("Lactacao", lactation))
        warnings.extend(self._perinatal_warnings("Periodo pos-parto", postpartum))

        renal = self._normalized_status(renal_status)
        hepatic = self._normalized_status(hepatic_status)
        warnings.extend(self._organ_warnings("Funcao renal", renal))
        warnings.extend(self._organ_warnings("Funcao hepatica", hepatic))

        return PatientPopulationContext(
            age_years=age,
            age_band=band,
            sex_context=str(sex_context or "not_informed").strip(),
            weight_kg=str(weight_kg or "").strip(),
            pregnancy_status=pregnancy,
            lactation_status=lactation,
            postpartum_status=postpartum,
            renal_status=renal,
            hepatic_status=hepatic,
            blocking_warnings=tuple(warnings),
        )

    @staticmethod
    def _organ_warnings(label: str, status: str) -> tuple[str, ...]:
        if status in {"preservada", "preserved", "not_applicable", "nao_aplicavel"}:
            return ()
        if status in {"alterada", "altered", "present"}:
            return (f"{label} alterada: revisao especifica obrigatoria",)
        return (f"{label}: Nao avaliada",)

    @staticmethod
    def _perinatal_warnings(label: str, status: str) -> tuple[str, ...]:
        if status in {"denied", "not_applicable", "nao_aplicavel"}:
            return ()
        if status == "present":
            return (f"{label}: revisao perinatal especifica obrigatoria",)
        return (f"{label}: Nao avaliada",)

    @staticmethod
    def _normalized_status(value: str) -> str:
        normalized = str(value or "not_assessed").strip().lower().replace(" ", "_")
        mapping = {
            "presente": "present",
            "negado": "denied",
            "nao_aplicavel": "not_applicable",
            "não_aplicável": "not_applicable",
            "desconhecido": "unknown",
        }
        return mapping.get(normalized, normalized)

    @staticmethod
    def _age(value: str, reference: date) -> int | None:
        try:
            born = date.fromisoformat(str(value or ""))
        except ValueError:
            return None
        if born > reference:
            return None
        age = reference.year - born.year - ((reference.month, reference.day) < (born.month, born.day))
        return age if 0 <= age <= 130 else None
