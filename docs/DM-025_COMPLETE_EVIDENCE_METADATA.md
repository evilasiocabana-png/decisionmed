# DM-025 — Metadados completos de evidência

## Resultado

`EvidenceSource` agora exige explicitamente toda a cadeia definida pela
`EVIDENCE_TRACEABILITY_POLICY` do PsychRx:

- fonte e localizador;
- ano;
- tipo;
- qualidade (`high`, `moderate`, `low`, `very_low`, `insufficient`);
- força (`strong`, `moderate`, `weak`, `conditional`,
  `insufficient_for_recommendation`);
- data de revisão interna;
- status;
- conflitos conhecidos;
- aplicabilidade clínica.

Não existem valores padrão para esses metadados. Data futura, texto ausente ou
categoria fora do vocabulário falham fechados. O loader externo exige os mesmos
campos e `EvidenceSource.runtime_eligible` permanece sempre falso.

Por ser uma alteração incompatível do envelope de evidência, a versão do
catálogo foi elevada de `1.0.0` para `2.0.0`.

## Migração

Somente fixtures sintéticas foram atualizadas. O catálogo científico externo
continua vazio, portanto não houve reclassificação de conteúdo clínico.

## Limites

Qualidade e força registradas são metadados sujeitos a revisão humana; o software
não as calcula. Mesmo uma fonte com status `validated` não autoriza execução
clínica ou regulatória.
