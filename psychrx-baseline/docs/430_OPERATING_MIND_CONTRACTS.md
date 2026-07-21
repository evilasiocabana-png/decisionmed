# 430 - Operating Mind Contracts

## Objetivo

Documentar os contratos internos do Clinical Operating Mind.

## Regras de fronteira

- Runtime executa, mas nao decide.
- Safety sempre precede Optimization.
- Evidence e lida antes de hipoteses terapeuticas.
- Explanation consolida justificativas e limites.
- Snapshot consolida o estado computacional.
- Timeline registra a evolucao longitudinal.
- Navigation expoe contexto ao Workspace.

## Imutabilidade

Resultados upstream devem ser consumidos como read-only.

## Trace

Toda execucao deve carregar referencias para Runtime, Safety, Evidence, Optimization, Explanation, Snapshot, Timeline e Navigation.

## Declaracao Final

Os contratos do Operating Mind tornam o nucleo operacional verificavel e rastreavel.

