# ADR 0009 - Clinical Experience Precedes Dashboard

## Status

Aceito.

## Data

2026-06-30

## Contexto

Depois da execucao do Programa 06, a proxima missao automatica apontava para:

```text
MISSION 120 - Desktop Layout
PROGRAM 08 - Dashboard
```

Essa sequencia criaria risco arquitetural, porque o Dashboard e consumidor visual da experiencia clinica. Ele nao deve definir a experiencia, os componentes clinicos reutilizaveis ou o fluxo de consulta.

Ainda faltam componentes implementaveis ou especificaveis da Clinical Experience Layer, como:

- Clinical Context;
- Clinical Card Stack;
- Live Question Panel;
- Consultation Flow;
- Clinical Snapshot ViewModel;
- cards reutilizaveis de consulta.

Sem esses elementos, o Dashboard tenderia a ficar estatico, duplicado ou responsavel por logica que deve nascer na Clinical Experience Layer.

## Decisao

Bloquear temporariamente o inicio do Programa 08 - Dashboard.

Executar primeiro a expansao do:

```text
PROGRAM 07 - Clinical Experience Layer
```

A nova ordem estrategica passa a ser:

```text
PROGRAM 06 - Software Platform
-> PROGRAM 07 - Clinical Experience Layer
-> PROGRAM 08 - Dashboard
-> PROGRAM 09 - Mobile Experience
-> PROGRAM 10 - Clinical Kernel Integration
-> PROGRAM 11 - Clinical Reasoning Engines
```

## Justificativa

Dashboard e representacao visual.

Clinical Experience e a experiencia da consulta.

Como desktop, tablet e mobile deverao reutilizar componentes da Clinical Experience Layer, a experiencia deve ser definida antes das superficies visuais finais.

Essa decisao reduz:

- duplicacao de componentes;
- retrabalho de UI;
- mistura entre dashboard e logica de consulta;
- risco de interface decidir conduta;
- inconsistencia entre desktop, tablet e mobile.

## Alternativas Consideradas

### Seguir para Program 08 - Dashboard

Rejeitada. O Dashboard consumiria componentes ainda inexistentes ou incompletos.

### Implementar Dashboard e Clinical Experience juntos

Rejeitada. Misturaria apresentacao visual com arquitetura de experiencia de consulta.

### Expandir Program 07 antes do Dashboard

Aceita. Permite criar componentes reutilizaveis primeiro e deixar o Dashboard apenas como superficie apresentacional.

## Impacto

- `NEXT_MISSION.md` passa a apontar para `MISSION 144 - Consultation Layout`.
- `PROJECT_TREE.md` passa a registrar as fases adicionais do Programa 07.
- `PROJECT_STATUS.md` passa a registrar o bloqueio temporario do Dashboard.
- `PROJECT_DEPENDENCIES.md` passa a declarar `Clinical Experience -> Dashboard`.
- `PROGRAM_07_CLINICAL_EXPERIENCE_LAYER.md` passa a detalhar a nova expansao.

## Riscos

- A Clinical Experience Layer pode ser confundida com UI final.
- Os cards podem ser tratados como motores clinicos.
- Strategy Card pode ser confundido com prescricao.
- Patient Mode pode ser confundido com orientacao direta ao paciente.

## Mitigacoes

- Reforcar que Clinical Experience organiza a consulta, mas nao decide conduta.
- Manter Risk Panel antes de Strategy Card.
- Manter medico como decisor final.
- Proibir prescricao automatica.
- Exigir rastreabilidade e explicabilidade para qualquer conteudo clinico futuro.

## Documentos Afetados

- `docs/PROGRAM_07_CLINICAL_EXPERIENCE_LAYER.md`
- `governance/execution/PROJECT_TREE.md`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/PROJECT_PROGRESS.md`
- `docs/PROJECT_DEPENDENCIES.md`
- `governance/execution/NEXT_MISSION.md`
- `governance/execution/PROJECT_INDEX.md`

## Criterios de Revisao Futura

Revisar esta decisao quando:

- MISSION 153 - Consultation Baseline for concluida;
- MISSION 159 - Conversation Baseline for concluida;
- MISSION 165 - Patient Baseline for concluida;
- o Programa 08 - Dashboard for desbloqueado;
- houver implementacao real de componentes visuais.

## Declaracao Final

Clinical Experience deve preceder Dashboard para garantir que a experiencia da consulta nasca como camada reutilizavel, segura e centrada no paciente, enquanto o Dashboard permanece apenas uma superficie de apresentacao.
