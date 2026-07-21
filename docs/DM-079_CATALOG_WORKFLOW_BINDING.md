# DM-079 — Vínculo entre catálogo e fluxo

## Objetivo

Impedir que um schema de referência carregado pelo catálogo aponte para uma
especialidade, contrato de fluxo ou etapa inexistente no produto.

## Garantias

- Cada schema é verificado na composição do aplicativo contra o fluxo da sua
  especialidade.
- Um contrato de fluxo divergente ou uma etapa inexistente interrompe a
  inicialização do aplicativo.
- O estado público informa, por especialidade, quais etapas possuem schema de
  referência e quais ainda não possuem cobertura.

## Limites

Cobertura de schema é somente um indicador de organização do catálogo. Ela não
valida conteúdo, não coleta dados de paciente, não produz recomendação e não
libera execução clínica.
