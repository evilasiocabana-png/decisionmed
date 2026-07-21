# Motor 2 Missing Range Audit

Auditoria gerada a partir de `knowledge_base/decision_support_engine/tables/motor2_strategy_matrix.csv`.

## Resumo

- Linhas totais: 1444
- OK_CONDITION_RANGE: 1007
- RESEARCH_REQUIRED_NO_COMPARABLE_RANGE: 55
- USE_DOSE_EFFECT_PENDING_CONDITION_RANGE: 382

## Interpretacao

- `OK_CONDITION_RANGE`: ja existe faixa por quadro e pode ser comparada diretamente.
- `USE_DOSE_EFFECT_PENDING_CONDITION_RANGE`: nao existe faixa por quadro, mas existe dose-efeito com fonte; o app deve usar como comparacao provisoria explicita, sem fingir que e quadro validado.
- `DOSE_EFFECT_WITH_SOURCE_GAP`: existe dose-efeito, mas a fonte precisa revisao formal.
- `RESEARCH_REQUIRED_NO_COMPARABLE_RANGE`: falta faixa por quadro e falta dose-efeito comparavel; exige pesquisa oficial antes de responder dose/conduta.

## Campos mais pendentes

- `condition_range`: 437
- `condition_range_min`: 437
- `condition_range_max`: 437
- `range_source`: 437
- `dominant_effect`: 297
- `mechanism_or_target`: 227
- `condition_key`: 226
- `dose_effect_band`: 167
- `dose_effect_source`: 139
- `strategy_if_range_missing`: 45
- `dose_effect_min`: 24
- `dose_effect_max`: 24

## Medicamentos com mais pendencias de faixa

- Risperidona: 24 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=24)
- Topiramato: 21 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=21)
- Olanzapina: 21 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=21)
- Aripiprazol: 21 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=21)
- Oxcarbazepina: 16 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=16)
- Mirtazapina: 16 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=16)
- Quetiapina: 15 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=15)
- Lamotrigina: 15 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=15)
- Clozapina: 15 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=15)
- Amitriptilina: 15 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=15)
- Haloperidol: 12 linhas pendentes (RESEARCH_REQUIRED_NO_COMPARABLE_RANGE=4, USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=8)
- Clorpromazina: 12 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=12)
- Carbamazepina: 12 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=12)
- Litio: 10 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=10)
- Levomepromazina: 9 linhas pendentes (RESEARCH_REQUIRED_NO_COMPARABLE_RANGE=9)
- Venlafaxina XR: 8 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=8)
- Trazodona: 8 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=8)
- Lurasidona: 8 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=8)
- Doxepina: 8 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=8)
- Valproato: 7 linhas pendentes (RESEARCH_REQUIRED_NO_COMPARABLE_RANGE=7)
- Venlafaxina: 6 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=6)
- Tioridazina: 6 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=6)
- Naltrexona: 6 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=6)
- Mianserina: 6 linhas pendentes (RESEARCH_REQUIRED_NO_COMPARABLE_RANGE=6)
- Desipramina: 6 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=6)
- Agomelatina: 6 linhas pendentes (RESEARCH_REQUIRED_NO_COMPARABLE_RANGE=6)
- Vortioxetina: 5 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=5)
- Lorazepam: 5 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=5)
- Vilazodona: 4 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=4)
- Diazepam: 4 linhas pendentes (USE_DOSE_EFFECT_PENDING_CONDITION_RANGE=4)

## Proximo preenchimento seguro

1. Corrigir campos com dose-efeito ja rastreavel, usando a dose-efeito como faixa operacional provisoria.
2. Pesquisar fontes oficiais para `RESEARCH_REQUIRED_NO_COMPARABLE_RANGE`.
3. Promover para faixa por quadro apenas quando houver par medicamento + quadro + faixa + fonte.

Arquivo detalhado: `docs/decision_support_engine/MOTOR2_MISSING_RANGE_AUDIT.csv`
