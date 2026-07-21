# Motor Farmacologico - Complemento dos 15 Medicamentos Prioritarios

## Objetivo

Registrar a incorporacao da primeira entrega de pesquisa dos 15 medicamentos prioritarios ao Motor Farmacologico.

## Arquivos atualizados

- `knowledge_base/decision_support_engine/tables/medication_explanation_profile_backlog.csv`
- `knowledge_base/decision_support_engine/tables/medication_explanation_pending_audit.csv`
- `knowledge_base/decision_support_engine/tables/Tabela_Motor_Unificada_audit_evilasio.xlsx`
- `tests/knowledge_base/test_decision_support_engine_tables.py`

## Medicamentos atualizados

| Medicamento | Cognicao | Sedacao | Peso | EPS | Status |
|---|---:|---:|---:|---:|---|
| Sertralina | 2 | 1 | 1 | 0 | source_located_pending_review |
| Fluoxetina | 2 | 0 | 0 | 0 | source_located_pending_review |
| Escitalopram | 2 | 1 | 2 | 0 | source_located_pending_review |
| Duloxetina | 2 | 1 | 2 | 0 | source_located_pending_review |
| Venlafaxina | 2 | 1 | 1 | 0 | source_located_pending_review |
| Mirtazapina | 1 | 4 | 4 | 0 | source_located_pending_review |
| Bupropiona | 3 | 0 | 0 | 0 | source_located_pending_review |
| Quetiapina | 1 | 4 | 3 | 1 | source_located_pending_review |
| Aripiprazol | 2 | 1 | 1 | 2 | source_located_pending_review |
| Lurasidona | 2 | 1 | 1 | 2 | source_located_pending_review |
| Olanzapina | 1 | 3 | 4 | 1 | source_located_pending_review |
| Risperidona | 1 | 2 | 3 | 3 | source_located_pending_review |
| Litio | 1 | 1 | 2 | 0 | source_located_pending_review |
| Valproato | 1 | 2 | 3 | 0 | source_located_pending_review |
| Lamotrigina | 3 | 1 | 0 | 0 | source_located_pending_review |

## Campos complementados

Para cada medicamento prioritario foram atualizados, quando fornecidos:

- `cognition_score`
- `sedation_risk`
- `weight_gain_risk`
- `extrapyramidal_risk`
- `dominant_effect`
- `receptor_or_mechanism`
- `dose_band`
- `source_reference`
- `source_required`
- `current_source_status`

## Estado de revisao

O status usado foi `source_located_pending_review`, conforme a entrega recebida. Isso significa que a fonte foi localizada/mapeada, mas ainda requer revisao medica/cientifica final antes de promocao para `validated_for_table`.

## Limite

Esta atualizacao nao cria prescricao automatica, nao habilita runtime clinico autonomo e nao transforma o motor em recomendador final. O app continua como suporte a decisao medica.
