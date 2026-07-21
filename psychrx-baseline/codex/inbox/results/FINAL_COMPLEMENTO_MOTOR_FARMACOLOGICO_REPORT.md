# FINAL_COMPLEMENTO_MOTOR_FARMACOLOGICO_REPORT

Data: 2026-07-11

## Conclusao

A missao foi executada como complemento do motor existente, sem reestruturar o app, sem criar motor paralelo e sem substituir as oito abas, a Aba 9 ou a Aba 10.

O aplicativo passou a incluir:

- medicacao em uso;
- dose prescrita e dose realmente utilizada;
- tempo total de uso e tempo na dose atual;
- adesao;
- resposta percebida;
- tolerabilidade;
- efeitos adversos;
- perguntas adicionais de risco;
- avaliacao da dose atual em relacao a faixa cadastrada;
- consequencias operacionais de risco;
- exibicao da adequacao da receita atual no Conselho do Motor.

## Arquivos criados

- `application/current_medication_assessment.py`
- `tests/application/test_current_medication_assessment.py`
- `codex/inbox/results/FINAL_COMPLEMENTO_MOTOR_FARMACOLOGICO_REPORT.md`

## Arquivos modificados

- `application/clinical_decision_support_contract.py`
- `application/decision_support_rule_table.py`
- `interfaces/web/static/index.html`
- `interfaces/web/static/app.js`
- `interfaces/web/static/styles.css`
- `tests/application/test_clinical_decision_support_contract.py`
- `tests/interfaces/test_web_app.py`

## Onde os novos campos foram integrados

Os campos foram integrados na etapa `Receita atual` do fluxo progressivo do app.

Campos adicionados:

- medicamento atual;
- indicacao atual;
- formulacao;
- via;
- dose prescrita;
- dose usada;
- unidade;
- frequencia;
- horario;
- inicio;
- ultima alteracao de dose;
- tempo de uso;
- tempo na dose atual;
- adesao;
- beneficio percebido;
- resposta percebida;
- efeitos adversos;
- tolerabilidade;
- motivo do uso.

O app envia esses dados em `current_medications` para `/api/decision-support`.

## Como a medicacao atual e avaliada

O novo servico `CurrentMedicationAssessmentService` calcula:

- `current_dose_status`;
- `duration_status`;
- `adherence_status`;
- `response_status`;
- `tolerability_status`;
- `optimization_possible`.

Estados retornados incluem:

- `below_registered_range`;
- `within_registered_range`;
- `above_registered_range`;
- `duration_possibly_insufficient`;
- `duration_possibly_sufficient`;
- `partial_response`;
- `no_response`;
- `good_response`;
- `insufficient_adherence`;
- `poor_tolerability`;
- `not_favored`;
- `possible_for_physician_review`;
- `indeterminate`.

## Como funcionam as perguntas de risco

As perguntas de risco foram incorporadas ao bloco existente de restricoes.

Novos riscos incluem:

- alergia ou reacao grave anterior;
- gestacao;
- lactacao;
- epilepsia;
- glaucoma;
- retencao urinaria;
- risco cardiovascular;
- QT prolongado;
- uso de substancias;
- fitoterapicos e suplementos;
- interacoes relevantes.

Cada risco mapeado recebe uma consequencia operacional:

- `INFORMAR`;
- `CAUTELA`;
- `REDUZIR_COMPATIBILIDADE`;
- `EXIGIR_REVISAO_MEDICA`;
- `BLOQUEAR_OPCAO`.

Riscos graves aparecem no resultado como `safety_warnings` e tambem no racional clinico.

## Como o alvo terapeutico aparece no resultado

O resultado preserva o bloco `Alvo farmacologico` e acrescenta a avaliacao da receita atual:

- medicamento atual;
- dose atual;
- faixa cadastrada;
- posicao da dose em relacao a faixa;
- tempo de uso;
- tempo na dose atual;
- adesao;
- resposta;
- tolerabilidade;
- possibilidade de otimizacao antes de troca.

Faixa de dose cadastrada e apresentada como apoio a decisao, nao como prescricao individual.

## Como as oito abas sao aproveitadas

As oito abas permanecem como base de conhecimento curada.

O motor continua usando:

- tabela de estrategia medicamentosa;
- matriz farmacologica local;
- tabela unificada;
- fontes e citations ja registradas;
- ranking farmacologico existente.

Nenhuma aba original foi removida ou substituida.

## Como as fontes oficiais sao rastreadas

As faixas e candidatos continuam usando `EvidenceCitationPayload` e fontes locais registradas.

Quando a fonte de dose existe, ela e carregada por `MedicationStrategyTable.current_dose_target`.

Quando a informacao nao esta disponivel, o sistema preserva estado indeterminado ou pendente em vez de inferir silenciosamente.

## Testes executados

```bash
python -m unittest tests.application.test_current_medication_assessment tests.application.test_clinical_decision_support_contract tests.interfaces.test_web_app
python -m unittest discover -s tests -t .
```

Resultado:

```text
169 tests OK
```

## Validacao local

```text
GET /health -> {"status": "ok", "mode": "read-only"}
POST /api/decision-support -> ready_for_clinician_review
```

Exemplo validado:

```text
Avaliacao da medicacao atual: Sertralina 50 mg 1x/dia.
Faixa cadastrada: 25 mg / 50 mg / 100 mg / 200 mg.
Dose atual: dentro da faixa cadastrada.
Tempo de uso: possivelmente suficiente.
Adesao: boa.
Resposta: resposta parcial.
Tolerabilidade: boa.
Otimizacao antes de troca: possivel para revisao medica.
Risco avaliado: QT prolongado -> consequencia operacional: BLOQUEAR_OPCAO.
```

## Limitacoes e dados pendentes

- A UI registra uma medicacao atual por vez nesta etapa.
- O backend ja aceita multiplas medicacoes em `current_medications`.
- A expansao visual para varias medicacoes pode ser feita depois sem alterar o contrato.
- Campos sem fonte validada devem continuar como indeterminados ou pendentes, sem virar regra ativa automatica.

## Confirmacao de limites

- Nao houve prescricao automatica.
- Nao houve dose individual automatica.
- Nao houve troca, associacao ou retirada automatica.
- Nao houve criacao de motor paralelo.
- Nao houve reestruturacao do app.
- O medico permanece responsavel pela decisao final.
