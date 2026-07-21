# ADR 0020 - Clinical Navigation Engine Architecture

## Status

Accepted.

## Contexto

O PsychRx precisa separar navegacao contextual da apresentacao e dos motores clinicos.

## Decisao

Criar `clinical_navigation/` como pacote independente, read-only, responsavel por estado de navegacao, rotas, breadcrumbs, historico, deep links, sincronizacao de widgets e auditoria.

## Alternativas

- Deixar Workspace controlar navegacao: rejeitado por acoplamento.
- Embutir navegacao nos motores: rejeitado por mistura entre execucao e apresentacao.

## Consequencias

Clinical Workspace delega navegacao para uma camada dedicada.

## Riscos

Navegacao ser confundida com decisao clinica.

## Mitigacoes

Contratos read-only, testes e documentacao explicita.

## Declaracao Final

Clinical Navigation Engine navega artefatos; nao executa raciocinio clinico.
