# 044 - Engine Input Output

## 1. Objetivo

Definir entradas, saidas, erros e estados conceituais de cada motor do PsychRx, sem implementar software.

## 2. Missao

Tornar explicito o que cada motor precisa receber, o que deve produzir e quando deve falhar ou bloquear o fluxo.

## 3. Padrao de Especificacao

Para cada motor, considerar:

- entrada obrigatoria;
- entrada opcional;
- saida obrigatoria;
- saida opcional;
- erros;
- estados.

## 4. Question Engine

Entrada obrigatoria: Clinical Snapshot parcial ou completo.

Entrada opcional: hipoteses, alertas, contexto, historico.

Saida obrigatoria: perguntas priorizadas e lacunas.

Saida opcional: criterio de suficiencia da coleta.

Erros: Snapshot ausente, dados contraditorios sem sinalizacao.

Estados: coleta pendente, coleta suficiente, incerteza persistente.

## 5. Diagnostic Reasoning Engine

Entrada obrigatoria: Clinical Snapshot e sintomas organizados.

Entrada opcional: dados longitudinais, contexto, evidencias diagnosticas.

Saida obrigatoria: hipoteses, diferenciais e nivel de confianca.

Saida opcional: criterios de confirmacao ou exclusao.

Erros: dados insuficientes, hipotese sem justificativa.

Estados: hipotese inicial, em avaliacao, revisada, suspensa.

## 6. Therapeutic Objective Engine

Entrada obrigatoria: Snapshot, hipoteses e riscos relevantes.

Entrada opcional: preferencias, funcionalidade, qualidade de vida.

Saida obrigatoria: objetivos primarios e secundarios.

Saida opcional: criterios de sucesso.

Erros: objetivo sem contexto, conflito nao explicitado.

Estados: objetivo proposto, priorizado, revisado, suspenso.

## 7. Safety First Engine

Entrada obrigatoria: dados de risco e restricoes essenciais.

Entrada opcional: interacoes, comorbidades, documentos regulatorios.

Saida obrigatoria: alertas, bloqueios ou liberacao conceitual.

Saida opcional: necessidade de encaminhamento ou monitorizacao.

Erros: risco essencial ausente, interacao sem avaliacao.

Estados: seguranca pendente, alerta moderado, alerta critico, bloqueado.

## 8. Strategy Generation Engine

Entrada obrigatoria: objetivo, seguranca e restricoes.

Entrada opcional: preferencias, historico, evidencias.

Saida obrigatoria: estrategias candidatas ou motivo de nao geracao.

Saida opcional: estrategias condicionais.

Erros: estrategia sem objetivo, evidencia ausente, bloqueio ignorado.

Estados: nao iniciado, candidatos gerados, bloqueado.

## 9. Strategy Comparison Engine

Entrada obrigatoria: estrategias candidatas, objetivos, seguranca e evidencias.

Entrada opcional: preferencias e dados longitudinais.

Saida obrigatoria: comparacao explicavel.

Saida opcional: ranking conceitual nao prescritivo.

Erros: comparacao sem evidencia, restricao ignorada.

Estados: comparacao pendente, comparado, inconclusivo.

## 10. Explanation Engine

Entrada obrigatoria: trilha de raciocinio e fontes.

Entrada opcional: alternativas, conflitos, incertezas.

Saida obrigatoria: justificativa rastreavel.

Saida opcional: explicacao de alternativas rejeitadas.

Erros: fonte ausente, cadeia incompleta, incerteza ocultada.

Estados: explicacao pendente, completa, insuficiente.

## 11. Monitoring Engine

Entrada obrigatoria: objetivo, risco ou estrategia.

Entrada opcional: eventos adversos, escalas, exames, adesao.

Saida obrigatoria: necessidades de monitorizacao.

Saida opcional: gatilhos de reavaliacao.

Erros: monitorizacao sem justificativa, risco sem acompanhamento.

Estados: monitorizacao definida, pendente, insuficiente.

## 12. Longitudinal Reasoning e Clinical Navigation

Entrada obrigatoria: Snapshot atual e referencia temporal.

Entrada opcional: Snapshots anteriores, resposta, recaida, remissao.

Saida obrigatoria: leitura longitudinal.

Saida opcional: necessidade de revisar hipoteses, objetivos ou estrategias.

Erros: estabilidade declarada sem dados, trajetoria ignorada.

Estados: evolucao incerta, melhora, piora, remissao, recaida, recorrencia, estabilidade.

## 13. Limites

Este documento nao define tipos de dados tecnicos, classes, schemas ou APIs.

## 14. Declaracao Final

Engine Input Output define o contrato operacional conceitual dos motores.

No PsychRx, motor sem entradas, saidas, erros e estados definidos ainda nao esta pronto para implementacao.
