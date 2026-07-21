# 025 - Strategy Generation Engine

## 1. Definicao

O Strategy Generation Engine e o motor conceitual responsavel por organizar estrategias terapeuticas possiveis a partir de objetivos terapeuticos, seguranca, restricoes, evidencias e contexto do paciente.

Ele nao prescreve e nao seleciona conduta final. Ele gera possibilidades estruturadas para raciocinio medico.

## 2. Missao

A missao do Strategy Generation Engine e produzir um conjunto de estrategias conceitualmente possiveis, justificadas e rastreaveis, sem ultrapassar os limites de seguranca ou evidencia.

## 3. Responsabilidades

- Gerar alternativas terapeuticas possiveis.
- Exigir objetivo terapeutico previo.
- Respeitar Safety First Engine.
- Respeitar Constraint Graph.
- Vincular estrategias a Evidence Graph.
- Diferenciar tipos de estrategia.
- Explicitar riscos, limites e incertezas.
- Preparar alternativas para Strategy Comparison Engine.

## 4. Entradas Conceituais

- Clinical Snapshot.
- TherapeuticObjective.
- Hipoteses diagnosticas.
- Resultado do Safety First Engine.
- Restricoes absolutas e relativas.
- Evidencias cientificas rastreaveis.
- Historico de resposta.
- Eventos adversos previos.
- Preferencias do paciente.
- Dados de monitorizacao.

## 5. Saidas Conceituais

- Estrategias candidatas.
- Estrategias bloqueadas.
- Estrategias condicionadas a monitorizacao.
- Justificativas iniciais.
- Evidencias associadas.
- Restricoes relevantes.
- Incertezas.
- Necessidade de comparacao posterior.

## 6. Monoterapia

Monoterapia representa estrategia com um unico agente ou abordagem psicofarmacologica principal.

Deve ser considerada quando for coerente com objetivo, seguranca, evidencia, tolerabilidade e contexto. Nao deve ser presumida como superior sem justificativa.

## 7. Associacao

Associacao representa uso combinado de estrategias ou agentes.

Deve exigir justificativa clara, avaliacao de interacoes, risco acumulado, evidencia aplicavel e monitorizacao proporcional.

## 8. Potencializacao

Potencializacao representa estrategia voltada a ampliar resposta quando a resposta isolada e insuficiente.

Deve considerar resposta parcial, tolerabilidade, risco adicional, evidencia e alternativas menos complexas.

## 9. Troca

Troca representa substituicao de uma estrategia por outra.

Deve considerar motivo da troca, falha de eficacia, intolerancia, evento adverso, preferencia, risco, continuidade do cuidado e necessidade de transicao segura.

## 10. Titulacao

Titulacao representa ajuste gradual de exposicao terapeutica.

Como conceito, deve ser vinculada a tolerabilidade, resposta, seguranca, monitorizacao e decisao medica. O documento nao define doses nem esquemas.

## 11. Descontinuacao

Descontinuacao representa retirada ou encerramento de uma estrategia.

Deve considerar estabilidade, risco de recaida, recorrencia, abstinencia, eventos adversos, preferencias e monitorizacao. Nao deve ser automatica.

## 12. Restricoes

Restricoes podem impedir, limitar ou condicionar a geracao de estrategias.

Estrategias que violam bloqueio absoluto nao devem ser apresentadas como adequadas.

## 13. Seguranca

Nenhuma estrategia deve ser gerada como candidata favoravel antes da avaliacao de seguranca.

Alertas e bloqueios devem acompanhar a estrategia desde sua origem.

## 14. Evidencias

Toda estrategia candidata deve indicar a necessidade de evidencia rastreavel.

Evidencia limitada, conflitante ou ausente deve reduzir a forca da estrategia e aparecer na explicacao.

## 15. Integracoes

O Strategy Generation Engine depende de Clinical Snapshot, Diagnostic Reasoning, Therapeutic Objective Engine, Safety First Engine, Constraint Graph e Evidence Graph.

Ele alimenta o Strategy Comparison Engine e o Explanation Engine.

## 16. Limites

O Strategy Generation Engine nao deve:

- prescrever;
- escolher estrategia final;
- gerar estrategia sem objetivo;
- ignorar seguranca;
- criar regra clinica sem fonte;
- misturar conhecimento cientifico com algoritmo;
- ocultar alternativa bloqueada quando isso for relevante para explicacao.

## 17. Declaracao Final

O Strategy Generation Engine organiza possibilidades terapeuticas sem transformar possibilidade em prescricao.

No PsychRx, toda estrategia nasce de objetivo, seguranca, restricao, evidencia e contexto.
