# 034 - Reasoning State Model

## 1. Objetivo

Definir os estados conceituais do raciocinio clinico do PsychRx, sem implementar maquina de estados tecnica, codigo ou algoritmo.

## 2. Missao

A missao do Reasoning State Model e representar em que fase o raciocinio clinico se encontra e quais condicoes permitem avancar, retornar ou interromper o fluxo.

## 3. Estado Inicial

O estado inicial ocorre quando ha necessidade de organizar um caso, mas ainda nao existe Clinical Snapshot suficiente.

Caracteristicas:

- dados incompletos;
- incerteza alta;
- necessidade de coleta;
- nenhuma estrategia permitida.

## 4. Coleta

O estado de coleta organiza informacoes clinicas essenciais.

Depende do Question Engine e deve priorizar seguranca, sintomas, contexto, historico e dados ausentes.

## 5. Investigacao

O estado de investigacao ocorre quando os dados coletados comecam a ser interpretados.

Nesse estado, o sistema organiza sintomas, sindromes, restricoes, contexto e incertezas.

## 6. Hipoteses

O estado de hipoteses envolve formacao, comparacao e revisao de hipoteses diagnosticas.

Cada hipotese deve possuir dados favoraveis, dados contrarios, incertezas e nivel de confianca.

## 7. Confirmacao

Confirmacao nao significa diagnostico automatico.

Significa que uma hipotese ganhou sustentacao suficiente para orientar objetivos terapeuticos, mantendo limites e decisao medica final.

## 8. Planejamento

Planejamento ocorre quando objetivos terapeuticos, restricoes, seguranca, evidencias e estrategias candidatas podem ser organizados.

Nenhum planejamento deve ocorrer sem Safety First Engine suficiente.

## 9. Monitorizacao

Monitorizacao acompanha resposta, tolerabilidade, adesao, eventos adversos, funcionalidade e sinais de risco.

Ela alimenta raciocinio longitudinal.

## 10. Reavaliacao

Reavaliacao ocorre quando novos dados exigem retorno a estados anteriores.

Pode ser disparada por piora, novo risco, evento adverso, resposta inesperada, recaida, recorrencia, remissao ou mudanca contextual.

## 11. Transicoes Conceituais

Transicoes devem ser explicitas e justificadas.

O sistema pode avancar quando criterios minimos estiverem satisfeitos, retornar diante de incerteza ou interromper diante de risco.

## 12. Limites

Este modelo nao implementa estado tecnico, nao define workflow de software e nao substitui julgamento medico.

## 13. Declaracao Final

O Reasoning State Model organiza o raciocinio clinico como processo progressivo e reversivel.

No PsychRx, avancar no raciocinio exige dados suficientes, seguranca avaliada, incerteza explicita e rastreabilidade preservada.
