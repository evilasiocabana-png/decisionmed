# DM-031 — Catálogo real no painel de prontidão

## Problema

O serviço da aplicação recebia um catálogo externo válido, mas construía o
painel técnico com registries vazios. A API informava simultaneamente catálogo
carregado e contagens iguais a zero.

## Correção

Quando nenhum serviço de prontidão customizado é fornecido, a aplicação agora
injeta os registries de evidência e conhecimento do `GovernedCatalogs` carregado.
Injeção explícita continua tendo precedência para testes e integrações.

## Segurança

As contagens corrigem apenas observabilidade técnica. Catálogo presente não
libera execução: validação humana, configuração de segurança e gate regulatório
continuam bloqueados.

## Verificação

O teste HTTP confirma que um catálogo sintético com uma fonte e um objeto produz
contagens `1/1`, enquanto `clinical_execution_allowed` permanece falso.
