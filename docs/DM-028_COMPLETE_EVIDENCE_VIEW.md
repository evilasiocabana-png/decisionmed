# DM-028 — Visualização completa da evidência

## Objetivo

Completar a explicabilidade dos formulários em modo referência. A API e a tela
passam a apresentar os metadados científicos que já existem no catálogo, sem
interpretá-los nem produzir uma conclusão clínica.

## Contrato da API

Cada campo expõe o objeto de conhecimento com nome, tipo, descrição,
aplicabilidade, limites, versão e status. Cada `EvidenceSource` inclui:

- título, ano, tipo e localizador público seguro;
- qualidade e força registradas;
- versão, status e data de revisão interna;
- especialidades, conflitos conhecidos e aplicabilidade clínica;
- `runtime_eligible: false`.

Schema, campo, objeto e fonte permanecem explicitamente sem elegibilidade de
runtime e sem autorização de execução clínica.

## Interface

A página apresenta os dados em um painel expansível “Base científica e limites”.
O JavaScript apenas renderiza o contrato recebido da Application Layer usando
`textContent`; ele não consulta o catálogo diretamente nem interpreta evidência.

## Reversão

Reverter o commit desta missão remove os metadados adicionais da resposta e o
painel visual, preservando o catálogo e a API de formulários anterior.
