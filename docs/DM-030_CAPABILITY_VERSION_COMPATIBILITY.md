# DM-030 — Compatibilidade de versões das capacidades

## Objetivo

Impedir que um pacote de especialidade seja composto com uma implementação de
capacidade cuja versão de contrato seja diferente da declarada pelo pacote.

## Contrato

Cada `CapabilityRequirement` contém:

- identificador canônico da capacidade;
- versão semântica exata requerida.

O `SpecialtyPack` mantém requisitos únicos e deriva deles a lista pública
`required_capabilities`. O resolver compara cada requisito com o
`CapabilityBinding` disponível.

Uma capacidade inexistente produz `missing_capability`. Uma capacidade presente
em versão diferente produz `incompatible_capability`, registra as versões
requerida e encontrada e bloqueia a composição. A API também expõe a lista
`incompatible_capabilities` para diagnóstico técnico.

## Limites de segurança

- Compatibilidade exata foi escolhida para falhar de forma conservadora; ranges
  semânticos podem ser introduzidos apenas em contrato futuro explícito.
- Compatibilidade técnica não equivale a validação científica, regulatória ou
  autorização de execução clínica.
- Nenhuma lógica, recomendação ou dado clínico foi adicionado.

## Rollback

Reverter a missão restaura requisitos sem versão. Pacotes e bindings atuais usam
`0.1.0`, portanto a mudança não altera o estado operacional `reference_only`.
