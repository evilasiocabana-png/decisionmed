# ADR 0014 - Safety Engine Architecture

## Status

Accepted.

## Contexto

O PsychRx precisa de um motor transversal de seguranca antes de qualquer motor terapeutico. A arquitetura exige seguranca antes de estrategia, separacao entre conhecimento cientifico e algoritmo, rastreabilidade e medico como decisor final.

## Decisao

Criar `safety_engine/` como pacote independente, integrado ao Clinical Runtime antes de Kernel e Knowledge, expondo `SafetyResult`, `SafetySnapshot`, `BlockingDecision`, alertas, auditoria e trace em modo read-only.

## Alternativas Consideradas

- Colocar seguranca dentro do Clinical Runtime: rejeitado por acoplamento.
- Colocar seguranca dentro do Kernel: rejeitado por misturar orquestracao com regra transversal.
- Adiar Safety Engine ate conhecimento real: rejeitado porque o contrato de seguranca precisa existir antes das regras.

## Justificativa

Safety Engine deve ser um guardiao arquitetural transversal, sem prescrever e sem conter conhecimento clinico hardcoded.

## Impacto

- Runtime passa a executar Safety antes de Kernel e Knowledge.
- Workspace passa a exibir Safety Engine Status Widget.
- Strategy Widget permanece bloqueado.

## Riscos

- Confundir bloqueio estrutural com decisao clinica real.
- Inserir conhecimento clinico diretamente no codigo em missoes futuras.

## Mitigacoes

- Testes garantindo ausencia de prescricao.
- Documentacao explicita de limites.
- Requisito de conhecimento validado para regras futuras.

## Documentos Afetados

- `governance/execution/PROJECT_STATUS.md`;
- `governance/execution/PROJECT_PROGRESS.md`;
- `governance/execution/PROJECT_TREE.md`;
- `governance/execution/PROJECT_INDEX.md`;
- `governance/execution/NEXT_MISSION.md`;
- `docs/PROGRAM_11_BASELINE.md`.

## Criterios de Revisao Futura

Revisar quando o Evidence Runtime e a primeira regra de seguranca validada forem introduzidos.
