# 119 Clinical Experience Baseline

## Objetivo

Consolidar a baseline conceitual da experiencia clinica do PsychRx.

## Componentes Baseline

- Clinical Workflow;
- Consultation Room;
- Guided Anamnesis;
- Live Question Panel;
- Clinical Card Stack;
- Symptom Capture;
- Strategy Panel;
- Risk Panel;
- Monitoring Timeline;
- Evidence Summary;
- Patient Friendly Mode;
- Consultation Timeline.

## Componentes Estruturais Oficiais

O Programa 07 fica alinhado a ADR 0005 e a camada:

```text
clinical_experience/
```

Componentes obrigatorios:

```text
consultation_room/
clinical_card_stack/
guided_anamnesis/
live_question_panel/
symptom_capture/
strategy_panel/
risk_panel/
monitoring_timeline/
evidence_summary/
patient_friendly_mode/
```

## Criterios de Maturidade

- paciente no centro;
- medico como decisor final;
- seguranca antes de estrategia;
- perguntas ligadas a incertezas;
- explicacao antes de conclusao;
- rastreabilidade longitudinal.

## Dependencias

- depende do Clinical Operating Mind;
- depende do Clinical Snapshot;
- depende do Safety First Engine;
- depende da Clinical Reasoning Architecture;
- depende de contratos futuros da Application Layer;
- nao depende diretamente de Evidence, Knowledge, Reasoning ou Safety para decidir conduta.

## Gate do Programa 07

O Programa 07 esta completo quando:

- todos os documentos 112-119 existem;
- todos os componentes oficiais da Clinical Experience Layer existem;
- a camada nao prescreve;
- a camada nao decide conduta;
- Risk Panel precede Strategy Panel;
- Patient Friendly Mode nao orienta automedicacao;
- interfaces permanecem apenas apresentacionais;
- testes estruturais passam.

## Limites

Esta baseline nao autoriza implementacao de UI, API, IA ou prescricao.

## Declaracao Final

A Clinical Experience Baseline estabelece como o PsychRx deve ser vivido na consulta antes de qualquer construcao visual definitiva.
