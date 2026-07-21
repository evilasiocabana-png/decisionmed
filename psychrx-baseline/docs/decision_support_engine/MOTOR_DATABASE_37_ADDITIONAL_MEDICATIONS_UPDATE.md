# Atualizacao do Banco do Motor - 37 Medicamentos Adicionais

## Resultado

O banco do Motor Farmacologico foi ampliado de **46** para **83** itens.

## Medicamentos adicionados

- Alprazolam
- Bromazepam
- Clobazam
- Clonazepam
- Diazepam
- Lorazepam
- Midazolam
- Oxazepam
- Temazepam
- Zolpidem
- Zopiclona
- Eszopiclona
- Buspirona
- Metilfenidato IR
- Metilfenidato LP
- Lisdexanfetamina
- Atomoxetina
- Guanfacina XR
- Clonidina
- Paliperidona
- Ziprasidona
- Amissulprida
- Sulpirida
- Asenapina
- Cariprazina
- Brexpiprazol
- Acamprosato
- Dissulfiram
- Naloxona
- Buprenorfina
- Metadona
- Donepezila
- Rivastigmina
- Galantamina
- Memantina
- Prometazina
- Droperidol

## Arquivos atualizados

- `knowledge_base/decision_support_engine/tables/medication_explanation_profile_backlog.csv`
- `knowledge_base/decision_support_engine/tables/pharmacological_decision_matrix.csv`
- `knowledge_base/decision_support_engine/tables/medication_disease_use_matrix.csv`
- `knowledge_base/decision_support_engine/tables/medication_explanation_pending_audit.csv`
- `knowledge_base/decision_support_engine/tables/Tabela_Motor_Unificada_audit_evilasio.xlsx`

## Estado de revisao

Todos os 37 novos registros foram inseridos como **preliminares**, com status:

`source_reference_mapped_pending_formal_review`

Isso significa: fonte mapeada, mas ainda sem cadeia final `fonte -> secao -> trecho -> campo -> revisao`.

## Totais atuais

- Perfis dose-efeito: **83**
- Matriz farmacologica/ranking: **83**
- Linhas de uso por doenca/contexto: **345**
- Linhas de auditoria de pendencias: **83**

## Status de fonte no backlog

| Status | Linhas |
|---|---:|
| source_reference_mapped_pending_formal_review | 83 |

## Status de revisao em uso por doenca

| Status | Linhas |
|---|---:|
| REFERENCIA_MAPEADA_PENDENTE_REVISAO_FORMAL | 345 |

## Distribuicao por classe

| Classe | Medicamentos |
|---|---:|
| Agonista alfa-2 TDAH/autonomico | 1 |
| Agonista alfa-2A TDAH | 1 |
| Agonista opioide | 1 |
| Agonista parcial opioide | 1 |
| Ansiolitico nao benzodiazepinico | 1 |
| Antagonista NMDA | 1 |
| Antagonista opioide emergencia | 1 |
| Anticonvulsivante/estabilizador | 5 |
| Antihistaminico sedativo | 1 |
| Antipsicotico D2/D3 | 2 |
| Antipsicotico atipico | 9 |
| Antipsicotico atipico parcial D2/5HT1A | 1 |
| Antipsicotico atipico parcial D3/D2 | 1 |
| Antipsicotico de urgencia/antiemetico | 1 |
| Antipsicotico tipico | 4 |
| Atipico antidepressivo | 1 |
| Benzodiazepinico | 6 |
| Benzodiazepinico anticonvulsivante | 1 |
| Benzodiazepinico de urgencia/sedacao | 1 |
| Benzodiazepinico hipnotico | 1 |
| Dependencia quimica | 3 |
| Estabilizador de humor | 4 |
| Estimulante TDAH | 3 |
| Hipnotico Z | 3 |
| Inibidor acetilcolinesterase | 3 |
| NDRI | 2 |
| NaSSA | 1 |
| Nao estimulante TDAH | 1 |
| SARI | 1 |
| SNRI | 4 |
| SSRI | 3 |
| SSRI/serotonergico | 5 |
| Tetraciclico | 1 |
| Triciclico | 8 |

## Pendencias por campo apos atualizacao

| Campo | OK/preenchido | Pendente pesquisar | Nao cadastrado |
|---|---:|---:|---:|
| `dose_band` | 82 | 1 | 0 |
| `dominant_effect` | 39 | 44 | 0 |
| `receptor_or_mechanism` | 74 | 9 | 0 |
| `cognition_score` | 0 | 83 | 0 |
| `sedation_risk` | 23 | 37 | 23 |
| `weight_gain_risk` | 5 | 37 | 41 |
| `extrapyramidal_risk` | 5 | 37 | 41 |

## Observacao critica

Os novos grupos adicionados incluem benzodiazepinicos, hipnoticos Z, ansiolitico nao benzodiazepinico, medicamentos para TDAH, antipsicoticos adicionais, dependencia quimica/overdose, demencias e urgencia/agita??o.

Como o material enviado e uma matriz preliminar, a base foi atualizada para permitir consulta e desenvolvimento do motor, mas **nao libera uso como conhecimento clinico validado**.

## Lacunas

- Confirmar formulacao e bula aplicavel no Brasil para medicamentos controlados, injetaveis, nao comercializados regularmente ou dependentes de via/formulacao.
- Preencher `cognition_score`, `sedation_risk`, `weight_gain_risk` e `extrapyramidal_risk` com fonte revisavel quando aplicavel.
- Validar dose por indicacao antes de qualquer exibicao como faixa consolidada.

## Consistencia

Medicamentos esperados ausentes: nenhum.
