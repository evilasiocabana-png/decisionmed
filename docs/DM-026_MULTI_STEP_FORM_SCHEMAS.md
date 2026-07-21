# DM-026 — Form schemas por etapa de workflow

## Objetivo

Permitir vários formulários governados na mesma especialidade sem ambiguidade. Cada
`SpecialtyFormSchema` passa a ser vinculado ao trio:

- `specialty_key`
- `workflow_id`
- `step_key`

## Contrato

- `schema_id` continua globalmente único.
- O trio de vinculação também é único no registro.
- Um workflow pode consultar todos os seus formulários de modo determinístico.
- O validador estrutural exige a vinculação completa e não retém valores clínicos.
- O catálogo externo usa `schema_version` `3.0.0`.

## Segurança

Esta missão não adiciona conteúdo, recomendação, cálculo ou regra clínica. Formulários
continuam sem permissão de execução clínica, inclusive quando validados.

## Reversão

Reverter o commit desta missão restaura o contrato anterior de um formulário por
especialidade e o catálogo `2.0.0`.
