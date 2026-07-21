# Clinical Operating Mind

## Proposito

O Clinical Operating Mind e o modelo operacional nuclear do PsychRx. Ele organiza como Runtime, Safety, Evidence, Therapeutic Optimization, Explanation, Snapshot, Timeline e Navigation trabalham juntos.

Ele nao e IA clinica, nao prescreve, nao recomenda conduta e nao substitui o medico.

## Arquitetura

```text
Runtime
-> Safety
-> Evidence
-> Optimization
-> Explanation
-> Snapshot
-> Timeline
-> Navigation
-> Clinical Operating Mind
-> Workspace
```

## Lifecycle

1. Context Intake
2. Safety Evaluation
3. Evidence Resolution
4. Therapeutic Hypothesis Generation
5. Explanation Assembly
6. Snapshot Creation
7. Timeline Update
8. Navigation Update

## State Machine

```text
idle
-> context_loaded
-> safety_checked
-> evidence_resolved
-> hypotheses_generated
-> explained
-> snapshot_created
-> timeline_updated
-> navigation_ready
```

Estados alternativos: `blocked` e `error`.

## Contratos

Cada motor possui contrato de entrada, saida, imutabilidade, trace e falha estruturada.

## Governanca

- Safety before Optimization.
- Evidence before Hypothesis.
- Snapshot after Explanation.
- Timeline after Snapshot.
- Navigation never mutates clinical state.
- No prescription output.
- No autonomous clinical decision.

## Falhas

Falhas sao retornadas como erros estruturados. O Operating Mind nao tenta compensar clinicamente, nao inventa dados e nao libera estrategia quando seguranca bloqueia.

## Audit e Trace

Toda execucao possui audit log e trace unificado com referencias aos motores nucleares.

## Extensao futura

Novas mudancas de ciclo, contratos, ordem de motores ou contratos de widgets exigem ADR.

## Declaracao Final

O Clinical Operating Mind fecha a arquitetura nuclear do PsychRx como um modelo operacional seguro, rastreavel, explicavel e read-only.

