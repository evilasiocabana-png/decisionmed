# Motor Flow Audit

Status: auditado em modo local

## Escopo

Auditoria da Tabela Motor e do fluxo do conselho exibido no app PsychRx.

Arquivos auditados:

- `knowledge_base/decision_support_engine/tables/pharmacological_decision_matrix.csv`
- `knowledge_base/decision_support_engine/tables/medication_explanation_profile_backlog.csv`
- `knowledge_base/decision_support_engine/tables/medication_disease_use_matrix.csv`
- `knowledge_base/decision_support_engine/tables/antidepressant_indication_matrix_table1.csv`
- `knowledge_base/decision_support_engine/tables/Tabela_Motor_Unificada_audit_evilasio.xlsx`
- `application/decision_support_rule_table.py`
- `application/medication_dose_profile_table.py`
- `application/medication_disease_use_table.py`
- `interfaces/web/static/app.js`

## Estado da base

### Cobertura medicamentosa

- Medicamentos na matriz farmacologica: 46.
- Medicamentos com perfil Dose - efeito: 46.
- Medicamentos com Uso por doenca: 46.
- Medicamentos sem perfil Dose - efeito: 0.
- Medicamentos sem fonte mapeada no perfil Dose - efeito: 0.

### Tabelas principais

| Tabela | Linhas | Funcao |
|---|---:|---|
| `pharmacological_decision_matrix.csv` | 46 | ranking por perfil farmacologico desejado |
| `medication_explanation_profile_backlog.csv` | 46 | Dose - efeito, fonte, mecanismo e explicacao por medicamento |
| `medication_disease_use_matrix.csv` | 249 | uso por doenca/contexto, papel e status |
| `antidepressant_indication_matrix_table1.csv` | 23 | faixa terapeutica por quadro para antidepressivos da aba 1 |

### Planilha unificada

Abas confirmadas:

- `Fluxo do App`
- `Tabela Motor`
- `Regras de Decisao`
- `Perguntas Derivadas`
- `Mapa das 8 Tabelas`
- `Dose - Efeito`
- `Regras Perfil Dose`
- `Uso por Doenca`
- `Regras Uso Doenca`

## Fluxo atual do motor

Fluxo executado no app:

```text
UI
↓
ClinicalDecisionSupportService
↓
DecisionSupportRuleTable
↓
PharmacologicalDecisionMatrix
↓
AntidepressantIndicationDoseMatrix
↓
MedicationDoseProfileTable
↓
MedicationDiseaseUseTable
↓
ClinicalDecisionSupportResponse
↓
Card Conselho do motor
```

## O que esta condizente

1. O app coleta contexto clinico, sintomas, prejuizo, objetivo, receita e seguranca antes do conselho.
2. O motor gera decisao pratica: manter, otimizar, substituir, associar, investigar ou retirar gradualmente.
3. O ranking farmacologico usa a matriz local de perfil desejado.
4. A faixa terapeutica por quadro e consultada quando o medicamento existe na matriz da aba 1.
5. O card `Faixa terapeutica` mostra:
   - faixa por quadro;
   - Dose - efeito;
   - classificacao do motor;
   - mecanismo/alvo.
6. O conselho mostra `Uso por doenca`.
7. Todos os 46 medicamentos possuem Dose - efeito e Uso por doenca.

## Pontos de atencao

### 1. Uso por doenca ainda e exibicao, nao filtro ativo

A matriz `medication_disease_use_matrix.csv` esta conectada ao conselho, mas ainda nao filtra o ranking.

Exemplo:

```text
Sertralina
→ mostra usos: depressao maior, TAG, panico, ansiedade social.
```

Isso e correto como informacao, mas ainda nao impede que um medicamento apareca fora do papel adequado.

Recomendacao:

```text
Adicionar filtro por papel/status:
tratamento_principal
potencializacao
manutencao
uso_restrito
off_label
nao_recomendado
```

### 2. Faixa por quadro cobre principalmente antidepressivos da aba 1

`antidepressant_indication_matrix_table1.csv` tem 23 medicamentos. Para antipsicoticos, estabilizadores e anticonvulsivantes, muitas faixas por quadro ainda caem como:

```text
faixa por quadro: nao cadastrado
```

Isso e aceitavel no estado atual, mas limita a precisao do card para quetiapina, lurasidona, olanzapina, litio, valproato etc.

Recomendacao:

```text
Criar matrizes equivalentes por classe:
- antipsicoticos por indicacao
- estabilizadores por fase bipolar
- anticonvulsivantes por uso neurologico/psiquiatrico
```

### 3. Dose - efeito esta mapeado, mas ainda pendente de revisao formal

Todos os medicamentos receberam texto Dose - efeito e referencias. O status correto e:

```text
source_reference_mapped_pending_formal_review
```

Isso significa que o motor pode exibir como apoio informativo, mas ainda precisa de revisao fina por fonte/trecho para virar regra forte.

### 4. Uso por doenca mostra as primeiras quatro linhas do medicamento

Hoje o app mostra ate quatro usos do medicamento selecionado/candidato. Isso pode ser util, mas ainda nao esta priorizado pelo contexto atual da consulta.

Exemplo:

```text
Bupropiona
→ depressao maior
→ baixa energia
→ anorexia nervosa nao principal
→ tabagismo
```

Recomendacao:

```text
Ordenar os usos por compatibilidade com:
- objetivo principal
- sintomas predominantes
- diagnostico informado
- fase do tratamento
```

## Veredito

O fluxo esta funcional e coerente como motor de apoio local.

Mas ainda ha uma diferenca entre:

```text
mostrar informacao farmacologica
```

e

```text
usar essa informacao como regra ativa de decisao
```

Estado atual:

```text
Base: boa
Cobertura: boa
Exibicao: boa
Rastreabilidade: intermediaria
Motor decisorio: parcialmente integrado
```

## Proxima melhoria recomendada

Implementar a etapa:

```text
Disease Use Filter
```

Objetivo:

Antes de montar o ranking final, o motor deve verificar se o medicamento e:

- tratamento principal para o quadro;
- potencializador;
- manutencao;
- uso restrito;
- off-label;
- nao recomendado para aquele contexto.

Com isso, o conselho deixa de apenas informar e passa a evitar rankings incoerentes.

