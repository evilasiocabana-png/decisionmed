# DM-302 — Registro de módulos clínicos e catálogo v8

## Decisão

O schema `8.0.0` acrescenta `clinical-modules.json` à release externa. O arquivo
contém identidades, tipos ontológicos, relações, aliases legados e governança.
Ele não contém regras executáveis nem autoriza diagnóstico ou conduta.

Releases `7.0.0` continuam aceitas e produzem um registro de módulos vazio.
Essa compatibilidade permite migrar o catálogo sem quebrar instalações atuais.

## Falha fechada

O loader rejeita:

- schema desconhecido;
- arquivo ausente ou com hash divergente;
- campos extras ou ausentes;
- contagem diferente do manifesto;
- ID, nome oficial ou alias legado duplicado;
- relação com módulo inexistente;
- referência a fonte ausente;
- módulo `validated` sem terminologia oficial, conteúdo completo, fontes,
  revisor e prazo vigente.

Mesmo um módulo estruturalmente validado mantém
`clinical_execution_allowed = false`. A identidade do módulo não substitui os
gates de evidência, segurança, raciocínio e autoridade profissional.

## Contratos

- `docs/schemas/catalog-manifest-v8.schema.json`;
- `docs/schemas/clinical-module-registry.schema.json`;
- `decisionmed/knowledge/clinical_modules.py`;
- `decisionmed/application/catalog_loader.py`.
