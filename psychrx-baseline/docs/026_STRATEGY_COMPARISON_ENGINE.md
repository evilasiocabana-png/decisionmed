# 026 - Strategy Comparison Engine

## 1. Definicao

O Strategy Comparison Engine e o motor conceitual responsavel por comparar estrategias terapeuticas candidatas de modo transparente, rastreavel e explicavel.

Ele nao decide conduta. Ele organiza criterios para que o medico compare alternativas com clareza.

Este documento nao implementa software, nao define API, nao cria banco de dados, nao escolhe tecnologia e nao descreve algoritmo executavel.

## 2. Missao

A missao do Strategy Comparison Engine e explicitar diferencas entre estrategias quanto a beneficios, riscos, evidencias, restricoes, preferencias e incertezas.

## 3. Responsabilidades

- Comparar beneficios esperados.
- Comparar riscos clinicos.
- Considerar qualidade e aplicabilidade da evidencia.
- Considerar preferencias do paciente.
- Considerar restricoes e contraindicações.
- Explicitar criterios de decisao.
- Indicar alternativas bloqueadas ou condicionais.
- Apoiar Explanation Engine.

## 4. Entradas Conceituais

- Estrategias candidatas.
- Objetivos terapeuticos.
- Resultado do Safety First Engine.
- Constraint Graph.
- Evidence Graph.
- Clinical Snapshot.
- Preferencias do paciente.
- Dados de monitorizacao.
- Incertezas.

## 5. Saidas Conceituais

- Comparacao estruturada.
- Fatores favoraveis por estrategia.
- Fatores desfavoraveis por estrategia.
- Riscos relevantes.
- Evidencias associadas.
- Restricoes aplicaveis.
- Incertezas.
- Justificativa da comparacao.

## 6. Beneficios

Beneficios devem ser avaliados em relacao ao objetivo terapeutico.

Uma estrategia pode ter beneficio teorico, mas baixa adequacao ao paciente se nao dialogar com sintomas-alvo, funcionalidade, qualidade de vida ou estabilidade.

## 7. Riscos

Riscos devem incluir contraindicações, interacoes, eventos adversos, riscos individuais, riscos contextuais e capacidade de monitorizacao.

Risco critico pode bloquear uma estrategia independentemente do beneficio esperado.

## 8. Evidencias

A comparacao deve diferenciar evidencia forte, moderada, limitada, conflitante ou nao aplicavel.

Evidencia populacional deve ser contextualizada ao paciente.

## 9. Preferencias do Paciente

Preferencias devem influenciar a comparacao, mas nao devem anular seguranca clinica.

Quando preferencia e seguranca entrarem em tensao, a tensao deve ser explicada.

## 10. Restricoes

Restricoes absolutas bloqueiam. Restricoes relativas modificam favorabilidade, monitorizacao ou necessidade de avaliacao adicional.

Nenhuma restricao deve ser escondida para tornar a comparacao mais simples.

## 11. Criterios de Decisao

Criterios de decisao conceituais incluem:

- alinhamento com objetivo;
- seguranca;
- eficacia esperada;
- tolerabilidade;
- evidencia;
- aplicabilidade;
- preferencia;
- viabilidade;
- monitorizacao;
- estabilidade longitudinal.

## 12. Transparencia

A comparacao deve permitir ao medico entender por que uma estrategia parece mais ou menos adequada.

Transparencia exige mostrar criterios, fontes, incertezas e alternativas.

## 13. Integracao com Constraint Graph

O Constraint Graph informa restricoes que modificam a comparacao.

O Strategy Comparison Engine nao resolve restricoes sozinho; ele incorpora seus efeitos no raciocinio comparativo.

## 14. Integracao com Explanation Engine

O Explanation Engine transforma a comparacao em justificativa clinica compreensivel.

Toda comparacao deve ser explicavel.

## 15. Limites

O Strategy Comparison Engine nao deve:

- escolher conduta final;
- prescrever;
- ignorar bloqueios;
- comparar sem objetivo;
- comparar sem evidencia rastreavel;
- ocultar incerteza;
- transformar preferencia em decisao automatica.

## 16. Declaracao Final

O Strategy Comparison Engine torna a comparacao terapeutica transparente.

No PsychRx, comparar nao e decidir: e organizar beneficios, riscos, evidencias, preferencias e restricoes para apoiar o julgamento medico.
