# ADR 0016 - Therapeutic Optimization Engine Architecture

## Status

Accepted.

## Contexto

Apos Clinical Runtime, Safety Engine e Evidence Runtime, o PsychRx precisa de um primeiro motor de raciocinio capaz de estruturar hipoteses terapeuticas sem prescrever.

## Decisao

Criar `therapeutic_optimization/` como pacote independente e read-only, integrado ao Runtime apos Evidence e antes do Kernel.

## Alternativas Consideradas

- Implementar otimizacao dentro do Kernel: rejeitado por acoplamento.
- Expor estrategias diretamente no Workspace: rejeitado porque interface nao decide logica clinica.
- Adiar o motor ate conhecimento real: rejeitado porque contratos e limites precisam existir antes do conteudo.

## Justificativa

TOE deve comparar candidatos, produzir hipoteses e explicar incertezas sem gerar conduta automatica.

## Impacto

- Runtime passa a executar Optimization apos Evidence.
- Workspace passa a exibir Therapeutic Optimization Status Widget.
- Strategy Widget permanece nao prescritivo.

## Riscos

- Confundir hipotese com recomendacao.
- Transformar score em ranking prescritivo.
- Inserir conhecimento terapeutico hardcoded.

## Mitigacoes

- Testes contra prescricao.
- Documentacao explicita de limites.
- `SafetyResult` e `EvidenceResult` read-only.

## Documentos Afetados

- `governance/execution/PROJECT_STATUS.md`;
- `governance/execution/PROJECT_PROGRESS.md`;
- `governance/execution/PROJECT_TREE.md`;
- `governance/execution/PROJECT_INDEX.md`;
- `governance/execution/NEXT_MISSION.md`;
- `docs/PROGRAM_13_BASELINE.md`.

## Criterios de Revisao Futura

Revisar antes de conectar conhecimento terapeutico validado ou expor hipoteses em fluxo clinico real.
