# ADR 0011 - Clinical Workspace Design Language

## Status

Aceito.

## Data

2026-06-30

## Contexto

O Programa 07 evoluiu de uma sequencia de telas e cards para o conceito de Clinical Workspace. A revisao CTO definiu que o projeto deve parar de pensar em telas isoladas e passar a organizar microexperiencias clinicas.

O termo `Card` e limitado, pois uma unidade de experiencia pode ser card, timeline, lista, painel, modal ou overlay.

## Decisao

Criar a `Clinical Workspace Design Language`.

O termo oficial para a unidade basica da experiencia passa a ser:

```text
Clinical Widget
```

O antigo `Live Question Panel` deve evoluir para:

```text
Clinical Investigation Panel
```

## Widgets Oficiais Iniciais

```text
Patient Widget
Snapshot Widget
Clinical Investigation Panel
Medication Widget
Risk Widget
Objectives Widget
Strategy Widget
Timeline Widget
Monitoring Widget
Evidence Widget
Conversation Widget
Missing Information Widget
Clinical Confidence Widget
Clinical Compass
```

## Justificativa

O Clinical Investigation Panel nao apenas mostra perguntas. Ele conduz investigacao clinica de forma organizada, exibindo poucas lacunas relevantes e mudando conforme o contexto.

O conceito de Clinical Widget permite que cada microexperiencia seja especificada, testada e implementada como unidade independente.

## Impacto

- `PROJECT_GLOSSARY.md` passa a registrar os novos termos.
- `PROGRAM_07_CLINICAL_EXPERIENCE_LAYER.md` passa a organizar fases por Workspace Infrastructure, Clinical Widgets, Dynamic Investigation, Consultation Flow, Patient View e Workspace Validation.
- `PROJECT_TREE.md` passa a usar Clinical Investigation Panel em vez de Live Question Panel para a missao 148.
- `NEXT_MISSION.md` passa a apontar para `148_CLINICAL_INVESTIGATION_PANEL.md`.
- `CLINICAL_WORKSPACE_DESIGN_LANGUAGE.md` passa a ser documento oficial de linguagem.

## Riscos

- Clinical Widget ser confundido com motor clinico.
- Clinical Investigation Panel ser confundido com IA.
- Clinical Confidence Widget parecer diagnostico automatico.
- Clinical Compass parecer decisor de suficiencia clinica.

## Mitigacoes

- Widgets organizam experiencia, nao decidem conduta.
- Clinical Investigation Panel nao usa IA nesta fase.
- Clinical Confidence Widget fica como infraestrutura conceitual, sem diagnostico automatico.
- Clinical Compass informa progresso, mas nao libera conduta.
- Medico permanece decisor final.

## Declaracao Final

A Clinical Workspace Design Language transforma o PsychRx de um conjunto de telas em um sistema de microexperiencias clinicas reutilizaveis, preservando a consulta como centro do produto e preparando a futura integracao com o Clinical Kernel.
