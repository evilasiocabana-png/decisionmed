"""Adapter for the specialized Psiquiatria GPT through the OpenAI API.

Custom GPTs from ChatGPT are not directly callable from localhost. This adapter
recreates the selected specialized GPT behavior through API instructions and the
ClinicalDecisionSupportResponse contract.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from application.clinical_decision_support_contract import (
    ActionEvidencePayload,
    ClinicalDecisionSupportResponse,
    EvidenceCitationPayload,
    MedicationActionExplanationPayload,
    MedicationOptionPayload,
    PharmacologicalTargetPayload,
)


DEFAULT_SPECIALIZED_GPT_NAME = "Psiquiatria"
DEFAULT_SPECIALIZED_GPT_URL = (
    "https://chatgpt.com/g/g-6a35c1c8f6208191a7c2c64201451179-psiquiatria"
)


class SpecializedGPTDecisionSupportAdapter:
    """Calls the selected specialized psychiatry GPT prompt when available."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        timeout_seconds: int = 45,
        gpt_name: str | None = None,
        gpt_url: str | None = None,
    ) -> None:
        self._api_key = api_key if api_key is not None else os.getenv("OPENAI_API_KEY")
        self._model = model or os.getenv("PSYCHRX_SPECIALIZED_GPT_MODEL", "gpt-5.5")
        self._timeout_seconds = timeout_seconds
        self._gpt_name = (
            gpt_name
            or os.getenv("PSYCHRX_SPECIALIZED_GPT_NAME")
            or DEFAULT_SPECIALIZED_GPT_NAME
        )
        self._gpt_url = (
            gpt_url
            or os.getenv("PSYCHRX_SPECIALIZED_GPT_URL")
            or DEFAULT_SPECIALIZED_GPT_URL
        )

    def is_available(self) -> bool:
        """Return whether the adapter can call the API."""
        return bool(self._api_key)

    def diagnostic_status(self) -> dict[str, Any]:
        """Return non-secret connection diagnostics for audits and UI fallback."""
        if not self._api_key:
            state = "not_configured"
            reason = "OPENAI_API_KEY ausente; usando fallback estrutural local."
        else:
            state = "configured"
            reason = "OPENAI_API_KEY configurada; adapter tentara chamar a API."
        return {
            "gpt_name": self._gpt_name,
            "gpt_url": self._gpt_url,
            "model": self._model,
            "state": state,
            "reason": reason,
        }

    def request(self, payload: dict[str, Any]) -> ClinicalDecisionSupportResponse | None:
        """Call the specialized GPT and parse the structured response."""
        if not self.is_available():
            return None

        raw = self._post_response(payload)
        content = self._extract_text(raw)
        parsed = json.loads(content)
        return self._response_from_dict(parsed)

    def _post_response(self, payload: dict[str, Any]) -> dict[str, Any]:
        body = {
            "model": self._model,
            "input": [
                {
                    "role": "system",
                    "content": self._system_prompt(),
                },
                {
                    "role": "user",
                    "content": json.dumps(payload, ensure_ascii=False),
                },
            ],
        }
        request = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(f"specialized_gpt_request_failed: {exc}") from exc

    def _system_prompt(self) -> str:
        return (
            f"GPT especializado selecionado: {self._gpt_name}.\n"
            f"Referencia do GPT customizado no ChatGPT: {self._gpt_url}.\n"
            "Observacao tecnica: o link do GPT customizado nao e chamado diretamente; "
            "esta API replica suas instrucoes clinicas dentro deste adapter.\n\n"
            "Voce e um GPT especializado em psiquiatria para suporte a decisao medica "
            "dentro do PsychRx.\n"
            "Responda em portugues do Brasil.\n"
            "Seu objetivo nao e fazer consulta autonoma nem substituir o medico. "
            "Sua funcao e produzir suporte a decisao psicofarmacologica: acao proposta, motivos, "
            "opcoes de substituicao/associacao, evidencia rastreavel, alvo "
            "farmacologico, dose terapeutica como alvo informativo e limites.\n"
            "Voce pode nomear candidatos medicamentosos apenas quando conseguir "
            "informar fonte, secao, trecho/aplicabilidade e alertas de seguranca. "
            "Quando isso nao for possivel, marque a pendencia em unresolved_reason.\n"
            "Toda afirmacao sobre medicamento, dose, substituicao ou associacao "
            "deve ter fonte, secao e aplicabilidade. Se faltar fonte, use "
            "unresolved_reason em linguagem clara.\n"
            "Retorne SOMENTE JSON valido no formato:\n"
            "{"
            "\"summary\": string,"
            "\"recommended_action\": \"maintain|optimize_current|increase_dose|decrease_dose|substitute|associate|taper_or_withdraw|select_candidate|investigate_before_change|insufficient_information\","
            "\"clinical_rationale\": [string],"
            "\"impairment_targets\": [string],"
            "\"pharmacological_targets\": [{\"impairment_domain\": string, \"symptom_target\": string, \"pharmacological_target\": string, \"therapeutic_dose_target\": string, \"unresolved_reason\": string}],"
            "\"substitution_options\": [{\"name\": string, \"role\": \"substitution_candidate\", \"reason\": string, \"pharmacological_target\": string, \"dose_guidance\": string, \"unresolved_reason\": string}],"
            "\"association_options\": [{\"name\": string, \"role\": \"association_candidate\", \"reason\": string, \"pharmacological_target\": string, \"dose_guidance\": string, \"unresolved_reason\": string}],"
            "\"action_evidence\": [{\"action\": string, \"rationale\": string, \"citations\": [{\"source_id\": string, \"title\": string, \"organization\": string, \"year\": string, \"section\": string, \"excerpt_anchor\": string, \"evidence_type\": string, \"quality\": string, \"applicability\": string, \"limitations\": string}], \"unresolved_reason\": string}],"
            "\"medication_action_explanations\": [{\"medication_name\": string, \"maintain_reason\": string, \"increase_reason\": string, \"substitute_reason\": string, \"associate_reason\": string, \"evidence_level\": string, \"substitution_candidate\": {\"name\": string, \"role\": \"substitution_candidate\", \"reason\": string, \"drug_class\": string, \"pharmacological_target\": string, \"dose_guidance\": string, \"evidence\": [], \"unresolved_reason\": string}|null}],"
            "\"rejected_alternatives\": [string],"
            "\"safety_warnings\": [string],"
            "\"monitoring_targets\": [string],"
            "\"confidence\": string,"
            "\"status\": \"ready_for_clinician_review|blocked|unresolved\","
            "\"prescription_boundary\": string"
            "}"
        )

    def _extract_text(self, response: dict[str, Any]) -> str:
        if isinstance(response.get("output_text"), str):
            return response["output_text"]
        texts: list[str] = []
        for item in response.get("output", []):
            for content in item.get("content", []):
                if content.get("type") == "output_text" and content.get("text"):
                    texts.append(str(content["text"]))
        if not texts:
            raise ValueError("specialized_gpt_empty_response")
        return "\n".join(texts).strip()

    def _response_from_dict(self, data: dict[str, Any]) -> ClinicalDecisionSupportResponse:
        response = ClinicalDecisionSupportResponse(
            summary=str(data.get("summary", "")),
            recommended_action=data.get("recommended_action", "insufficient_information"),
            clinical_rationale=tuple(str(item) for item in data.get("clinical_rationale", ())),
            impairment_targets=tuple(str(item) for item in data.get("impairment_targets", ())),
            pharmacological_targets=tuple(
                self._target_from_dict(item)
                for item in data.get("pharmacological_targets", ())
                if isinstance(item, dict)
            ),
            substitution_options=tuple(
                self._option_from_dict(item, "substitution_candidate")
                for item in data.get("substitution_options", ())
                if isinstance(item, dict)
            ),
            association_options=tuple(
                self._option_from_dict(item, "association_candidate")
                for item in data.get("association_options", ())
                if isinstance(item, dict)
            ),
            action_evidence=tuple(
                self._action_evidence_from_dict(item)
                for item in data.get("action_evidence", ())
                if isinstance(item, dict)
            ),
            medication_action_explanations=tuple(
                self._medication_action_explanation_from_dict(item)
                for item in data.get("medication_action_explanations", ())
                if isinstance(item, dict)
            ),
            rejected_alternatives=tuple(str(item) for item in data.get("rejected_alternatives", ())),
            safety_warnings=tuple(str(item) for item in data.get("safety_warnings", ())),
            monitoring_targets=tuple(str(item) for item in data.get("monitoring_targets", ())),
            confidence=str(data.get("confidence", "not_calculated")),
            status=data.get("status", "unresolved"),
            prescription_boundary=str(
                data.get(
                    "prescription_boundary",
                    "Suporte a decisao medica. A prescricao final permanece com o medico.",
                )
            ),
        )
        issues = response.validate_for_display()
        if issues:
            return ClinicalDecisionSupportResponse(
                summary="Resposta do GPT especializado incompleta para exibicao segura.",
                recommended_action="insufficient_information",
                clinical_rationale=(
                    "A resposta foi recebida, mas falhou na validacao estrutural.",
                    f"Pendencias: {', '.join(issues)}.",
                ),
                action_evidence=(
                    ActionEvidencePayload(
                        action="insufficient_information",
                        rationale="A resposta do GPT precisa ser corrigida antes de aparecer como conselho.",
                        unresolved_reason="invalid_specialized_gpt_response",
                    ),
                ),
                status="unresolved",
            )
        return response

    def _target_from_dict(self, item: dict[str, Any]) -> PharmacologicalTargetPayload:
        return PharmacologicalTargetPayload(
            impairment_domain=str(item.get("impairment_domain", "")),
            symptom_target=str(item.get("symptom_target", "")),
            pharmacological_target=str(item.get("pharmacological_target", "")),
            therapeutic_dose_target=str(item.get("therapeutic_dose_target", "")),
            unresolved_reason=str(item.get("unresolved_reason", "")),
        )

    def _option_from_dict(self, item: dict[str, Any], default_role: str) -> MedicationOptionPayload:
        return MedicationOptionPayload(
            name=str(item.get("name", "")),
            role=item.get("role", default_role),
            reason=str(item.get("reason", "")),
            drug_class=str(item.get("drug_class", "")),
            pharmacological_target=str(item.get("pharmacological_target", "")),
            dose_guidance=str(item.get("dose_guidance", "")),
            evidence=tuple(
                self._citation_from_dict(citation)
                for citation in item.get("evidence", ())
                if isinstance(citation, dict)
            ),
            safety_notes=tuple(str(note) for note in item.get("safety_notes", ())),
            unresolved_reason=str(item.get("unresolved_reason", "")),
        )

    def _action_evidence_from_dict(self, item: dict[str, Any]) -> ActionEvidencePayload:
        return ActionEvidencePayload(
            action=item.get("action", "insufficient_information"),
            rationale=str(item.get("rationale", "")),
            citations=tuple(
                self._citation_from_dict(citation)
                for citation in item.get("citations", ())
                if isinstance(citation, dict)
            ),
            unresolved_reason=str(item.get("unresolved_reason", "")),
        )

    def _medication_action_explanation_from_dict(
        self, item: dict[str, Any]
    ) -> MedicationActionExplanationPayload:
        candidate = item.get("substitution_candidate")
        return MedicationActionExplanationPayload(
            medication_name=str(item.get("medication_name", "")),
            maintain_reason=str(item.get("maintain_reason", "")),
            increase_reason=str(item.get("increase_reason", "")),
            substitute_reason=str(item.get("substitute_reason", "")),
            associate_reason=str(item.get("associate_reason", "")),
            evidence_level=str(item.get("evidence_level", "")),
            substitution_candidate=(
                self._option_from_dict(candidate, "substitution_candidate")
                if isinstance(candidate, dict)
                else None
            ),
        )

    def _citation_from_dict(self, item: dict[str, Any]) -> EvidenceCitationPayload:
        return EvidenceCitationPayload(
            source_id=str(item.get("source_id", "")),
            title=str(item.get("title", "")),
            organization=str(item.get("organization", "")),
            year=str(item.get("year", "")),
            section=str(item.get("section", "")),
            excerpt_anchor=str(item.get("excerpt_anchor", "")),
            evidence_type=str(item.get("evidence_type", "")),
            quality=str(item.get("quality", "")),
            applicability=str(item.get("applicability", "")),
            limitations=str(item.get("limitations", "")),
        )
