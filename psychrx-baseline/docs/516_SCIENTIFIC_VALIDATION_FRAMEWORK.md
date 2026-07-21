# Scientific Validation Framework

## Proposito

O Scientific Validation Framework e a camada oficial de governanca cientifica do PsychRx.

Ele controla a incorporacao, revisao, atualizacao, versionamento, publicacao e aposentadoria de conhecimento cientifico.

## Limites

O SVF nao interpreta casos clinicos, nao participa do Runtime, nao gera hipoteses, nao recomenda e nao prescreve.

## Arquitetura

```text
Scientific Sources
-> Scientific Validation Framework
-> Knowledge Repository
-> Evidence Runtime
-> Clinical Operating Mind
```

## Validation Workflow

1. Registrar fonte.
2. Registrar metadados.
3. Avaliar qualidade.
4. Registrar conflitos.
5. Revisar editorialmente.
6. Atribuir versao.
7. Aplicar Publication Gate.
8. Emitir release report.

## Editorial Process

Revisoes exigem estado, revisores e justificativa.

## Knowledge Lifecycle

```text
candidate -> validated -> active -> deprecated -> retired -> archived
```

## Governance

Nenhum conhecimento cientifico entra no Knowledge Layer sem fonte, versao, revisao editorial, trace e publication decision.

## Developer Guide

Novos validadores devem retornar relatorios estruturados, preservar fontes, nao inferir aplicabilidade clinica individual e nunca criar recomendacao.

## Declaracao Final

O Scientific Validation Framework impede conhecimento clinico sem fonte e separa validacao cientifica de execucao clinica.

