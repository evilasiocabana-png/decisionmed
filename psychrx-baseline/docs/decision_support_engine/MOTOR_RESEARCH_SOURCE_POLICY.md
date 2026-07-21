# Motor Research Source Policy

## Objetivo

Definir as fontes oficiais que podem sustentar a pesquisa, preenchimento e revisao dos campos pendentes do Motor Farmacologico do PsychRx.

Esta politica vale especialmente para:

- `medication_explanation_profile_backlog.csv`;
- `medication_explanation_pending_audit.csv`;
- futuras tabelas de perfil explicativo por medicamento;
- futuras respostas explicativas do conselho do motor.

## Regra Central

Nenhum campo pendente pode ser preenchido por inferencia livre.

Todo preenchimento deve possuir:

```text
fonte
-> edicao/ano/versao
-> secao/capitulo
-> trecho ou localizacao revisavel
-> campo preenchido
-> status de revisao
```

Se essa cadeia nao existir, o campo permanece:

```text
PENDENTE_PESQUISAR
```

## Fontes Oficiais por Funcao

| Fonte | Funcao no PsychRx |
|---|---|
| Stahl's Essential Psychopharmacology | Mecanismo de acao, receptores, farmacodinamica e racional psicofarmacologico |
| Stahl's Prescriber's Guide | Uso clinico, indicacoes, doses, efeitos adversos, monitorizacao, troca e associacao |
| Goodman & Gilman's The Pharmacological Basis of Therapeutics | Farmacologia de base, receptores, farmacodinamica, farmacocinetica e metabolismo |
| American Psychiatric Association Guidelines | Diretrizes clinicas por transtorno, indicacao e contexto terapeutico |
| NICE Guidelines | Algoritmos terapeuticos, sequencia de tratamento e evidencia aplicada |
| FDA / DailyMed | Bula oficial, dose, contraindicoes, advertencias, seguranca e monitorizacao regulatoria |
| EMA | Documento regulatorio, seguranca, autorizacao, alertas e informacao europeia |
| ANVISA | Bula, regulacao e alertas aplicaveis ao Brasil |

## Uso Preferencial por Campo

| Campo do motor | Fontes preferenciais |
|---|---|
| `receptor_or_mechanism` | Stahl Essential; Goodman & Gilman |
| `dominant_effect` | Stahl Essential; Stahl Prescriber's Guide; Goodman & Gilman |
| `dose_band` | Stahl Prescriber's Guide; FDA/DailyMed; EMA; ANVISA |
| `pharmacological_target` | Stahl Essential; Stahl Prescriber's Guide; Goodman & Gilman |
| `sedation_risk` | Stahl Prescriber's Guide; FDA/DailyMed; EMA; ANVISA |
| `weight_gain_risk` | Stahl Prescriber's Guide; FDA/DailyMed; EMA; ANVISA |
| `extrapyramidal_risk` | Stahl Prescriber's Guide; FDA/DailyMed; EMA; ANVISA |
| `cognition_score` | Stahl Essential; Stahl Prescriber's Guide; guideline quando aplicavel |
| indicacao/contexto clinico | APA; NICE; Stahl Prescriber's Guide |
| troca/associacao | Stahl Prescriber's Guide; APA; NICE |
| monitorizacao | Stahl Prescriber's Guide; FDA/DailyMed; EMA; ANVISA |

## Exemplo: Quetiapina

Para preencher faixas como:

```text
25-100 mg/dia
150-300 mg/dia
300-800 mg/dia
```

e associar cada faixa a sedacao, ansiolise, efeito antidepressivo, bloqueio D2 ou papel da norquetiapina, e necessario localizar a informacao em uma das fontes oficiais e registrar a localizacao.

Enquanto isso nao ocorrer, esses campos permanecem:

```text
PENDENTE_PESQUISAR
```

## Status Permitidos

| Status | Significado |
|---|---|
| `PENDENTE_PESQUISAR` | Campo identificado, mas sem fonte revisavel |
| `source_located` | Fonte localizada, mas ainda sem extracao validada |
| `extracted_draft` | Trecho extraido, ainda nao revisado |
| `scientific_review_pending` | Pendente de revisao cientifica |
| `editorial_review_pending` | Pendente de revisao editorial |
| `validated_for_table` | Validado para tabela de conhecimento |
| `runtime_blocked` | Validado como conhecimento, mas ainda bloqueado para runtime |

## Limites Permanentes

Esta politica nao autoriza:

- prescricao automatica;
- recomendacao terapeutica autonoma;
- escolha medicamentosa paciente-especifica sem revisao medica;
- inferencia sem fonte;
- uso de campos pendentes no runtime clinico.

## Regra de Atualizacao

Ao preencher qualquer campo pendente, atualizar tambem:

- tabela de origem;
- campo alterado;
- fonte;
- secao/capitulo;
- status;
- data de revisao;
- responsavel editorial, quando aplicavel.

