# ADR 0025 - Knowledge Governance Platform

## Status

Accepted.

## Contexto

O Scientific Validation Framework governa qualidade cientifica, mas o PsychRx tambem precisa de autoridade separada para consistencia semantica de ontologias, entidades, relacionamentos, taxonomias e grafos.

## Decisao

Criar `knowledge_governance_platform/` como plataforma de governanca semantica isolada do Runtime.

## Alternativas Consideradas

- misturar governanca semantica com Scientific Validation Framework;
- permitir que Knowledge Layer aceite estruturas sem validacao semantica;
- deixar a Ontologia como documento estatico.

## Justificativa

Separar governanca cientifica e governanca semantica reduz acoplamento, evita deriva conceitual e permite evolucao controlada do Knowledge Graph.

## Impacto

- App expoe status read-only da KGP;
- Runtime nao acessa KGP;
- Knowledge Layer deve aceitar apenas estruturas semanticamente validadas.

## Riscos

- duplicar responsabilidade com SVF;
- bloquear evolucao de conhecimento por validacao semantica excessiva;
- confundir validacao semantica com validacao cientifica.

## Mitigacoes

- KGP governa estrutura, SVF governa ciencia;
- KGP nao interpreta casos;
- Migration Planner nao executa migracoes automaticas.

## Documentos Afetados

- `docs/540_KNOWLEDGE_GOVERNANCE_PLATFORM.md`
- `docs/PROGRAM_22_BASELINE.md`
- `governance/execution/PROJECT_TREE.md`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/NEXT_MISSION.md`

## Criterios de Revisao Futura

Revisar esta ADR antes de alterar validacao semantica, versionamento, compatibilidade ou contratos com Knowledge Layer.

