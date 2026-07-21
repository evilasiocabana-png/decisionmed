# DM-024 — Repositório científico independente

## Entrega

Foi criado o repositório privado
[`evilasiocabana-png/decisionmed-knowledge`](https://github.com/evilasiocabana-png/decisionmed-knowledge)
para hospedar a futura base científica sem misturá-la ao software da plataforma.

Estado inicial verificável:

- branch padrão `main`;
- commit raiz `76cb3cdb5d96c7749c13817e73179bb1f50e2ec0`;
- release `0.1.0`, status `draft`;
- zero fontes, zero objetos e zero schemas clínicos;
- manifesto com SHA-256 dos três arquivos;
- CI `validate-catalog` aprovado usando os contratos públicos do DecisionMEd;
- CODEOWNERS e política de contribuição científica presentes.

## Conformidade

A entrega executa a ADR-0002: plataforma e conhecimento possuem versionamento e
revisão independentes. Nenhuma regra, recomendação ou afirmação clínica foi
adicionada. A futura população científica deverá ocorrer em PRs do repositório de
conhecimento, sempre começando em `draft` ou `awaiting_validation`.

## Limites

O repositório privado e seu CI não constituem validação científica, regulatória
ou autorização de uso clínico. Esses gates permanecem bloqueados.
