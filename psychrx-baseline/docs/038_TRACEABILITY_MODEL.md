# 038 - Traceability Model

## 1. Objetivo

Definir como toda informacao clinica e cientifica sera rastreada no PsychRx, sem implementar software, banco de dados, logs tecnicos ou APIs.

## 2. Missao

A missao do Traceability Model e permitir reconstruir a origem, evidencia, interpretacao, decisao, justificativa e auditoria de qualquer informacao usada no raciocinio clinico.

## 3. Origem

Toda informacao deve declarar origem.

Origem pode ser fonte cientifica, guideline, documento regulatorio, dado do paciente, Clinical Snapshot, objeto de conhecimento validado ou decisao de curadoria.

## 4. Evidencia

Toda afirmacao clinica relevante deve apontar para evidencia ou registrar ausencia, limitacao ou conflito de evidencia.

Evidencia deve conter tipo, qualidade, ano, aplicabilidade, status e data de revisao.

## 5. Guideline

Quando a origem for guideline, a rastreabilidade deve indicar instituicao, ano, versao, escopo, recomendacao de fonte e limites.

## 6. Decisao

Decisao, neste contexto, significa decisao conceitual do raciocinio: considerar, limitar, bloquear, comparar, explicar ou monitorar.

Cada decisao conceitual deve apontar para dados, evidencias, restricoes e motores envolvidos.

## 7. Justificativa

Justificativa deve conectar dado clinico, objeto de conhecimento, evidencia, relacao semantica e conclusao apresentada.

Sem justificativa, a informacao nao deve ser exibida como clinicamente sustentada.

## 8. Auditoria

Auditoria deve permitir responder:

- qual dado foi usado;
- qual fonte sustentou;
- qual versao estava ativa;
- qual motor participou;
- qual incerteza existia;
- qual explicacao foi produzida;
- quando a informacao foi revisada.

## 9. Cadeia Minima

```text
dado ou afirmacao
  -> objeto de conhecimento
  -> fonte/evidencia
  -> versao/status
  -> relacao clinica
  -> raciocinio
  -> explicacao
  -> auditoria
```

## 10. Limites

Este documento nao define implementacao de logs, banco de dados, trilhas tecnicas ou ferramentas de auditoria.

## 11. Declaracao Final

O Traceability Model garante que o PsychRx possa explicar de onde veio cada informacao.

No PsychRx, nada clinicamente relevante deve existir sem origem, evidencia, versao, justificativa e capacidade de auditoria.
