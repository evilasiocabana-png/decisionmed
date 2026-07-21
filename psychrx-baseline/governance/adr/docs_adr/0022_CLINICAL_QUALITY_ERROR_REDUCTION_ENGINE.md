# ADR 0022 - Clinical Quality & Error Reduction Engine

## Status

Accepted.

## Contexto

O Clinical Operating Mind consolidou o ciclo operacional nuclear do PsychRx. Antes de expor estados ao Workspace, o projeto precisava de uma camada independente para validar completude, consistencia, rastreabilidade e explicabilidade.

## Decisao

Criar `clinical_quality/` como Clinical Quality & Error Reduction Engine, uma camada read-only de Quality Assurance estrutural executada apos o Clinical Operating Mind.

## Alternativas Consideradas

- incorporar validacoes diretamente ao Operating Mind;
- deixar o Workspace detectar inconsistencias;
- adiar quality gate para uma fase de producao.

## Justificativa

Separar qualidade reduz acoplamento, preserva imutabilidade dos motores e cria um Publication Gate verificavel antes da exibicao no Workspace.

## Impacto

- Runtime passa a produzir `clinical_quality`;
- Workspace exibe status de qualidade via App ViewModel;
- Snapshot passa a ter contrato de publicacao governado por Quality Gate.

## Riscos

- confundir quality score estrutural com escore clinico;
- transformar warnings em recomendacoes;
- bloquear indevidamente estados validos por criterios incompletos.

## Mitigacoes

- Quality Score e exclusivamente estrutural;
- CQERE nao recomenda, nao interpreta evidencias e nao altera Snapshot;
- testes cobrem publication gate, trace, completeness e integracao.

## Documentos Afetados

- `docs/468_CLINICAL_QUALITY_ENGINE.md`
- `docs/PROGRAM_19_BASELINE.md`
- `governance/execution/PROJECT_TREE.md`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/NEXT_MISSION.md`

## Criterios de Revisao Futura

Revisar esta ADR antes de alterar publication gate, dimensoes de qualidade, ordem de execucao ou contrato de publicacao do Snapshot.

