# ADR 0010 - Clinical Workspace Priority

## Status

Aceito.

## Data

2026-06-30

## Contexto

O Programa 07 estava registrado como Clinical Experience Layer, com Consultation MVP antes do Dashboard. Uma revisao CTO posterior definiu que o maior ativo do PsychRx sera a consulta e que o programa deve ser tratado como:

```text
PROGRAM 07 - Clinical Workspace
```

O objetivo passa a ser construir a experiencia completa da consulta clinica antes de IA, Clinical Kernel e Dashboard definitivo.

## Decisao

Priorizar o Clinical Workspace como programa atual do PsychRx.

O Programa 07 passa a governar:

- Consultation Workspace;
- Dynamic Consultation;
- Clinical Cards;
- Timeline;
- Workspace Review.

O Programa 08 deixa de ser Dashboard e passa a ser candidato a:

```text
PROGRAM 08 - Clinical Kernel Integration
```

O Dashboard definitivo continua bloqueado ate que o workspace tenha baseline validada.

## Reconciliacao de Numeracao

Antes desta ADR, as missoes 144, 145 e 146 ja haviam sido executadas:

- `144_CONSULTATION_LAYOUT.md`
- `145_PATIENT_HEADER_CARD.md`
- `146_CURRENT_MEDICATION_CARD.md`

A revisao CTO propunha `146_LIVE_CLINICAL_SNAPSHOT` e `147_CURRENT_MEDICATION_CARD`. Para nao reutilizar numeros nem renomear silenciosamente documentos ja criados, a sequencia local fica:

```text
144 - Consultation Layout
145 - Patient Header Card
146 - Current Medication Card
147 - Live Clinical Snapshot
148 - Live Question Panel
149 - Objectives Card
150 - Risk Panel
151 - Clinical Strategy Card
152 - Monitoring Card
153 - Consultation Workspace Baseline
```

## Justificativa

O Clinical Kernel precisara de uma superficie preparada para apresentar raciocinio ao medico. Construir o workspace primeiro reduz retrabalho, impede que o Dashboard defina a experiencia e preserva a consulta como centro do produto.

## Alternativas Consideradas

### Seguir para IA

Rejeitada. IA sem workspace validado aumenta risco de produto desorganizado.

### Seguir para Clinical Kernel

Rejeitada neste momento. O Kernel precisara de superficie preparada para exibicao segura.

### Seguir para Dashboard

Rejeitada. Dashboard e consumidor, nao definidor da experiencia.

### Priorizar Clinical Workspace

Aceita. A consulta passa a organizar as proximas entregas.

## Impacto

- `PROGRAM_07_CLINICAL_EXPERIENCE_LAYER.md` deve ser atualizado para Clinical Workspace.
- `PROJECT_TREE.md` deve refletir Sprints 18 a 22.
- `PROJECT_STATUS.md` deve registrar Programa 07 como prioridade maxima.
- `NEXT_MISSION.md` deve apontar para `147_LIVE_CLINICAL_SNAPSHOT.md`.
- `PROJECT_DEPENDENCIES.md` deve refletir `Software Platform -> Clinical Workspace -> Clinical Kernel Integration`.

## Riscos

- Workspace ser confundido com motor clinico.
- Live Snapshot parecer raciocinio automatico.
- Dynamic Question System parecer IA.
- Strategy Card parecer prescricao.

## Mitigacoes

- Manter tudo read-only enquanto nao houver kernel.
- Bloquear Strategy Card ate Clinical Kernel.
- Proibir IA, prescricao e regra terapeutica.
- Manter medico como decisor final.
- Exigir rastreabilidade futura.

## Documentos Afetados

- `docs/PROGRAM_07_CLINICAL_EXPERIENCE_LAYER.md`
- `governance/execution/PROJECT_TREE.md`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/PROJECT_PROGRESS.md`
- `docs/PROJECT_DEPENDENCIES.md`
- `governance/execution/NEXT_MISSION.md`

## Declaracao Final

O Clinical Workspace passa a ser a prioridade maxima do PsychRx porque a consulta e a superficie onde todo raciocinio futuro devera aparecer de forma segura, silenciosa, rastreavel e centrada no paciente.
