# 306 - Optimization Coordinator

## Objetivo

Criar o coordenador estrutural do TOE.

## Responsabilidades

- receber contexto runtime;
- receber `SafetyResult`;
- receber `EvidenceResult`;
- coordenar goals, generator, matcher, comparator, scoring, explanation e hypothesis;
- produzir `TherapeuticOptimizationResult`.

## Declaracao Final

Optimization Coordinator organiza o fluxo de hipoteses sem decidir conduta.
