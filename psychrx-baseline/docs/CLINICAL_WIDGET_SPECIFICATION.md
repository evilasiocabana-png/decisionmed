# Clinical Widget Specification

## 1. Objetivo

Definir a biblioteca oficial de Clinical Widgets do PsychRx.

Este documento nao implementa software, nao cria UI final, nao cria IA, nao cria Clinical Kernel e nao define regra terapeutica.

Ele padroniza os widgets que irao compor o Clinical Workspace.

## 2. Definicao

Clinical Widget e a unidade basica da experiencia clinica do PsychRx.

Um widget pode ser card, lista, timeline, painel, modal, overlay, indicador ou faixa de status.

Clinical Widget organiza a consulta.

Clinical Widget nao decide conduta.

Clinical Widget nao prescreve.

## 3. Contrato Conceitual Obrigatorio

Todo Clinical Widget deve possuir:

```text
id
title
priority
state
context
dependencies
actions
explanation
visibility
permissions
```

## 4. Campos

### id

Identificador estavel do widget.

### title

Nome exibivel e compreensivel.

### priority

Ordem de importancia relativa dentro do workspace.

### state

Estado atual do widget.

Exemplos:

```text
empty
pending
ready
blocked
requires_review
hidden
```

### context

Contexto clinico ou operacional que justifica a exibicao.

### dependencies

Outros widgets, contratos ou dados necessarios.

### actions

Acoes permitidas no futuro.

Nesta fase, acoes sao conceituais e nao executaveis.

### explanation

Motivo pelo qual o widget esta visivel ou em determinado estado.

### visibility

Regra conceitual de exibicao.

### permissions

Limites de quem pode ver, editar ou confirmar informacoes.

## 5. Widgets Oficiais

### Patient Widget

Ancora a consulta no paciente.

Nao reduz a pessoa ao diagnostico.

### Medication Widget

Organiza tratamento atual.

Nao recomenda inicio, suspensao, troca ou ajuste.

### Snapshot Widget

Representa estado clinico dinamico.

Nao fecha diagnostico.

### Clinical Investigation Panel

Conduz investigacao por lacunas clinicas relevantes.

Nao usa IA nesta fase.

Nao diagnostica.

### Risk Widget

Mantem riscos visiveis antes de estrategia.

Nao libera conduta.

### Objective Widget

Organiza objetivos terapeuticos em discussao.

Nao escolhe objetivo pelo medico.

### Strategy Widget

Mostra estrategia apenas quando permitido por fases futuras.

Nesta fase permanece bloqueado.

Nao prescreve.

### Monitoring Widget

Organiza acompanhamento longitudinal.

Nao substitui seguimento medico.

### Evidence Widget

Exibe fonte, qualidade, conflito e aplicabilidade quando houver conhecimento validado.

Nao transforma evidencia em regra individual automatica.

### Timeline Widget

Organiza eventos da consulta e do curso clinico.

Nao apaga historico sem rastreabilidade futura.

### Explanation Widget

Organiza justificativas, incertezas e origem das informacoes.

Nao oculta incerteza.

### Conversation Widget

Organiza conversa clinica.

Nao vira chatbot autonomo.

### Clinical Compass

Mostra orientacao da consulta, progresso e pendencias.

Nao decide se informacoes sao suficientes para conduta.

### Missing Information Widget

Mostra lacunas clinicas pendentes.

Nao diagnostica e nao prescreve.

### Clinical Confidence Widget

Representa confianca futura de hipoteses ou informacoes.

Nesta fase e apenas especificacao conceitual.

Nao confirma diagnostico automaticamente.

## 6. Arquitetura de Apresentacao

Estrutura oficial:

```text
presentation/
    clinical_workspace/
        widgets/
        layouts/
        workspace/
        investigation/
        timeline/
        strategy/
        monitoring/
        patient/
        shared/
```

## 7. Dependencias Permitidas

```text
presentation -> application contracts
interfaces -> presentation
```

## 8. Dependencias Proibidas

```text
presentation -> domain direct decision
presentation -> knowledge direct rule
presentation -> evidence direct conclusion
presentation -> reasoning direct execution
presentation -> safety bypass
widget -> prescription
widget -> autonomous diagnosis
```

## 9. Regras de Maturidade

Um widget so pode ser considerado maduro quando possuir:

- responsabilidade unica;
- contrato conceitual;
- estado definido;
- limites clinicos;
- comportamento proibido;
- testes futuros previstos;
- documentacao;
- relacao com outros widgets.

## 10. Relacao com Clinical Kernel

O Clinical Kernel futuro alimentara widgets por contratos.

Widgets nao devem chamar motores diretamente.

Widgets apresentam estado, explicacao e rastreabilidade.

## Declaracao Final

Clinical Widget Specification define a biblioteca de componentes clinicos do PsychRx. Ela prepara o Workspace para receber o Clinical Kernel no futuro sem transformar apresentacao em decisao clinica.
