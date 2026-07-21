# ADR 0012 - Presentation Clinical Widget Architecture

## Status

Aceito.

## Data

2026-06-30

## Contexto

O Clinical Workspace passou a ser organizado por microexperiencias clinicas chamadas Clinical Widgets. Para evitar que cada widget vire um componente isolado sem contrato comum, foi necessario definir uma arquitetura de apresentacao propria.

## Decisao

Criar a estrutura conceitual:

```text
presentation/
    clinical_workspace/
        widgets/
        layouts/
        workspace/
        investigation/
        timeline/
        strategy/
        monitoring/
        patient/
        shared/
```

Criar tambem `docs/CLINICAL_WIDGET_SPECIFICATION.md` como biblioteca oficial de componentes clinicos.

Cada Clinical Widget devera possuir, quando implementado:

```text
id
title
priority
state
context
dependencies
actions
explanation
visibility
permissions
```

## Justificativa

O Clinical Workspace nao deve ser tratado como frontend generico. Ele e uma camada de apresentacao clinica orientada a microexperiencias reutilizaveis.

Padronizar Clinical Widgets antes da implementacao reduz duplicacao, evita retrabalho e permite que Clinical Kernel, desktop, tablet e mobile alimentem ou exibam os mesmos contratos.

## Impacto

- cria `presentation/clinical_workspace/`;
- cria `CLINICAL_WIDGET_SPECIFICATION.md`;
- atualiza `PROJECT_STATUS.md`;
- atualiza `PROJECT_INDEX.md`;
- adiciona teste estrutural da camada de apresentacao.

## Riscos

- Presentation ser confundida com Interface final.
- Widget ser confundido com motor clinico.
- Confidence Widget parecer diagnostico automatico.
- Investigation Workflow parecer IA.

## Mitigacoes

- Presentation organiza apresentacao, nao decide conduta.
- Widgets nao prescrevem.
- Widgets nao acessam knowledge, evidence, reasoning ou safety diretamente.
- Medico permanece decisor final.
- Clinical Kernel futuro alimenta widgets por contratos de application.

## Declaracao Final

A arquitetura de Presentation Clinical Widget transforma o Clinical Workspace em uma biblioteca de microexperiencias clinicas reutilizaveis, sem autorizar prescricao, IA ou raciocinio clinico automatico.
