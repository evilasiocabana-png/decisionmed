# PsychRx Enterprise Roadmap

## Relacao com o Master Development Plan

O `MASTER_DEVELOPMENT_PLAN.md` e o plano diretor de execucao do PsychRx.

Este roadmap permanece como mapa sequencial resumido. O MDP governa a decomposicao por volumes, programas, fases, sprints, missoes, gates e Definition of Done.

## Objetivo

Este documento reorganiza o roadmap do PsychRx em uma sequencia enterprise, adequada a uma plataforma medica de apoio ao raciocinio clinico em psicofarmacologia.

O roadmap preserva os documentos fundadores, nao altera a Constituicao Clinica, nao cria conteudo clinico novo e nao autoriza prescricoes automaticas.

## Principio Central

O PsychRx deve evoluir na seguinte ordem:

```text
Arquitetura
-> Dominio
-> Conhecimento
-> Clinical Kernel
-> Motores
-> UX
-> Dashboard
-> API
-> Persistencia
-> IA
```

A IA nao decide. A IA apoia.

## Roadmap Sequencial

| Sprint | Nome | Missoes |
| --- | --- | --- |
| 0 | Governanca Arquitetural | 000-007 |
| 1 | Fundacao Cientifica | 008-015 |
| 2 | Arquitetura Cientifica | 016-023 |
| 3 | Motores Conceituais | 024-031 |
| 4 | Nucleo do Raciocinio Clinico | 032-039 |
| 5 | Modelo Computacional do Conhecimento | 040-047 |
| 6 | Engineering Blueprint | 048-055 |
| 7 | Domain Core | 056-063 |
| 8 | Knowledge Layer | 064-071 |
| 9 | Biblioteca Cientifica | 072-079 |
| 10 | Clinical Kernel | 080-087 |
| 11 | Clinical Reasoning Engines | 088-095 |
| 12 | Safety Platform | 096-103 |
| 13 | Therapeutic Intelligence | 104-111 |
| 14 | Clinical Experience | 112-119 |
| 15 | Dashboard Medico | 120-127 |
| 16 | Mobile Experience | 128-135 |
| 17 | API Clinica | 136-143 |
| 18 | Persistencia | 144-151 |
| 19 | Auditoria | 152-159 |
| 20 | Simulacoes Clinicas | 160-167 |
| 21 | Validacao Cientifica | 168-175 |
| 22 | Performance | 176-183 |
| 23 | Seguranca | 184-191 |
| 24 | Release Candidate | 192-199 |
| 25 | Clinical AI Assistant | 200-209 |
| 26 | PsychRx GPT | 210-219 |
| 27 | Multiagentes Clinicos | 220-229 |
| 28 | Dashboard Definitivo | 230-239 |
| 29 | Producao | 240-249 |
| 30 | Evolucao Continua | 250-259 |

## Trilhas Paralelas

O roadmap deve ser executado por trilhas sincronizadas por milestones:

1. Arquitetura e Engenharia: software, contratos, APIs, infraestrutura e integracao.
2. Conhecimento Cientifico: diretrizes, psicofarmacos, evidencias e governanca.
3. Experiencia Clinica: consulta, dashboard, mobile e ergonomia medica.
4. Qualidade e Governanca: testes, auditoria, validacao cientifica e rastreabilidade.
5. Inteligencia Clinica: IA assistiva, recuperacao de evidencias e agentes.

## Regra de Evolucao

Nenhuma trilha pode introduzir:

- prescricao automatica;
- decisao clinica sem medico;
- regra terapeutica sem fonte rastreavel;
- conhecimento cientifico hardcoded;
- interface que decida conduta;
- API que contorne safety, auditoria ou explicabilidade.

## Estado de Implementacao Documental

Os documentos 112-143 foram criados como especificacoes conceituais iniciais dos Sprints 14-17, porque o anexo definiu explicitamente seus nomes e objetivos.

Os documentos 144-259 permanecem como backlog futuro e devem ser decompostos em novas missoes antes da execucao.

## Declaracao Final

O PsychRx passa a possuir um roadmap enterprise oficial, com separacao entre arquitetura, conhecimento, experiencia clinica, qualidade e inteligencia assistiva, preservando o medico como decisor final.
