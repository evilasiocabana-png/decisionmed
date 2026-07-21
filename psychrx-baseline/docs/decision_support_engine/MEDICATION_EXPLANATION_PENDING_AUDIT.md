# Medication Explanation Pending Audit

## Objetivo

Auditar todos os medicamentos do backlog de enriquecimento farmacologico e listar campos pendentes de pesquisa e campos nao cadastrados na Tabela Motor.

## Escopo

- Fonte auditada: `knowledge_base/decision_support_engine/tables/medication_explanation_profile_backlog.csv`.
- As 8 tabelas originais nao foram alteradas.
- A Tabela Motor ativa nao foi alterada.
- `PENDENTE_PESQUISAR` significa que falta fonte externa revisavel.
- `nao cadastrado` significa que a Tabela Motor/local foi consultada e nao trouxe esse campo.
- Todo campo preenchido ou marcado como nao cadastrado possui coluna de fonte correspondente.

## Resumo Executivo

- Medicamentos auditados: 46.
- Linhas de backlog auditadas: 46.

## Distribuicao por Classe

- Triciclico: 8
- Antipsicotico atipico: 6
- Anticonvulsivante/estabilizador: 5
- SSRI/serotonergico: 5
- Antipsicotico tipico: 4
- Estabilizador de humor: 4
- SNRI: 4
- SSRI: 3
- NDRI: 2
- Atipico antidepressivo: 1
- Dependencia quimica: 1
- NaSSA: 1
- SARI: 1
- Tetraciclico: 1

## Campos Pendentes de Pesquisa

- dose_band: 46 medicamentos
- dominant_effect: 46 medicamentos
- receptor_or_mechanism: 46 medicamentos
- cognition_score: 46 medicamentos

## Campos Nao Cadastrados na Tabela Motor

- weight_gain_risk: 41 medicamentos
- extrapyramidal_risk: 41 medicamentos
- sedation_risk: 23 medicamentos

## Auditoria por Medicamento

| Medicamento | Classe | Ja temos | Pendente pesquisar | Nao cadastrado | Fonte local |
|---|---|---|---|---|---|
| Agomelatina | Atipico antidepressivo | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Amitriptilina | Triciclico | sedation_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Aripiprazol | Antipsicotico atipico | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 5 |
| Bupropiona | NDRI | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Bupropiona XL | NDRI | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Carbamazepina | Estabilizador de humor | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 7<br>Tabela 8 |
| Citalopram | SSRI/serotonergico | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Clomipramina | Triciclico | sedation_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Clorpromazina | Antipsicotico tipico | sedation_risk <br> extrapyramidal_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk | Tabela 3 |
| Clozapina | Antipsicotico atipico | sedation_risk <br> weight_gain_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | extrapyramidal_risk | Tabela 5 |
| Desipramina | Triciclico | sedation_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk <br> extrapyramidal_risk | Tabela 2 |
| Desvenlafaxina | SNRI | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Divalproato | Anticonvulsivante/estabilizador | sedation_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk <br> extrapyramidal_risk | Tabela 8 |
| Dosulepina | Triciclico | sedation_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk <br> extrapyramidal_risk | Tabela 1 |
| Doxepina | Triciclico | sedation_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Duloxetina | SNRI | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Escitalopram | SSRI | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Fenitoina | Anticonvulsivante/estabilizador | sedation_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk <br> extrapyramidal_risk | Tabela 7<br>Tabela 8 |
| Fenobarbital | Anticonvulsivante/estabilizador | sedation_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk <br> extrapyramidal_risk | Tabela 7<br>Tabela 8 |
| Fluoxetina | SSRI | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Fluvoxamina | SSRI/serotonergico | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Haloperidol | Antipsicotico tipico | sedation_risk <br> extrapyramidal_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk | Tabela 3 |
| Imipramina | Triciclico | sedation_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Lamotrigina | Estabilizador de humor | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 7<br>Tabela 8 |
| Levomepromazina | Antipsicotico tipico | sedation_risk <br> extrapyramidal_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk | Tabela 3 |
| Litio | Estabilizador de humor | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 7<br>Tabela 8 |
| Lurasidona | Antipsicotico atipico | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 5<br>Tabela 8 |
| Maprotilina | Triciclico | sedation_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Mianserina | Tetraciclico | sedation_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Mirtazapina | NaSSA | sedation_risk <br> weight_gain_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Naltrexona | Dependencia quimica | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 8 |
| Nortriptilina | Triciclico | sedation_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Olanzapina | Antipsicotico atipico | sedation_risk <br> weight_gain_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | extrapyramidal_risk | Tabela 5 |
| Oxcarbazepina | Anticonvulsivante/estabilizador | sedation_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk <br> extrapyramidal_risk | Tabela 7 |
| Paroxetina | SSRI/serotonergico | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Quetiapina | Antipsicotico atipico | sedation_risk <br> weight_gain_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | extrapyramidal_risk | Tabela 5 |
| Risperidona | Antipsicotico atipico | weight_gain_risk <br> extrapyramidal_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk | Tabela 5 |
| Sertralina | SSRI | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Tioridazina | Antipsicotico tipico | sedation_risk <br> extrapyramidal_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk | Tabela 3 |
| Topiramato | Anticonvulsivante/estabilizador | sedation_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk <br> extrapyramidal_risk | Tabela 8 |
| Trazodona | SARI | sedation_risk <br> drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Valproato | Estabilizador de humor | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 7<br>Tabela 8 |
| Venlafaxina | SNRI | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Venlafaxina XR | SNRI | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Vilazodona | SSRI/serotonergico | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |
| Vortioxetina | SSRI/serotonergico | drug_class <br> pharmacological_target <br> anxiety_score <br> sleep_score <br> mood_score <br> energy_score <br> source_reference | dose_band <br> dominant_effect <br> receptor_or_mechanism <br> cognition_score | sedation_risk <br> weight_gain_risk <br> extrapyramidal_risk | Tabela 1<br>Tabela 2 |

## Proxima Acao Recomendada

Pesquisar primeiro os campos `PENDENTE_PESQUISAR`. Campos `nao cadastrado` so devem mudar se uma fonte ou revisao da Tabela Motor trouxer informacao nova.
