# DM-019 — Alinhamento da política de dependências

O verificador criado na DM-016 foi alinhado literalmente ao documento
`LAYER_DEPENDENCY_RULES.md` do baseline PsychRx.

A principal correção permite que `knowledge` use a linguagem conceitual de
`domain`, mantendo proibidas dependências de aplicação e interface. A missão
também antecipa as regras de `reasoning`, `application` e `interface`, evitando
uma nova alteração quando esses pacotes forem materializados.

Não há mudança de runtime, conteúdo clínico ou dados.
