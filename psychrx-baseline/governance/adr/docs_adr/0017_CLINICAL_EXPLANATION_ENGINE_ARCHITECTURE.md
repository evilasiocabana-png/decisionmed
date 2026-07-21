# ADR 0017 - Clinical Explanation Engine Architecture

## Status

Accepted.

## Contexto

O PsychRx precisa transformar artefatos de Runtime, Safety, Evidence e Therapeutic Optimization em explicacoes compreensiveis, rastreaveis e seguras.

## Decisao

Criar `clinical_explanation/` como pacote independente e read-only, integrado ao Runtime apos Optimization e antes do Kernel.

## Alternativas Consideradas

- Colocar explicacao dentro do Workspace: rejeitado porque interface nao deve decidir ou compor logica.
- Colocar explicacao dentro do Optimization Engine: rejeitado por acoplamento.
- Gerar explicacao apenas no final do Kernel: rejeitado porque Safety, Evidence e Runtime precisam ser navegaveis.

## Consequencias

- Runtime passa a executar Explanation apos Optimization.
- Workspace passa a expor Clinical Explanation Engine Status Widget.
- Explicacoes ficam sob guardrails de linguagem.

## Implicacoes de Seguranca

Explicacoes nao podem conter linguagem prescritiva ou conclusiva. O medico permanece decisor final.

## Impacto de Governanca

Toda explicacao futura deve possuir trace, fonte e limite explicito.

## Documentos Afetados

- `governance/execution/PROJECT_STATUS.md`;
- `governance/execution/PROJECT_PROGRESS.md`;
- `governance/execution/PROJECT_TREE.md`;
- `governance/execution/PROJECT_INDEX.md`;
- `governance/execution/NEXT_MISSION.md`;
- `docs/PROGRAM_14_BASELINE.md`.

## Criterios de Revisao Futura

Revisar quando Clinical Snapshot Engine consolidar os resultados em estado clinico unico.
