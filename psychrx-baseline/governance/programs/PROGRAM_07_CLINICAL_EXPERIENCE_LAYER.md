# Program 07 - Clinical Workspace

## Status

Prioridade maxima do PsychRx apos ADR 0010 e ADR 0011.

Baseline documental anterior da Clinical Experience Layer: concluida.

Nova prioridade: construir a experiencia completa da consulta clinica por Clinical Widgets antes de IA, Clinical Kernel e Dashboard definitivo.

## Missao do Programa

Construir o ambiente onde o raciocinio clinico acontecera.

Este programa nao implementa raciocinio clinico.

Ele cria o workspace da consulta para que o medico possa usar o PsychRx sem perder contato visual com o paciente.

## Linguagem Oficial

O Programa 07 segue a `Clinical Workspace Design Language`.

Termos oficiais:

- Clinical Workspace;
- Clinical Widget;
- Clinical Investigation Panel;
- Clinical Compass;
- Missing Information Widget;
- Clinical Confidence Widget.

O termo Card pode continuar existindo como forma visual, mas nao como unidade arquitetural principal.

## Principio Central

O maior ativo do PsychRx sera a consulta.

O Clinical Workspace vem antes de:

- IA;
- Clinical Kernel Integration;
- Dashboard definitivo;
- Mobile definitivo;
- regras terapeuticas.

## Fora de Escopo

- prescricao automatica;
- recomendacao terapeutica final;
- IA clinica;
- Clinical Kernel;
- motores clinicos;
- banco de dados;
- API clinica real;
- regras terapeuticas hardcoded.

## PHASE 01 - Workspace Infrastructure

Objetivo: construir a infraestrutura conceitual inicial do workspace.

```text
SPRINT 18 - Consultation Workspace
    MISSION 144 - CONSULTATION_LAYOUT
    MISSION 145 - PATIENT_HEADER_CARD
    MISSION 146 - CURRENT_MEDICATION_CARD
    MISSION 147 - LIVE_CLINICAL_SNAPSHOT
    MISSION 148 - CLINICAL_INVESTIGATION_PANEL
    MISSION 149 - OBJECTIVES_CARD
    MISSION 150 - RISK_PANEL
    MISSION 151 - CLINICAL_STRATEGY_CARD
    MISSION 152 - MONITORING_CARD
    MISSION 153 - CONSULTATION_WORKSPACE_BASELINE
```

Observacao de reconciliacao: `146_CURRENT_MEDICATION_CARD.md` ja existia antes da revisao CTO que reposicionou o Live Clinical Snapshot. Para nao reutilizar numero, `LIVE_CLINICAL_SNAPSHOT` foi movido para 147.

## PHASE 02 - Clinical Widgets

Objetivo: consolidar widgets clinicos independentes e reutilizaveis.

```text
SPRINT 19 - Clinical Widgets
    MISSION 154 - CLINICAL_WIDGET_SYSTEM
    MISSION 155 - CLINICAL_COMPASS
    MISSION 156 - MISSING_INFORMATION_WIDGET
    MISSION 157 - CLINICAL_CONFIDENCE_WIDGET
    MISSION 158 - WIDGET_CONTRACTS
    MISSION 159 - WIDGET_BASELINE
```

## PHASE 03 - Dynamic Investigation

Objetivo: estruturar investigacao dinamica sem IA.

```text
SPRINT 20 - Dynamic Investigation
    MISSION 160 - CONVERSATION_PANEL
    MISSION 161 - DYNAMIC_INVESTIGATION_SYSTEM
    MISSION 162 - QUESTION_PRIORITY_ENGINE
    MISSION 163 - QUESTION_COMPLETION
    MISSION 164 - CONSULTATION_PROGRESS
    MISSION 165 - DYNAMIC_INVESTIGATION_BASELINE
```

## PHASE 04 - Consultation Flow

Objetivo: organizar fluxo da consulta sem motor clinico.

```text
SPRINT 21 - Consultation Flow
    MISSION 166 - CONSULTATION_FLOW
    MISSION 167 - CLINICAL_TIMELINE
    MISSION 168 - MEDICATION_TIMELINE
    MISSION 169 - SYMPTOM_TIMELINE
    MISSION 170 - RESPONSE_TIMELINE
    MISSION 171 - FLOW_BASELINE
```

## PHASE 05 - Patient View

Objetivo: criar versao segura e simplificada para comunicacao com paciente.

```text
SPRINT 22 - Patient View
    MISSION 172 - PATIENT_VIEW
    MISSION 173 - PATIENT_TIMELINE
    MISSION 174 - PATIENT_GOALS
    MISSION 175 - PATIENT_EDUCATION
    MISSION 176 - PATIENT_SUMMARY
    MISSION 177 - PATIENT_VIEW_BASELINE
```

## PHASE 06 - Workspace Validation

Objetivo: validar desktop, tablet, mobile, responsividade e acessibilidade.

```text
SPRINT 23 - Workspace Validation
    MISSION 178 - DESKTOP_REVIEW
    MISSION 179 - TABLET_REVIEW
    MISSION 180 - MOBILE_REVIEW
    MISSION 181 - RESPONSIVE_VALIDATION
    MISSION 182 - ACCESSIBILITY
    MISSION 183 - WORKSPACE_BASELINE
```

## Gate de Conclusao do Programa

O Programa 07 so fica completo quando existirem:

- Clinical Workspace;
- Clinical Widget System;
- Clinical Investigation Panel;
- Clinical Compass;
- Missing Information Widget;
- Clinical Confidence Widget;
- Timeline;
- Monitoring View;
- Patient View;
- responsividade desktop, tablet e mobile;
- baseline de workspace validada.

## Gate para Programa 08

O Programa 08 - Clinical Kernel Integration so deve iniciar quando o Workspace Baseline estiver completo.

## Declaracao Final

O Programa 07 transforma a consulta no centro operacional do PsychRx. Ele cria microexperiencias clinicas reutilizaveis onde o raciocinio futuro sera apresentado ao medico, sem IA, sem motor clinico, sem prescricao e sem regras terapeuticas.
