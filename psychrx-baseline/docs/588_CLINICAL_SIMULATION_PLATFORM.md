# Clinical Simulation Platform

## Proposito

A Clinical Simulation Platform executa simulacoes controladas sobre clones do Digital Clinical Twin em ambiente isolado.

## Limites

A CSP nao atende pacientes, nao altera Clinical Operating Mind, nao modifica o Twin oficial, nao produz prescricao automatica e nao interfere na operacao clinica.

## Arquitetura

```text
Clinical Workspace
-> Digital Clinical Twin
-> Clinical Simulation Platform
-> Simulation Runtime
-> Experimental Results
```

## Sandbox Model

Toda simulacao ocorre em sandbox isolado, com estado temporario e cleanup automatico.

## Scenario Lifecycle

draft -> configured -> validated -> running -> completed -> archived.

## Branch Model

Branches sao ramificacoes imutaveis e comparaveis de trajetorias simuladas.

## Reporting

Relatorios sao artefatos de pesquisa e desenvolvimento, sem recomendacao clinica.

## Developer Guide

Novas simulacoes devem operar apenas sobre clones, nunca sobre o Twin oficial ou Runtime clinico.

## Declaracao Final

A CSP permite experimentacao computacional controlada sem comprometer seguranca clinica, rastreabilidade ou governanca.

