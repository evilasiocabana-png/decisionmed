# ADR 0027 - Clinical Simulation Platform

## Status

Accepted.

## Contexto

O Digital Clinical Twin permite representacao longitudinal computacional. O PsychRx precisa de um ambiente isolado para experimentar cenarios sobre clones do Twin sem alterar estado oficial.

## Decisao

Criar `clinical_simulation/` como plataforma de simulacao isolada, read-only em relacao a producao e sem integracao com Clinical Runtime.

## Alternativas Consideradas

- simular diretamente no Twin oficial;
- usar Clinical Runtime para simulacoes;
- adiar simulacao para a camada de inteligencia.

## Justificativa

Separar simulacao de operacao protege o Twin oficial, preserva rastreabilidade e permite pesquisa reprodutivel.

## Isolation Guarantees

- simulacao usa clones;
- nenhuma mutacao de producao;
- nenhum Runtime clinico chamado;
- nenhum resultado retorna automaticamente ao Twin oficial;
- export de producao e proibido.

## Impacto

- App expoe status read-only da CSP;
- Research Platform podera lancar simulacoes futuras;
- DCTP fornece apenas fonte de clone.

## Riscos

- confundir simulacao com recomendacao;
- contaminar estado oficial;
- usar outputs simulados como conduta.

## Mitigacoes

- CSP nao prescreve;
- CSP nao modifica producao;
- testes garantem isolamento.

## Documentos Afetados

- `docs/588_CLINICAL_SIMULATION_PLATFORM.md`
- `docs/PROGRAM_24_BASELINE.md`
- `governance/execution/PROJECT_TREE.md`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/NEXT_MISSION.md`

## Criterios de Revisao Futura

Revisar esta ADR antes de qualquer integracao da CSP com pesquisa ativa, inteligencia clinica ou componentes de simulacao avancada.

