# DM-008 — Domain Core técnico

## Escopo

Cria as abstrações técnicas mínimas do domínio do DecisionMEd: identidade,
entidade, objeto de valor, evento, resultado explícito, erros e contrato de
repositório.

## Limites preservados

- nenhuma entidade ou regra clínica;
- nenhum conhecimento científico;
- nenhum banco, ORM, framework ou implementação de repositório;
- nenhuma recomendação, decisão ou prescrição;
- dependências restritas à biblioteca padrão do Python.

O rollback consiste em reverter o commit da missão. Futuras entidades clínicas
continuam condicionadas à Ontologia, às fontes e aos gates de validação.
