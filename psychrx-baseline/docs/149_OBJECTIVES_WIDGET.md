# 149 - Objectives Widget

## Objetivo

Implementar e documentar o Objectives Widget em modo read-only no Clinical Workspace.

## Conceito

O Objectives Widget mostra objetivos terapeuticos conceituais que ajudam o medico a organizar a consulta.

Ele nao gera objetivos automaticamente, nao prioriza conduta, nao recomenda tratamento e nao prescreve.

## Escopo Entregue

- Widget visual "Objectives Widget" no app localhost.
- Objetivos conceituais exibidos em modo read-only.
- Aviso explicito de que nao ha calculo dinamico.
- Integracao com a regiao Safety and Strategy do Consultation Workspace.
- Testes atualizados para preservar o contrato de seguranca.

## Objetivos Exibidos

- Reduzir sofrimento atual.
- Melhorar sono.
- Reduzir ansiedade.
- Melhorar funcionalidade.
- Minimizar efeitos adversos.
- Preservar seguranca clinica.

## Limites

O Objectives Widget nao:

- calcula objetivo terapeutico;
- prioriza clinicamente;
- sugere medicamento;
- sugere dose;
- escolhe estrategia;
- desbloqueia Strategy Widget;
- usa IA;
- usa Clinical Kernel;
- substitui julgamento medico.

## Relacao com o Clinical Workspace

O widget aparece antes do Strategy Widget e junto dos componentes de seguranca, reforcando que objetivos precisam existir antes de qualquer estrategia futura.

## Relacao com o Clinical Kernel

Nesta fase, os objetivos sao estaticos e conceituais.

Futuramente, o Clinical Kernel podera alimentar objetivos estruturados, desde que haja rastreabilidade, explicabilidade, seguranca e revisao medica.

## Criterios de Aceite

- Objectives Widget aparece no localhost.
- Conteudo e read-only.
- Nenhum objetivo e calculado dinamicamente.
- Nao recomenda tratamento.
- Nao prescreve.
- Testes passam.
- PROJECT_STATUS foi atualizado.
- NEXT_MISSION aponta para MISSION 150 - Risk Widget.

## Declaracao Final

O Objectives Widget e uma camada de apresentacao read-only para organizar objetivos conceituais da consulta, sem calcular conduta e sem prescrever.
