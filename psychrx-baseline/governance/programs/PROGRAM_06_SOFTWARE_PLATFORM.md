# Program 06 - Software Platform

## Status

Programa oficial conforme `MASTER_DEVELOPMENT_PLAN.md`.

Estado atual: baseline read-only validada.

## Objetivo

Definir e validar a plataforma de software inicial do PsychRx sem implementar logica clinica, prescricao, IA, persistencia ou motores clinicos reais.

## Escopo

O Programa 06 cobre:

- Domain Layer;
- Application Layer;
- Interfaces;
- Adapters;
- Infrastructure;
- Audit;
- testes de estrutura;
- app localhost read-only;
- contratos de independencia entre camadas.

## Fora de Escopo

O Programa 06 nao autoriza:

- prescricao automatica;
- decisao clinica;
- implementacao de motores clinicos;
- IA clinica;
- banco de dados;
- API clinica real;
- dados reais de pacientes;
- regras terapeuticas executaveis.

## Baseline Atual

```text
domain/
application/
interfaces/
adapters/
infrastructure/
audit/
tests/
```

## Componentes Existentes

### Domain

Estrutura inicial de pacote existe.

Status: estrutural, sem entidades clinicas implementadas.

### Application

Fachada inicial existe para alimentar o app localhost read-only.

Status: apresentacional, sem decisao clinica.

### Interfaces

Interface web local existe.

Status: read-only, sem formularios clinicos reais, sem prescricao e sem IA.

### Adapters

Diretorio existe como fronteira futura.

Status: sem integracoes reais.

### Infrastructure

Diretorio existe como fronteira futura.

Status: sem banco, sem filas, sem servicos externos.

### Audit

Diretorio existe como fronteira futura.

Status: sem pipeline real de auditoria.

## Dependencias Permitidas

```text
Interfaces -> Application
Clinical Experience -> Application
Application -> contratos internos
```

## Dependencias Proibidas

```text
Domain -> Application
Domain -> Interface
Interface -> Infrastructure
Interface -> Clinical Decision
Application -> prescritor automatico
Software Platform -> regra terapeutica hardcoded
```

## Missoes Validadas

| Missao | Artefato | Status |
| --- | --- | --- |
| 051 | `051_DOMAIN_IMPLEMENTATION_SPEC.md` | Validada como especificacao futura |
| Localhost App Shell | `LOCALHOST_APP.md` e app local | Validado read-only |
| Clinical Experience Bridge | app exibe Clinical Experience Layer | Validado read-only |

## Lacunas

- Missoes 052-064 ainda precisam reconciliacao.
- Domain Core real ainda nao deve ser implementado sem missao especifica.
- Application Layer ainda nao possui contratos clinicos reais.
- Audit Layer ainda nao possui pipeline real.
- Infrastructure ainda nao possui servicos reais.

## Gate do Programa 06

O Programa 06, nesta execucao, e considerado completo apenas como baseline read-only quando:

- app localhost responde em modo read-only;
- testes automatizados passam;
- domain permanece independente;
- interface nao decide conduta;
- nao ha prescricao;
- nao ha IA clinica;
- nao ha banco de dados;
- conflito de numeracao fica documentado por ADR.

## Proxima Evolucao Permitida

Antes de implementar Domain Core real, executar uma missao especifica de reconciliacao das missoes 052-064 ou seguir a proxima missao autorizada em `NEXT_MISSION.md`.

## Declaracao Final

O Programa 06 estabelece a Software Platform como base tecnica inicial do PsychRx, mantendo a plataforma em modo read-only, independente de tecnologia clinica real e incapaz de prescrever ou decidir conduta.
