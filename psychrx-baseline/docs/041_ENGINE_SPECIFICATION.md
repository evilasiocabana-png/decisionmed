# 041 - Engine Specification

## 1. Objetivo

Definir a especificacao de engenharia conceitual dos motores do PsychRx, sem implementar software, escolher tecnologia, escrever codigo ou criar APIs.

## 2. Missao

Transformar os motores conceituais em contratos de engenharia compreensiveis para implementacao futura, preservando seguranca clinica, rastreabilidade, explicabilidade e separacao entre conhecimento e algoritmo.

## 3. Motores Abrangidos

Esta especificacao abrange:

- Question Engine;
- Diagnostic Reasoning Engine;
- Therapeutic Objective Engine;
- Clinical Context Engine;
- Uncertainty Engine;
- Safety First Engine;
- Strategy Generation Engine;
- Strategy Comparison Engine;
- Explanation Engine;
- Monitoring Engine;
- Longitudinal Reasoning;
- Clinical Navigation Engine;
- Clinical Decision Orchestrator.

## 4. Responsabilidades Gerais

Cada motor deve ter responsabilidade unica, limites definidos e saidas conceituais rastreaveis.

Motores nao devem acessar interface diretamente, conter evidencia hardcoded, prescrever, substituir julgamento medico ou decidir conduta final.

## 5. Entradas

Entradas devem ser explicitas, validadas e semanticamente coerentes.

Categorias de entrada:

- dados do paciente;
- Clinical Snapshot;
- contexto clinico;
- hipoteses;
- objetivos;
- restricoes;
- evidencias;
- estados de raciocinio;
- alertas;
- historico longitudinal.

## 6. Saidas

Saidas devem ser interpretaveis por outros motores e pelo Explanation Engine.

Categorias de saida:

- perguntas;
- hipoteses;
- objetivos;
- restricoes;
- alertas;
- estrategias candidatas;
- comparacoes;
- explicacoes;
- planos conceituais de monitorizacao;
- estados longitudinais;
- erros ou bloqueios.

## 7. Dependencias

Dependencias devem seguir a arquitetura em camadas.

Regras principais:

- motores dependem de contratos conceituais, nao de interface;
- motores nao dependem de dashboard;
- motores nao acessam conhecimento cientifico como texto solto;
- evidencias chegam por objetos de conhecimento validados;
- qualquer saida clinica deve ser explicavel.

## 8. Contratos

Cada motor deve declarar:

- responsabilidade;
- entradas obrigatorias;
- entradas opcionais;
- saidas obrigatorias;
- saidas opcionais;
- pre-condicoes;
- pos-condicoes;
- erros possiveis;
- criterios de falha;
- relacoes com auditoria.

## 9. Pre-condicoes

Pre-condicoes sao requisitos para um motor operar.

Exemplos:

- Strategy Generation exige TherapeuticObjective;
- Strategy Comparison exige seguranca avaliada;
- Explanation exige trilha de rastreabilidade;
- Monitoring exige objetivo, risco ou estrategia;
- Longitudinal Reasoning exige pelo menos um estado clinico comparavel.

## 10. Pos-condicoes

Pos-condicoes descrevem o que deve ser verdadeiro apos a execucao conceitual de um motor.

Exemplos:

- uma pergunta deve ter justificativa;
- uma hipotese deve ter nivel de confianca;
- uma estrategia deve ter objetivo;
- um alerta deve ter explicacao;
- uma comparacao deve ter evidencias e restricoes visiveis.

## 11. Criterios de Falha

Falhas ocorrem quando:

- falta dado obrigatorio;
- ha risco nao avaliado;
- ha evidencia ausente;
- ha conflito nao tratado;
- existe nomenclatura nao oficial;
- a saida nao e explicavel;
- a rastreabilidade e insuficiente;
- a dependencia viola arquitetura.

## 12. Limites

Este documento nao define classes, metodos, schemas, linguagem, framework ou persistencia.

## 13. Declaracao Final

Engine Specification e o contrato conceitual dos motores do PsychRx.

No PsychRx, nenhum motor deve ser implementado antes de ter responsabilidade, entrada, saida, dependencia, pre-condicao, pos-condicao e falha claramente especificadas.
