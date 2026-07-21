# ADR 0015 - Evidence Runtime Architecture

## Status

Accepted.

## Contexto

O PsychRx precisa disponibilizar evidencias cientificas para motores clinicos em tempo de execucao sem misturar conhecimento cientifico com algoritmo e sem permitir recomendacao terapeutica sem rastreabilidade.

## Decisao

Criar `evidence_runtime/` como pacote independente e read-only, integrado ao Clinical Runtime apos Safety Engine e antes do Clinical Kernel.

## Alternativas Consideradas

- Colocar evidencia diretamente no Kernel: rejeitado por acoplamento.
- Fazer motores consultarem Knowledge diretamente: rejeitado por perda de contrato e rastreabilidade.
- Adiar Evidence Runtime: rejeitado porque motores futuros precisam de `EvidenceResult` padronizado.

## Justificativa

Evidence Runtime fornece evidencias, citacoes, versoes, snapshot e auditoria sem interpretar ciencia nem recomendar conduta.

## Impacto

- Runtime passa a executar Evidence apos Safety.
- Workspace passa a exibir Evidence Runtime Status Widget.
- Strategy Widget permanece bloqueado.

## Riscos

- Confundir ranking hierarquico com recomendacao.
- Inserir evidencia real sem validacao.
- Permitir que Knowledge dependa de Runtime.

## Mitigacoes

- Testes de ausencia de recomendacao.
- Documentacao explicita de limites.
- Contrato unidirecional Knowledge -> Evidence Runtime.

## Documentos Afetados

- `governance/execution/PROJECT_STATUS.md`;
- `governance/execution/PROJECT_PROGRESS.md`;
- `governance/execution/PROJECT_TREE.md`;
- `governance/execution/PROJECT_INDEX.md`;
- `governance/execution/NEXT_MISSION.md`;
- `docs/PROGRAM_12_BASELINE.md`.

## Criterios de Revisao Futura

Revisar quando o primeiro conjunto validado de evidencias reais for conectado ao runtime.
