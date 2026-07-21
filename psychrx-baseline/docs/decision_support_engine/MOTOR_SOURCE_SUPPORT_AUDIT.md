# Motor Farmacologico - Auditoria de Suporte por Fontes

## Escopo

Auditoria completa dos artefatos atuais do Motor Farmacologico do PsychRx, sem alterar a base cientifica nem a planilha.

Arquivos auditados:

- `knowledge_base/decision_support_engine/tables/Tabela_Motor_Unificada_audit_evilasio.xlsx`
- `knowledge_base/decision_support_engine/tables/Tabela_Motor_Abas_Unificadas_audit_evilasio.xlsx`
- `knowledge_base/decision_support_engine/tables/medication_explanation_profile_backlog.csv`
- `knowledge_base/decision_support_engine/tables/medication_explanation_pending_audit.csv`
- `knowledge_base/decision_support_engine/tables/medication_disease_use_matrix.csv`
- `knowledge_base/decision_support_engine/tables/pharmacological_decision_matrix.csv`
- `knowledge_base/decision_support_engine/tables/medication_source_legend.csv`

## Conclusao executiva

O motor possui uma base local ampla e estruturada, mas ainda nao esta cientificamente fechado.

- Medicamentos auditados: **46**.
- Linhas de uso por doenca/quadro: **249**.
- Entradas da matriz farmacologica/ranking: **46**.
- Entradas de dose-efeito na planilha unificada: **46**.
- Todas as entradas de `Uso por Doenca` estao com status **REFERENCIA_MAPEADA_PENDENTE_REVISAO_FORMAL**.
- Todas as entradas de `Dose - Efeito` estao com status **REFERENCIA_MAPEADA_PENDENTE_REVISAO_FORMAL**.
- A matriz farmacologica esta com status **draft_from_source_audit** para os 46 medicamentos.

Interpretacao: a informacao tem suporte local e referencias externas mapeadas, mas a maioria ainda nao possui a cadeia completa `fonte -> secao -> trecho -> campo -> revisao`. Portanto, deve permanecer como suporte a decisao em revisao, nao como conhecimento clinico validado para runtime autonomo.

## Fontes oficiais previstas pela politica do projeto

- `TM`: Tabela Motor / tabelas locais do PsychRx (local_curated)
- `T1-T8`: Planilhas originais 1 a 8 do Motor Farmacologico (local_curated)
- `DM`: FDA / DailyMed (official_regulatory)
- `ST-E`: Stahl's Essential Psychopharmacology (official_reference_required)
- `ST-PG`: Stahl's Prescriber's Guide (official_reference_required)
- `GG`: Goodman & Gilman's The Pharmacological Basis of Therapeutics (official_reference_required)
- `APA`: American Psychiatric Association Guidelines (official_guideline)
- `NICE`: National Institute for Health and Care Excellence Guidelines (official_guideline)
- `EMA`: European Medicines Agency (official_regulatory)
- `ANVISA`: ANVISA (official_regulatory)
- `PENDENTE_PESQUISAR`: Fonte ainda nao localizada ou trecho ainda nao revisado (blocked_for_runtime)

## Verificacao externa pontual de fontes-base

Foram checadas fontes externas oficiais e primarias para validar se o tipo de fonte usado pelo motor e coerente:

- NICE NG222 cobre tratamento e manejo de depressao em adultos e foi revisado em 2026: https://www.nice.org.uk/guidance/ng222
- NICE CG185 cobre avaliacao e manejo do transtorno bipolar: https://www.nice.org.uk/guidance/cg185
- NICE CG178 cobre psicose e esquizofrenia em adultos: https://www.nice.org.uk/guidance/cg178
- DailyMed/FDA disponibiliza bula oficial de sertralina, incluindo dose inicial, intervalo de ajuste e maximo diario: https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=6c26a87a-b2b6-4302-bb8d-2031461f28ce
- DailyMed/FDA disponibiliza bula de mirtazapina com inicio 15 mg e aumento ate 45 mg/dia: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=98ad1917-a094-44f5-a28f-a64a8cfcd887
- DailyMed/FDA disponibiliza bula de quetiapina com faixas distintas por indicacao/formulacao: https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=874e50ad-5da0-4ac3-9290-79442c91399e
- EMA Valdoxan confirma agomelatina, indicacao em episodio depressivo maior adulto, mecanismo MT1/MT2 e 5-HT2C, e documentacao regulatoria europeia: https://www.ema.europa.eu/en/medicines/human/EPAR/valdoxan

Essas fontes confirmam que o conjunto de fontes escolhido pelo PsychRx e adequado. Elas nao substituem a revisao linha a linha ainda pendente.

## Distribuicao por classe

| Classe | Medicamentos |
|---|---:|
| Anticonvulsivante/estabilizador | 5 |
| Antipsicotico atipico | 6 |
| Antipsicotico tipico | 4 |
| Atipico antidepressivo | 1 |
| Dependencia quimica | 1 |
| Estabilizador de humor | 4 |
| NDRI | 2 |
| NaSSA | 1 |
| SARI | 1 |
| SNRI | 4 |
| SSRI | 3 |
| SSRI/serotonergico | 5 |
| Tetraciclico | 1 |
| Triciclico | 8 |

## Auditoria por campo do perfil explicativo

| Campo | OK/local preenchido | Pendente pesquisar/revisar | Nao cadastrado | Fonte mapeada |
|---|---:|---:|---:|---:|
| `dose_band` | 45 | 1 | 0 | 46 |
| `dominant_effect` | 39 | 7 | 0 | 46 |
| `pharmacological_target` | 46 | 0 | 0 | 46 |
| `receptor_or_mechanism` | 39 | 7 | 0 | 46 |
| `anxiety_score` | 46 | 0 | 0 | 46 |
| `sleep_score` | 46 | 0 | 0 | 46 |
| `mood_score` | 46 | 0 | 0 | 46 |
| `energy_score` | 46 | 0 | 0 | 46 |
| `cognition_score` | 0 | 46 | 0 | 46 |
| `sedation_risk` | 23 | 0 | 23 | 46 |
| `weight_gain_risk` | 5 | 0 | 41 | 46 |
| `extrapyramidal_risk` | 5 | 0 | 41 | 46 |

Leitura critica:

- `cognition_score` aparece como pendente em **46/46** medicamentos.
- `weight_gain_risk` e `extrapyramidal_risk` aparecem como nao cadastrados em **41/46** medicamentos.
- `sedation_risk` aparece como nao cadastrado em **23/46** medicamentos.
- `dominant_effect` e `receptor_or_mechanism` ainda possuem pendencia em **7/46** medicamentos.
- Todas as colunas de fonte estao preenchidas, mas isso significa fonte mapeada, nao validacao cientifica final.

## Uso por doenca/quadro

### Status das linhas

| Status | Linhas |
|---|---:|
| nao_recomendado_como_principal | 46 |
| principal_ou_conforme_diretriz | 41 |
| principal_guideline_or_regulatory | 33 |
| principal_ou_conforme_contexto | 19 |
| contextual | 19 |
| bloquear_sem_avaliacao_de_risco | 16 |
| perfil_sintomatico | 13 |
| principal_ou_contextual | 12 |
| adjuvante_selecionado | 8 |
| neurologico_principal | 8 |
| off_label_ou_contextual | 6 |
| principal_off_label_ou_evidencia_variavel | 4 |
| nao_ranking_rotineiro_sem_regra | 4 |
| principal_ou_conforme_evidencia | 4 |
| evidencia_limitada_ou_contextual | 2 |
| nao_recomendado_como_central | 2 |
| principal_conforme_avaliacao | 2 |
| off_label_contextual | 2 |
| nao_recomendado_como_rotina | 2 |
| principal_conforme_formulacao | 2 |
| associado_a_olanzapina_conforme_contexto | 1 |
| restrito_com_monitorizacao_obrigatoria | 1 |
| nao_recomendado_como_geral | 1 |
| nao_recomendado_como_equivalente | 1 |

### Status de revisao

| Status de revisao | Linhas |
|---|---:|
| REFERENCIA_MAPEADA_PENDENTE_REVISAO_FORMAL | 249 |

### Referencias declaradas

| Fonte declarada | Linhas |
|---|---:|
| Texto fundador Uso por Doenca; NICE/Guideline quando indicado | 200 |
| NICE NG222; texto fundador | 26 |
| NICE CG178; texto fundador | 10 |
| NICE CG185; texto fundador | 7 |
| NICE NG222/CANMAT/APA conforme caso; texto fundador | 5 |
| NICE CG115; texto fundador | 1 |

Conclusao: o modulo `Uso por Doenca` ja consegue filtrar por diagnostico/quadro, mas ainda esta editorialmente pendente. Ele pode orientar o ranking como rascunho, mas nao deve ser tratado como validado.

## Cobertura por medicamento

| Medicamento | Classe | Campos OK | Campos pendentes | Campos nao cadastrados | Linhas uso por doenca | Status matriz |
|---|---|---:|---:|---:|---:|---|
| Agomelatina | Atipico antidepressivo | 8 | 1 | 3 | 2 | draft_from_source_audit |
| Amitriptilina | Triciclico | 7 | 3 | 2 | 8 | draft_from_source_audit |
| Aripiprazol | Antipsicotico atipico | 6 | 3 | 3 | 7 | draft_from_source_audit |
| Bupropiona | NDRI | 8 | 1 | 3 | 6 | draft_from_source_audit |
| Bupropiona XL | NDRI | 8 | 1 | 3 | 4 | draft_from_source_audit |
| Carbamazepina | Estabilizador de humor | 8 | 1 | 3 | 6 | draft_from_source_audit |
| Citalopram | SSRI/serotonergico | 8 | 1 | 3 | 6 | draft_from_source_audit |
| Clomipramina | Triciclico | 9 | 1 | 2 | 5 | draft_from_source_audit |
| Clorpromazina | Antipsicotico tipico | 10 | 1 | 1 | 4 | draft_from_source_audit |
| Clozapina | Antipsicotico atipico | 10 | 1 | 1 | 3 | draft_from_source_audit |
| Desipramina | Triciclico | 9 | 1 | 2 | 2 | draft_from_source_audit |
| Desvenlafaxina | SNRI | 8 | 1 | 3 | 5 | draft_from_source_audit |
| Divalproato | Anticonvulsivante/estabilizador | 9 | 1 | 2 | 6 | draft_from_source_audit |
| Dosulepina | Triciclico | 9 | 1 | 2 | 2 | draft_from_source_audit |
| Doxepina | Triciclico | 9 | 1 | 2 | 5 | draft_from_source_audit |
| Duloxetina | SNRI | 8 | 1 | 3 | 8 | draft_from_source_audit |
| Escitalopram | SSRI | 8 | 1 | 3 | 9 | draft_from_source_audit |
| Fenitoina | Anticonvulsivante/estabilizador | 9 | 1 | 2 | 3 | draft_from_source_audit |
| Fenobarbital | Anticonvulsivante/estabilizador | 9 | 1 | 2 | 3 | draft_from_source_audit |
| Fluoxetina | SSRI | 8 | 1 | 3 | 12 | draft_from_source_audit |
| Fluvoxamina | SSRI/serotonergico | 8 | 1 | 3 | 6 | draft_from_source_audit |
| Haloperidol | Antipsicotico tipico | 9 | 2 | 1 | 4 | draft_from_source_audit |
| Imipramina | Triciclico | 9 | 1 | 2 | 4 | draft_from_source_audit |
| Lamotrigina | Estabilizador de humor | 6 | 3 | 3 | 5 | draft_from_source_audit |
| Levomepromazina | Antipsicotico tipico | 10 | 1 | 1 | 3 | draft_from_source_audit |
| Litio | Estabilizador de humor | 8 | 1 | 3 | 5 | draft_from_source_audit |
| Lurasidona | Antipsicotico atipico | 6 | 3 | 3 | 4 | draft_from_source_audit |
| Maprotilina | Triciclico | 9 | 1 | 2 | 2 | draft_from_source_audit |
| Mianserina | Tetraciclico | 7 | 3 | 2 | 4 | draft_from_source_audit |
| Mirtazapina | NaSSA | 8 | 3 | 1 | 7 | draft_from_source_audit |
| Naltrexona | Dependencia quimica | 8 | 1 | 3 | 3 | draft_from_source_audit |
| Nortriptilina | Triciclico | 9 | 1 | 2 | 3 | draft_from_source_audit |
| Olanzapina | Antipsicotico atipico | 10 | 1 | 1 | 7 | draft_from_source_audit |
| Oxcarbazepina | Anticonvulsivante/estabilizador | 9 | 1 | 2 | 4 | draft_from_source_audit |
| Paroxetina | SSRI/serotonergico | 8 | 1 | 3 | 10 | draft_from_source_audit |
| Quetiapina | Antipsicotico atipico | 10 | 1 | 1 | 10 | draft_from_source_audit |
| Risperidona | Antipsicotico atipico | 10 | 1 | 1 | 6 | draft_from_source_audit |
| Sertralina | SSRI | 8 | 1 | 3 | 10 | draft_from_source_audit |
| Tioridazina | Antipsicotico tipico | 10 | 1 | 1 | 2 | draft_from_source_audit |
| Topiramato | Anticonvulsivante/estabilizador | 7 | 3 | 2 | 7 | draft_from_source_audit |
| Trazodona | SARI | 9 | 1 | 2 | 5 | draft_from_source_audit |
| Valproato | Estabilizador de humor | 8 | 1 | 3 | 7 | draft_from_source_audit |
| Venlafaxina | SNRI | 8 | 1 | 3 | 9 | draft_from_source_audit |
| Venlafaxina XR | SNRI | 8 | 1 | 3 | 9 | draft_from_source_audit |
| Vilazodona | SSRI/serotonergico | 8 | 1 | 3 | 3 | draft_from_source_audit |
| Vortioxetina | SSRI/serotonergico | 8 | 1 | 3 | 4 | draft_from_source_audit |

## Gaps principais

1. A planilha tem **suporte local** nas tabelas 1-8, mas muitos campos ainda nao tem suporte externo validado.
2. O campo `Tabela Motor` da planilha unificada possui 19 linhas resumidas; a cobertura completa dos 46 medicamentos esta distribuida nas abas `Dose - Efeito`, `Uso por Doenca` e CSVs derivados.
3. `Dose - Efeito` foi enriquecido para todos os 46 medicamentos, mas todos ainda estao como `REFERENCIA_MAPEADA_PENDENTE_REVISAO_FORMAL`.
4. `Uso por Doenca` contem 249 linhas, todas pendentes de revisao formal.
5. A matriz de ranking farmacologico contem 46 medicamentos, mas o status e `draft_from_source_audit`.
6. Informacoes como cognicao, peso, EPS e sedacao ainda nao estao suficientemente completas para todos os medicamentos.

## Regra de seguranca recomendada

No app, qualquer texto do motor que dependa de campo com status `REFERENCIA_MAPEADA_PENDENTE_REVISAO_FORMAL`, `draft_from_source_audit`, `PENDENTE_PESQUISAR` ou `nao cadastrado` deve ser exibido como apoio em revisao, nao como recomendacao final.

## Proxima etapa recomendada

Executar uma missao de validacao por lote, nao por medicamento isolado:

1. Priorizar medicamentos mais usados no app: sertralina, fluoxetina, escitalopram, duloxetina, venlafaxina, mirtazapina, bupropiona, quetiapina, aripiprazol, lurasidona, olanzapina, risperidona, litio, valproato, lamotrigina.
2. Para cada um, preencher a cadeia completa:
   `fonte -> secao/capitulo -> trecho/localizacao -> campo -> status de revisao`.
3. Atualizar status de `REFERENCIA_MAPEADA_PENDENTE_REVISAO_FORMAL` para `validated_for_table` apenas quando houver revisao.
4. Manter campos sem fonte como `PENDENTE_PESQUISAR`.
5. Reexecutar os testes e gerar nova auditoria.

## Arquivo detalhado

Tabela detalhada por medicamento: `docs/decision_support_engine/MOTOR_SOURCE_SUPPORT_AUDIT_TABLE.csv`.
