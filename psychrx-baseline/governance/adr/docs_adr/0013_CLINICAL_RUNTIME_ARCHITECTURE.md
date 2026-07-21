# ADR 0013 - Clinical Runtime Architecture

## Status

Accepted

## Contexto

PsychRx precisa de uma camada de execucao que coordene Workspace, Kernel e Knowledge Library sem misturar coordenacao tecnica com raciocinio clinico.

## Decisao

Criar `clinical_runtime/` como orquestrador estrutural read-only, com session, context, pipeline, scheduler, events, store, validator, audit, trace, replay e integration.

## Alternativas

- Executar diretamente pelo Clinical Kernel.
- Colocar coordenacao na Application Layer.

## Justificativa

Separar Runtime evita acoplamento entre interface, kernel e conhecimento, preservando rastreabilidade e testabilidade.

## Impacto

Program 10 passa a ser a camada de coordenacao tecnica. Motores clinicos futuros deverao ser plugados sem criar regras hardcoded no runtime.

## Riscos

Runtime pode crescer demais se receber logica clinica. Essa decisao proibe esse acoplamento.

## Revisao Futura

Revisar antes de Program 11 - Safety Engine.
