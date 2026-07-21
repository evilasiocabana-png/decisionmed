# Clinical Phenotype + Disease Use Filter Implementation

## Mission

Implementar filtro de fenotipo clinico e filtro de uso por doenca/quadro no motor local do PsychRx, integrados ao ranking, ao contrato de resposta e aos quatro quadros principais do app.

## Arquivos alterados

- `application/clinical_decision_support_contract.py`
- `application/clinical_decision_support_service.py`
- `application/decision_support_rule_table.py`
- `application/medication_disease_use_table.py`
- `interfaces/web/static/index.html`
- `interfaces/web/static/app.js`
- `tests/application/test_clinical_decision_support_contract.py`
- `tests/interfaces/test_web_app.py`

## Arquivos criados

- `application/clinical_phenotype_filter.py`
- `application/disease_use_filter.py`
- `docs/decision_support_engine/CLINICAL_PHENOTYPE_DISEASE_FILTER_IMPLEMENTATION.md`

## Fluxo anterior

```text
Dados clinicos
-> matriz farmacologica
-> ranking
-> exibicao de uso por doenca como explicacao
```

O campo `Uso por doenca` era exibido depois do ranking, mas nao atuava como filtro forte de elegibilidade.

## Fluxo novo

```text
Dados clinicos
-> ClinicalPhenotypeFilter
-> estrategia terapeutica estrutural
-> DiseaseUseFilter
-> ranking somente entre candidatos elegiveis
-> resposta estruturada para o app
```

## Classes criadas

### `ClinicalPhenotypeFilter`

Detecta quadro/fenotipo predominante sem afirmar diagnostico:

- `DEPRESSIVE_SYNDROME`
- `ANXIOUS_SYNDROME`
- `MANIFORM_SYNDROME`
- `PSYCHOTIC_SYNDROME`
- `OBSESSIVE_COMPULSIVE_SYNDROME`
- `AGITATION_SYNDROME`
- `INSOMNIA_PREDOMINANT`
- `COGNITIVE_SYNDROME`
- `SUBSTANCE_WITHDRAWAL_OR_USE_SYNDROME`
- `UNSPECIFIED_OR_INSUFFICIENT_DATA`

### `DiseaseUseFilter`

Avalia cada candidato antes da exibicao final, retornando `MedicationEligibility`.

## Regras de bloqueio

- `NOT_RECOMMENDED` fica fora do ranking principal.
- `RESTRICTED` fica fora por padrao.
- Sem mapeamento de uso por doenca/quadro nao gera compatibilidade presumida.
- Potencializador/adjuvante nao entra como substituto simples.
- Antidepressivo em monoterapia fica bloqueado diante de fenotipo maniforme ou contexto bipolar relevante.
- Insonia isolada nao vira indicacao automatica para antipsicotico.

## Regras de rebaixamento

- `OFF_LABEL_WITH_EVIDENCE` recebe penalidade e sinalizacao.
- `LIMITED_EVIDENCE` recebe penalidade e sinalizacao.

## Funcionamento sem diagnostico

Quando `diagnostic_context` esta vazio ou em investigacao, o app usa fenotipo/quadro clinico:

```text
Quadro depressivo sem diagnostico fechado
Quadro ansioso sem diagnostico fechado
Quadro maniforme/suspeita bipolar sem diagnostico fechado
```

O texto da interface muda para `Uso por quadro clinico`, sem apresentar a doenca como diagnostico confirmado.

## Funcionamento com diagnostico

Quando existe diagnostico/contexto informado, o filtro usa o mapeamento de `medication_disease_use_matrix.csv` para comparar:

- contexto/doenca;
- papel terapeutico;
- status;
- fase;
- fonte.

## Exemplos verificados

### Sem diagnostico fechado

Entrada: primeira consulta, humor deprimido, fadiga, sem medicacao atual.

Saida: `select_candidate`, `INITIAL_MONOTHERAPY`, fenotipo `DEPRESSIVE_SYNDROME`, uso exibido como quadro clinico sem diagnostico fechado.

### Contexto bipolar/maniforme

Entrada: transtorno bipolar em acompanhamento, humor elevado, impulsividade.

Saida: candidatos do ranking principal passam a ser estabilizadores/antipsicoticos compativeis; antidepressivos nao aparecem como monoterapia principal.

### Troca simples

Entrada: depressao em acompanhamento, sem resposta, receita atual com antidepressivo.

Saida: medicamentos mapeados apenas como potencializacao/adjuvancia nao entram como substitutos simples.

## Interface

Os quadros principais agora consomem:

- decisao/estrategia;
- justificativa com fenotipo e elegibilidade;
- estrategia/medicamento elegivel;
- faixa terapeutica e dose-efeito;
- objetivo clinico.

Blocos complementares mantem:

- `Dose - efeito`;
- `Uso por doenca` ou `Uso por quadro clinico`;
- fontes locais.

## Testes

Foram adicionados/atualizados testes para:

- fenotipo depressivo sem diagnostico fechado;
- contexto bipolar/maniforme sem antidepressivo em monoterapia no ranking principal;
- potencializador nao exibido como substituto simples;
- campos novos do contrato;
- interface com rotulo dinamico de uso por doenca/quadro.

Resultado:

```text
python -m unittest discover -s tests -t .
Ran 175 tests in 9.853s
OK
```

## Validacao localhost

```text
GET http://127.0.0.1:8765/health
{"status":"ok","mode":"read-only"}
```

Endpoint `/api/decision-support` validado com retorno de:

- `strategy_code`;
- `phenotype_summary`;
- `eligibility_summary`;
- `excluded_medications`;
- `disease_use_summary`.

## Limitacoes remanescentes

- O filtro depende da cobertura existente em `medication_disease_use_matrix.csv`.
- Campos sem fonte ou sem mapeamento continuam como nao elegiveis ou pendentes; nao ha preenchimento inventado.
- O motor permanece suporte a decisao medica e nao prescricao autonoma.

