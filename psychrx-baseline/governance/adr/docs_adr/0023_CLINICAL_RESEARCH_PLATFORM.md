# ADR 0023 - Clinical Research Platform

## Status

Accepted.

## Contexto

Com Clinical Operating Mind e Clinical Quality estabelecidos, o PsychRx precisa de um ambiente separado para testar arquiteturas, motores e modelos sem impactar a operacao clinica.

## Decisao

Criar `clinical_research/` como Clinical Research Platform isolada do Clinical Runtime.

## Alternativas Consideradas

- executar experimentos dentro do Runtime;
- usar o Workspace como ambiente de pesquisa;
- adiar pesquisa ate producao.

## Justificativa

Separar pesquisa de operacao reduz risco, preserva governanca e permite benchmarking reprodutivel antes de qualquer promocao.

## Impacto

- App expõe status read-only da CRP;
- Runtime nao consome CRP;
- promocoes exigem ADR, documentacao, benchmark e validacao.

## Riscos

- misturar pesquisa com atendimento;
- promover componentes experimentais sem governanca;
- confundir benchmark estrutural com validacao clinica.

## Mitigacoes

- CRP nao integra ao Runtime;
- Promotion Pipeline exige governanca;
- testes garantem isolamento e ausencia de prescricoes.

## Documentos Afetados

- `docs/492_CLINICAL_RESEARCH_PLATFORM.md`
- `docs/PROGRAM_20_BASELINE.md`
- `governance/execution/PROJECT_TREE.md`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/NEXT_MISSION.md`

## Criterios de Revisao Futura

Revisar esta ADR antes de qualquer integracao da CRP com producao, Runtime ou Knowledge Layer validado.

