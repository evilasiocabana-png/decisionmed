"""Application gateway for clinical decision-support payloads.

The default implementation uses a local deterministic rule table. A specialized
GPT adapter can be injected explicitly for experiments, but the app no longer
depends on an external API key or quota to produce decision-support output.
"""

from __future__ import annotations

from typing import Any

from application.clinical_decision_support_contract import (
    ClinicalDecisionSupportResponse,
    CurrentMedicationPayload,
)
from application.decision_support_rule_table import (
    DecisionSupportRuleTable,
    RuleTableContext,
)
from application.clinical_context_registry import ClinicalContextRegistry
from application.clinical_coverage_matrix import ClinicalCoverageMatrix
from application.patient_population_context import PatientPopulationContextService
from application.specialized_gpt_decision_support_adapter import (
    SpecializedGPTDecisionSupportAdapter,
)


class ClinicalDecisionSupportService:
    """Creates display-safe decision-support responses."""

    def __init__(
        self,
        specialized_adapter: SpecializedGPTDecisionSupportAdapter | None = None,
        use_specialized_adapter: bool = False,
        rule_table: DecisionSupportRuleTable | None = None,
        population_context: PatientPopulationContextService | None = None,
        clinical_context_registry: ClinicalContextRegistry | None = None,
        clinical_coverage_matrix: ClinicalCoverageMatrix | None = None,
    ) -> None:
        self._specialized_adapter = (
            specialized_adapter or SpecializedGPTDecisionSupportAdapter()
        )
        self._use_specialized_adapter = use_specialized_adapter
        self._rule_table = rule_table or DecisionSupportRuleTable()
        self._population_context = population_context or PatientPopulationContextService()
        self._clinical_context_registry = clinical_context_registry or ClinicalContextRegistry()
        self._clinical_coverage_matrix = clinical_coverage_matrix or ClinicalCoverageMatrix()
        self._last_adapter_error = ""

    def build_response(self, payload: dict[str, Any]) -> ClinicalDecisionSupportResponse:
        """Return a structured response compatible with the UI contract."""
        if self._use_specialized_adapter:
            external_response = self._request_external_response(payload)
            if external_response is not None:
                return external_response

        symptoms = tuple(str(item) for item in payload.get("symptoms", ()))
        observed_signs = tuple(str(item) for item in payload.get("observed_signs", ()))
        impairment_domains = tuple(
            str(item) for item in payload.get("impairment_domains", ())
        )
        impairment_severity = str(payload.get("impairment_severity", ""))
        stability = str(payload.get("stability", "") or "Nao definido")
        comorbidities = tuple(str(item) for item in payload.get("comorbidities", ()))
        clinical_presentation = str(
            payload.get("clinical_presentation", payload.get("current_state", ""))
        )
        diagnostic_context = str(payload.get("diagnostic_context", ""))
        therapeutic_objective = str(payload.get("therapeutic_objective", ""))
        pharmacological_profile = tuple(
            str(item) for item in payload.get("pharmacological_profile", ())
        )
        clinical_axes = tuple(str(item) for item in payload.get("clinical_axes", ()))
        clinical_context_ids = tuple(
            str(item) for item in payload.get("clinical_context_ids", ())
        )
        medications = tuple(
            CurrentMedicationPayload(**item)
            for item in payload.get("current_medications", ())
            if isinstance(item, dict) and item.get("name")
        )
        safety = payload.get("safety", {}) if isinstance(payload.get("safety"), dict) else {}
        population = self._population_context.assess(
            birth_date=str(payload.get("birth_date", "")),
            sex_context=str(payload.get("sex_context", "not_informed")),
            weight_kg=str(payload.get("weight_kg", "")),
            pregnancy_status=str(payload.get("pregnancy_status", "not_assessed")),
            lactation_status=str(payload.get("lactation_status", "not_assessed")),
            postpartum_status=str(payload.get("postpartum_status", "not_assessed")),
            renal_status=str(payload.get("renal_status", "not_assessed")),
            hepatic_status=str(payload.get("hepatic_status", "not_assessed")),
        )
        clinical_contexts = self._clinical_context_registry.assess(clinical_context_ids)
        coverage = self._clinical_coverage_matrix.match(diagnostic_context)

        return self._rule_table.build(
            RuleTableContext(
                symptoms=symptoms,
                observed_signs=observed_signs,
                impairment_domains=impairment_domains,
                impairment_severity=impairment_severity,
                stability=stability,
                comorbidities=comorbidities,
                medications=medications,
                safety={str(key): str(value) for key, value in safety.items()},
                diagnostic_context=diagnostic_context,
                clinical_presentation=clinical_presentation,
                therapeutic_objective=therapeutic_objective,
                pharmacological_profile=pharmacological_profile,
                clinical_axes=clinical_axes,
                population=population,
                clinical_contexts=clinical_contexts,
                coverage=coverage,
            )
        )

    def _request_external_response(
        self, payload: dict[str, Any]
    ) -> ClinicalDecisionSupportResponse | None:
        try:
            self._last_adapter_error = ""
            return self._specialized_adapter.request(payload)
        except Exception as exc:
            self._last_adapter_error = str(exc)
            return None

    def _adapter_note(self) -> str:
        status_method = getattr(self._specialized_adapter, "diagnostic_status", None)
        if callable(status_method):
            status = status_method()
            base = (
                f"GPT especializado configurado: {status.get('gpt_name', 'desconhecido')} "
                f"({status.get('state', 'desconhecido')}). {status.get('reason', '')}"
            )
        else:
            base = "Status do GPT especializado indisponivel; usando fallback estrutural local."
        if self._last_adapter_error:
            return f"{base} Erro do adapter: {self._last_adapter_error}."
        return base
