# DM-023 — Integridade da release do catálogo

Cada catálogo externo agora exige `catalog-manifest.json` com identidade,
versão, status de revisão e SHA-256 de `evidence.json`, `knowledge.json` e
`form-schemas.json`.

Os hashes são verificados antes do parsing e das referências cruzadas. Qualquer
alteração posterior à emissão do manifesto falha fechada. Status `validated`
também exige data de revisão e identificador do validador humano.

O manifesto é imutável e nunca libera execução clínica. Assinatura criptográfica
e distribuição confiável permanecem etapas futuras; SHA-256 aqui garante
integridade de conteúdo, não identidade do publicador.
