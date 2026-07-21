# 148 - Clinical Investigation Panel

## Objetivo

Implementar e documentar o Clinical Investigation Panel como widget read-only do Clinical Workspace.

## Conceito

O Clinical Investigation Panel substitui o antigo Live Question Panel.

Ele organiza perguntas clinicas prioritarias e lacunas relevantes durante a consulta, mantendo o medico como decisor final.

O painel nao decide conduta, nao fecha diagnostico, nao prescreve, nao usa IA e nao executa motor clinico.

## Escopo Entregue

- Secao visual de investigacao clinica no app localhost.
- Perguntas pendentes organizadas por prioridade textual.
- Estado read-only explicito.
- Aviso de que as perguntas ainda sao estaticas.
- Integracao ao Consultation Workspace.
- Testes atualizados para preservar nomenclatura e limites.

## Perguntas Minimas

- Ideacao suicida?
- Sintomas maniformes previos?
- Uso de alcool?
- Uso de substancias?
- Adesao ao tratamento?
- Efeitos adversos relevantes?
- Gestacao ou lactacao, quando aplicavel?

## Limites

O Clinical Investigation Panel nao:

- calcula prioridade clinica real;
- cria diagnostico;
- sugere tratamento;
- desbloqueia estrategia terapeutica;
- usa IA;
- substitui anamnese medica;
- grava dados em banco;
- aciona Clinical Kernel.

## Relacao com o Clinical Workspace

O painel ocupa a regiao Clinical Inquiry do Consultation Workspace.

Ele deve aparecer antes de qualquer Strategy Widget, porque lacunas de seguranca e contexto precisam ser visiveis antes de estrategias.

## Relacao com o Clinical Kernel

Nesta fase, o painel e estatico e read-only.

Futuramente, o Clinical Kernel podera alimentar perguntas dinamicas, estados de resposta e lacunas clinicas calculadas, desde que respeite:

- Constituicao Clinica;
- Clinical Widget Specification;
- rastreabilidade;
- explicabilidade;
- medico como decisor final.

## Criterios de Aceite

- O painel aparece no localhost.
- O painel usa a linguagem Clinical Investigation Panel.
- O painel mostra perguntas em modo read-only.
- O painel nao sugere conduta.
- O painel nao calcula prioridade clinicamente.
- Os testes passam.
- PROJECT_STATUS foi atualizado.
- NEXT_MISSION aponta para MISSION 149 - Objectives Widget.

## Declaracao Final

O Clinical Investigation Panel e apenas uma camada de apresentacao read-only do PsychRx, aguardando futura integracao com o Clinical Kernel.
