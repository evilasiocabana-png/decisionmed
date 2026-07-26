# DM-301 — Baseline da missão DM-300

## Estado capturado

O baseline foi registrado em 26 de julho de 2026, antes da migração do motor
clínico para o catálogo governado de 300 módulos.

- branch: `main`;
- commit de referência: `c2e0f6d3fe45c61fa088fecc38e6d0c1bb7258c2`;
- motor local de raciocínio: `0.2.0`;
- entradas clínicas no protótipo: 14;
- testes Python: 250 aprovados;
- testes Node: 20 aprovados.

O inventário legível por máquina está em
`docs/baselines/dm300-phase0-module-inventory.json`.

## Fronteiras encontradas

O repositório da plataforma já possui:

- loader externo estrito;
- manifesto de release;
- validação de SHA-256;
- registros de evidência, conhecimento, formulários e segurança;
- gates que mantêm execução clínica bloqueada;
- auditoria e contratos de raciocínio.

O repositório externo `DecisionMEd-Knowledge` já existe e está limpo, com
release `0.10.0`, schema `7.0.0` e conteúdo em `draft`.

O protótipo de anamnese ainda mantém as 14 definições clínicas diretamente em
`decisionmed/static/intake-reasoning.js`. Essa é a principal dívida a remover
antes da expansão: multiplicar esse arquivo por 300 criaria conteúdo
duplicado, difícil de versionar e impossível de governar adequadamente.

## Estratégia de compatibilidade

As 14 chaves existentes não serão renomeadas durante a migração. Cada uma terá
um módulo externo correspondente e um alias de compatibilidade. Assim:

- casos sintéticos antigos continuam reproduzíveis;
- trilhas de auditoria continuam resolvendo o nome registrado;
- links entre roteamento, perguntas e raciocínio não quebram;
- nomes e tipos clínicos podem evoluir por versão sem alterar a identidade.

## Critério para avançar

A fase 0 é considerada atendida quando:

1. o JSON de inventário valida;
2. sua contagem corresponde ao catálogo exportado pelo motor `0.2.0`;
3. os 270 testes de baseline permanecem aprovados;
4. nenhuma alteração é feita no PsychRx original.
