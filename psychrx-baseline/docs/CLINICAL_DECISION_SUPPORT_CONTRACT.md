# Clinical Decision Support Contract

Este contrato define como o PsychRx envia o estado da consulta ao GPT especializado
e como recebe a resposta de suporte a decisao medica.

O contrato nao autoriza prescricao automatica. Ele organiza:

- estado clinico atual;
- sintomas e sinais;
- prejuizo funcional;
- receita atual;
- seguranca;
- conselho estruturado;
- evidencias por acao;
- alvo farmacologico;
- opcoes de substituicao ou associacao;
- limites para revisao medica.

## Entrada

`ClinicalDecisionSupportRequest`

Campos principais:

- `patient_label`
- `birth_date`
- `diagnostic_context`
- `current_state`
- `symptoms`
- `observed_signs`
- `impairment_domains`
- `impairment_severity`
- `stability`
- `comorbidities`
- `current_medications`
- `safety`
- `clinician_question`

## Saida

`ClinicalDecisionSupportResponse`

Campos principais:

- `summary`
- `recommended_action`
- `clinical_rationale`
- `impairment_targets`
- `pharmacological_targets`
- `substitution_options`
- `association_options`
- `action_evidence`
- `medication_action_explanations`
- `rejected_alternatives`
- `safety_warnings`
- `monitoring_targets`
- `confidence`
- `status`
- `prescription_boundary`

## Evidencia

Cada acao proposta deve possuir `ActionEvidencePayload`.

Cada evidencia deve apontar:

- `source_id`
- `title`
- `organization`
- `year`
- `section`
- `excerpt_anchor`
- `evidence_type`
- `quality`
- `applicability`
- `limitations`

Se a evidencia ainda nao existir, a resposta deve preencher `unresolved_reason`.
O GPT especializado nunca deve inventar fonte.

## Explicacao de acao por medicamento

Cada medicamento registrado na receita atual pode possuir um
`MedicationActionExplanationPayload`. O payload deve responder separadamente:

1. por que manter;
2. por que aumentar;
3. por que trocar;
4. por que potencializar;
5. qual e o nivel de evidencia demonstravel para aquela decisao.

As respostas devem declarar se a estrategia esta favorecida, condicional, nao
favorecida ou nao avaliavel. O nivel de evidencia nao pode ser convertido em
`forte`, `moderado` ou `limitado` sem classificacao cientifica formal. Quando
existirem apenas fontes de faixa ou perfil farmacologico, a resposta deve dizer
que ha rastreabilidade, mas que a forca comparativa da decisao ainda nao foi
classificada.

A camada Interface apenas apresenta esse payload. Ela nao pode inferir a
justificativa clinica a partir do layout, do nome do medicamento ou da acao
global da receita.

## Alvo farmacologico

Cada `PharmacologicalTargetPayload` deve ligar:

- dominio de prejuizo;
- sintoma alvo;
- alvo farmacologico;
- dose terapeutica alvo;
- fonte da dose ou motivo de pendencia.

## Limite

O GPT especializado fornece suporte a decisao.
O medico permanece responsavel por:

- escolha final do medicamento;
- dose;
- prescricao;
- conduta;
- monitorizacao clinica.

## GPT especializado selecionado

O GPT especializado selecionado para suporte ao motor e:

`Psiquiatria`

URL de referencia:

`https://chatgpt.com/g/g-6a35c1c8f6208191a7c2c64201451179-psiquiatria`

Observacao tecnica: GPTs customizados do ChatGPT nao sao chamados diretamente pelo
localhost. O app usa um adapter que replica as instrucoes do GPT especializado via
API, mantendo o contrato `ClinicalDecisionSupportResponse`.

## Integracao com API

O app usa:

`application/specialized_gpt_decision_support_adapter.py`

Variaveis de ambiente:

- `OPENAI_API_KEY`: chave usada para chamar a API.
- `PSYCHRX_SPECIALIZED_GPT_MODEL`: modelo usado pelo adapter. Padrao: `gpt-5.5`.
- `PSYCHRX_SPECIALIZED_GPT_NAME`: nome logico do GPT. Padrao: `Psiquiatria`.
- `PSYCHRX_SPECIALIZED_GPT_URL`: URL de referencia do GPT customizado.

Se `OPENAI_API_KEY` nao estiver configurada, o app usa fallback estrutural seguro
e marca os campos cientificos como pendentes.

O endpoint local permanece:

`POST /api/decision-support`

Fluxo:

```text
UI
↓
ClinicalDecisionSupportRequest
↓
SpecializedGPTDecisionSupportAdapter
↓
OpenAI API
↓
ClinicalDecisionSupportResponse
↓
UI
```
