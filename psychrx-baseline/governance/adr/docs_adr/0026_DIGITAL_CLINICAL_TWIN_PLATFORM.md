# ADR 0026 - Digital Clinical Twin Platform

## Status

Accepted.

## Contexto

O PsychRx possui Snapshot, Timeline, Operating Mind, Quality, Scientific Validation e Knowledge Governance. O projeto precisa de uma representacao longitudinal unificada do estado computacional produzido por esses componentes.

## Decisao

Criar `digital_clinical_twin/` como plataforma read-only de representacao computacional longitudinal.

## Alternativas Consideradas

- tratar Timeline como Twin;
- representar o Twin no Runtime;
- adiar a representacao longitudinal para a fase de simulacao.

## Justificativa

Separar Twin de Runtime e prontuario preserva a fronteira entre representacao computacional e paciente real, permitindo pesquisa e futura simulacao com seguranca arquitetural.

## Impacto

- App expoe status read-only da DCTP;
- Runtime nao acessa DCTP;
- Research futura podera ler o Twin sem modifica-lo.

## Riscos

- confundir Twin com paciente real;
- confundir Twin com prontuario;
- transformar Twin em mecanismo de recomendacao.

## Mitigacoes

- DCTP nao executa Runtime;
- DCTP nao prescreve;
- DCTP nao representa paciente real;
- testes garantem isolamento.

## Documentos Afetados

- `docs/564_DIGITAL_CLINICAL_TWIN_PLATFORM.md`
- `docs/PROGRAM_23_BASELINE.md`
- `governance/execution/PROJECT_TREE.md`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/NEXT_MISSION.md`

## Criterios de Revisao Futura

Revisar esta ADR antes de integrar DCTP com simulacao, pesquisa longitudinal ou qualquer componente que possa modificar estado oficial.

