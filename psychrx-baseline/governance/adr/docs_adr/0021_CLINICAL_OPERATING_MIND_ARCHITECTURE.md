# ADR 0021 - Clinical Operating Mind Architecture

## Status

Accepted.

## Contexto

Programs 10 a 17 criaram Runtime, Safety, Evidence, Therapeutic Optimization, Explanation, Snapshot, Timeline e Navigation. Era necessario consolidar esses motores em um modelo operacional unico, rastreavel e governado.

## Decisao

Criar `clinical_operating_mind/` como camada nuclear de coordenacao estrutural read-only, integrada ao Clinical Runtime e exposta ao Clinical Workspace.

## Alternativas Consideradas

- manter a coordenacao apenas no Runtime;
- deixar o Workspace consumir motores diretamente;
- adiar a consolidacao para uma fase de IA.

## Justificativa

Separar o Operating Mind reduz acoplamento, explicita ciclo operacional, impede atalhos de seguranca e cria uma fronteira clara entre execucao, experiencia clinica e motores futuros.

## Impacto

- Runtime passa a produzir `clinical_operating_mind`;
- Workspace consome status via App ViewModel;
- mudancas em lifecycle, contratos, ordem de motores ou widget contract exigem ADR.

## Riscos

- duplicar responsabilidade com Runtime;
- transformar coordenacao estrutural em decisao clinica;
- permitir bypass de Safety ou Evidence.

## Mitigacoes

- Operating Mind nao executa conduta;
- Runtime permanece camada de execucao;
- testes cobrem ordem, contratos, gate de seguranca, trace e proibicoes.

## Documentos Afetados

- `docs/440_CLINICAL_OPERATING_MIND.md`
- `docs/PROGRAM_18_BASELINE.md`
- `governance/execution/PROJECT_TREE.md`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/NEXT_MISSION.md`

## Criterios de Revisao Futura

Revisar esta ADR antes de qualquer alteracao no lifecycle, contratos, engine order ou contrato dos Clinical Widgets.

