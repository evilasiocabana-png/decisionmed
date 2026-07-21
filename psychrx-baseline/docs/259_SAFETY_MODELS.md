# 259 - Safety Models

## Objetivo

Criar modelos tipados do Safety Engine.

## Modelos

- `Risk`;
- `Constraint`;
- `Contraindication`;
- `Interaction`;
- `Alert`;
- `BlockingDecision`;
- `SafetySnapshot`;
- `SafetyResult`;
- `SafetyTraceReference`.

## Propriedades Arquiteturais

- modelos imutaveis;
- rastreabilidade estrutural;
- sem conhecimento clinico hardcoded;
- serializacao para ViewModel, Runtime e auditoria.

## Declaracao Final

Os Safety Models definem contratos de seguranca rastreaveis, sem incorporar regras terapeuticas ao codigo.
