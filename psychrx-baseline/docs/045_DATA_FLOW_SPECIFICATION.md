# 045 - Data Flow Specification

## 1. Objetivo

Definir o fluxo oficial de dados conceituais do PsychRx, sem implementar pipeline, banco de dados, API ou software.

## 2. Missao

Garantir que dados clinicos, conhecimento, seguranca, explicacao e auditoria circulem em ordem coerente, rastreavel e segura.

## 3. Fluxo Principal

```text
Paciente
  -> Snapshot
  -> Question Engine
  -> Diagnostic Engine
  -> Objectives
  -> Constraints
  -> Safety
  -> Strategies
  -> Explanation
  -> Monitoring
  -> Audit
```

## 4. Paciente

O fluxo comeca no paciente, sua historia, sintomas, contexto, riscos, preferencias, funcionalidade e qualidade de vida.

Paciente nao deve ser reduzido a diagnostico ou medicamento.

## 5. Snapshot

Clinical Snapshot organiza o estado clinico atual.

Sem Snapshot atualizado, o fluxo nao deve avancar para estrategia.

## 6. Question Engine

Identifica lacunas e perguntas necessarias para reduzir incerteza.

Dados ausentes relevantes devem permanecer visiveis.

## 7. Diagnostic Engine

Organiza hipoteses, diferenciais, criterios, nivel de confianca e incertezas.

Diagnostico final automatico e proibido.

## 8. Objectives

TherapeuticObjective define o alvo clinico antes de qualquer Strategy.

Objetivos devem nascer do paciente e nao do medicamento.

## 9. Constraints

Constraints organizam restricoes absolutas, relativas, contextuais, regulatorias e individuais.

Restricoes modificam ou bloqueiam o fluxo estrategico.

## 10. Safety

Safety First Engine avalia riscos antes da comparacao.

Bloqueios e alertas devem preceder qualquer estrategia favoravel.

## 11. Strategies

Strategy Generation cria candidatos e Strategy Comparison compara alternativas.

Estrategias dependem de objetivo, seguranca, restricoes e evidencia.

## 12. Explanation

Explanation Engine transforma o percurso em justificativa rastreavel.

Sem explicacao, o fluxo esta incompleto.

## 13. Monitoring

Monitoring define acompanhamento proporcional a risco, objetivo, estrategia e estado longitudinal.

Monitorizacao alimenta reavaliacao.

## 14. Audit

Audit preserva origem, versao, fonte, motor, decisao conceitual, incerteza e explicacao.

## 15. Fluxos de Retorno

O fluxo pode retornar quando surgir:

- novo dado;
- risco;
- conflito de evidencia;
- evento adverso;
- resposta inesperada;
- recaida;
- recorrencia;
- deterioracao.

## 16. Limites

Este documento nao define arquitetura de eventos, mensageria, armazenamento ou integracao tecnica.

## 17. Declaracao Final

Data Flow Specification define a ordem clinica dos dados no PsychRx.

No PsychRx, dados so avancam para estrategia quando Snapshot, perguntas, hipoteses, objetivos, restricoes, seguranca e evidencia estiverem coerentes.
