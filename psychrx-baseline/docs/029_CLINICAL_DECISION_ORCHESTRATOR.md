# 029 - Clinical Decision Orchestrator

## 1. Definicao

O Clinical Decision Orchestrator e o componente conceitual que coordena a ordem, as dependencias e o fluxo de informacoes entre os motores do PsychRx.

Ele nao e algoritmo de execucao. Ele define a arquitetura de orquestracao do raciocinio clinico.

## 2. Missao

A missao do Clinical Decision Orchestrator e garantir que os motores operem em sequencia coerente, segura, rastreavel e explicavel.

## 3. Responsabilidades

- Definir ordem conceitual dos motores.
- Coordenar fluxo de informacoes.
- Explicitar dependencias.
- Interromper raciocinio quando seguranca exigir.
- Acionar reavaliacao.
- Tratar falhas conceituais.
- Evitar sobreposicao de responsabilidades.
- Preservar medico como decisor final.

## 4. Entradas Conceituais

- Clinical Snapshot.
- Perguntas pendentes.
- Hipoteses diagnosticas.
- Objetivos terapeuticos.
- Restricoes.
- Evidencias.
- Alertas de seguranca.
- Estrategias candidatas.
- Dados longitudinais.

## 5. Saidas Conceituais

- Fluxo de raciocinio coordenado.
- Estado de cada motor.
- Dependencias satisfeitas ou pendentes.
- Interrupcoes por seguranca.
- Necessidade de reavaliacao.
- Explicacao do percurso decisorio.

## 6. Ordem de Execucao Conceitual

A ordem conceitual recomendada e:

1. Clinical Snapshot.
2. Clinical Context Engine.
3. Question Engine.
4. Diagnostic Reasoning Engine.
5. Uncertainty Engine.
6. Therapeutic Objective Engine.
7. Constraint Graph e Safety First Engine.
8. Strategy Generation Engine.
9. Strategy Comparison Engine.
10. Evidence Graph e Biblioteca Cientifica.
11. Explanation Engine.
12. Monitoring Engine.
13. Longitudinal Reasoning e Clinical Navigation Engine.

Essa ordem pode retroceder quando surgirem novas informacoes, riscos ou incertezas.

## 7. Fluxo de Informacoes

Cada motor deve receber apenas o que precisa conceitualmente e devolver saidas claras para os motores seguintes.

Conhecimento cientifico deve permanecer separado do raciocinio. Interface nao decide logica clinica.

## 8. Dependencias entre Motores

Estrategia depende de objetivo. Objetivo depende de Snapshot e hipoteses. Comparacao depende de seguranca, restricoes e evidencias. Explicacao depende de toda a trilha do raciocinio. Monitorizacao depende de risco, estrategia e objetivo.

## 9. Reavaliacao

O orquestrador deve prever retorno a etapas anteriores quando:

- novo dado surge;
- risco e identificado;
- hipotese muda;
- objetivo muda;
- evidencia entra em conflito;
- evento adverso ocorre;
- resposta longitudinal altera o caso.

## 10. Tratamento de Falhas Conceituais

Falhas conceituais incluem:

- Snapshot insuficiente;
- dado essencial ausente;
- risco nao avaliado;
- ausencia de evidencia rastreavel;
- conflito nao resolvido;
- objetivo inexistente;
- estrategia sem justificativa;
- explicacao incompleta.

Falhas devem interromper ou limitar o raciocinio conforme impacto clinico.

## 11. Coordenacao entre Motores

O orquestrador deve evitar duplicidade: cada motor tem responsabilidade propria e compartilha resultados sem invadir o papel dos demais.

## 12. Criterios de Interrupcao por Seguranca

O fluxo deve ser interrompido ou bloqueado quando houver risco agudo, bloqueio absoluto, dado essencial ausente, interacao grave, contraindicação critica ou necessidade de encaminhamento.

## 13. Limites

O Clinical Decision Orchestrator nao deve:

- implementar algoritmo;
- prescrever;
- decidir conduta;
- substituir medico;
- executar interface;
- armazenar conhecimento cientifico;
- permitir salto de seguranca.

## 14. Declaracao Final

O Clinical Decision Orchestrator coordena o raciocinio do PsychRx.

No PsychRx, os motores nao operam como ilhas: eles formam uma sequencia clinica segura, rastreavel, explicavel e sempre subordinada ao julgamento medico.
