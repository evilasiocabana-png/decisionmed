# ADR 0028 - Clinical Intelligence Platform

## Status

Accepted.

## Contexto

O PsychRx possui Operating Mind, Quality, Research, Simulation, Scientific Validation e Knowledge Governance. Para permitir inteligencia futura sem violar a arquitetura, e necessaria uma camada de contratos e governanca antes de qualquer IA real.

## Decisao

Criar `clinical_intelligence/` como plataforma de infraestrutura para futuras capabilities inteligentes, sem implementacao de IA e sem integracao com Clinical Runtime.

## Alternativas Consideradas

- implementar IA diretamente nos motores;
- permitir agentes controlando Operating Mind;
- adiar contratos de inteligencia para fase posterior.

## Justificativa

Definir contratos antes da IA reduz risco de autonomia indevida, preserva explicabilidade e impede bypass dos guardrails nucleares.

## Governance Guarantees

- nenhuma capability controla lifecycle;
- nenhuma capability prescreve;
- nenhuma capability decide autonomamente;
- acesso read-only por padrao;
- outputs sem trace sao rejeitados.

## Impacto

- App expoe status read-only da CIP;
- Runtime nao acessa CIP;
- Research e Simulation poderao avaliar capabilities isoladas.

## Riscos

- confundir infraestrutura de inteligencia com IA clinica;
- permitir inferencia sem contrato;
- permitir output opaco.

## Mitigacoes

- CIP nao implementa IA;
- contratos e governanca sao obrigatorios;
- testes garantem isolamento e ausencia de prescricao.

## Documentos Afetados

- `docs/612_CLINICAL_INTELLIGENCE_PLATFORM.md`
- `docs/PROGRAM_25_BASELINE.md`
- `governance/execution/PROJECT_TREE.md`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/NEXT_MISSION.md`

## Criterios de Revisao Futura

Revisar esta ADR antes de introduzir qualquer capability inteligente real, agente especializado ou inferencia assistiva.

