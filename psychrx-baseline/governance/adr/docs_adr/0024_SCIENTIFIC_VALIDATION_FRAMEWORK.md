# ADR 0024 - Scientific Validation Framework

## Status

Accepted.

## Contexto

O PsychRx precisa impedir que conhecimento clinico entre no Knowledge Layer sem fonte, versao, qualidade, revisao editorial, trace e publication decision.

## Decisao

Criar `scientific_validation/` como Scientific Validation Framework isolado do Runtime, responsavel por governar o ciclo de vida cientifico.

## Alternativas Consideradas

- deixar Evidence Runtime validar fontes diretamente;
- inserir conhecimento manualmente no Knowledge Layer;
- adiar governanca cientifica para producao.

## Justificativa

Separar validacao cientifica da execucao clinica preserva rastreabilidade, reduz risco e garante que o Runtime consuma apenas conhecimento previamente validado.

## Impacto

- App expoe status read-only do SVF;
- Runtime nao acessa SVF;
- Knowledge Layer so deve aceitar entradas validadas.

## Riscos

- confundir validacao cientifica com recomendacao clinica;
- permitir bypass do Publication Gate;
- duplicar responsabilidade com Evidence Runtime.

## Mitigacoes

- SVF nao interpreta casos;
- Evidence Runtime permanece consumidor;
- Publication Gate exige qualidade, editorial, trace e versao.

## Documentos Afetados

- `docs/516_SCIENTIFIC_VALIDATION_FRAMEWORK.md`
- `docs/PROGRAM_21_BASELINE.md`
- `governance/execution/PROJECT_TREE.md`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/NEXT_MISSION.md`

## Criterios de Revisao Futura

Revisar esta ADR antes de alterar Publication Gate cientifico, hierarquia de evidencia, versionamento ou integracao com Knowledge Layer.

