# Program A08 Blocked Report - Scientific Content Population: MAOIs

## Status

Bloqueado.

## Programa Solicitado

Track A - Scientific Knowledge Expansion

Program A08 - Scientific Content Population: MAOIs

## Objetivo do Programa

Popular cientificamente a classe dos inibidores da monoamina oxidase:

- Phenelzine;
- Tranylcypromine;
- Isocarboxazid;
- Moclobemide.

## Dependencia Declarada no Proprio Programa

O Program A08 depende obrigatoriamente de:

- Track A - Program A07;
- Program 21 - Scientific Validation Framework;
- Program 22 - Knowledge Governance Platform.

## Estado Real das Dependencias

Program 21 e Program 22 estao concluidos.

Program A07 esta bloqueado por dependencia do Program A06.

Program A06 esta bloqueado por dependencia do Program A05.

Program A05 esta bloqueado por dependencia do Program A04.

Program A04 esta bloqueado por dependencia do Program A03.

Program A03 ainda nao concluiu:

- source corpus intake;
- reviewer assignment;
- piloto de populacao e validacao de Fluoxetine;
- validacao semantica por campo;
- publication checklist aprovado.

## Decisao

O Program A08 nao pode ser executado agora.

Executar A08 antes de A03, A04, A05, A06 e A07 violaria:

- ordem oficial de populacao;
- dependencias declaradas pelo proprio Program A08;
- Evidence Traceability Policy;
- Scientific Validation Framework;
- Knowledge Governance Platform;
- Publication Gate;
- ADR 0031 - A03 Scientific Content Population Gate;
- ADR 0032 - Block A04 Until A03 Validation;
- ADR 0033 - Block A05 Until A04 Validation;
- ADR 0034 - Block A06 Until A05 Validation;
- ADR 0035 - Block A07 Until A06 Validation;
- NEXT_MISSION atual.

## Missoes A08 Bloqueadas

- A08-001 - Phenelzine Scientific Population
- A08-002 - Tranylcypromine Scientific Population
- A08-003 - Isocarboxazid Scientific Population
- A08-004 - Moclobemide Scientific Population
- A08-005 - MAOI Mechanism Mapping
- A08-006 - MAOI Pharmacokinetic Mapping
- A08-007 - Drug Interaction Population
- A08-008 - Food Interaction Population
- A08-009 - Hypertensive Crisis Risk
- A08-010 - Washout Requirements
- A08-011 - Switching Contraindications
- A08-012 - Safety Constraint Mapping
- A08-013 - Knowledge Graph Integration
- A08-014 - Evidence Runtime Validation
- A08-015 - Semantic Validation
- A08-016 - Scientific Quality Review
- A08-017 - Safety Consistency Analysis
- A08-018 - Coverage Analysis
- A08-019 - Scientific Audit
- A08-020 - Replay Support
- A08-021 - Scientific Trace
- A08-022 - Scientific Tests
- A08-023 - Scientific Documentation
- A08-024 - ADR MAOI Scientific Population

## Risco Evitado

- populacao de MAOIs antes de validar o pipeline SSRI;
- criacao de conteudo sobre interacoes medicamentosas e alimentares sem corpus versionado;
- publicacao de washout, switching e restricoes de seguranca sem revisao editorial;
- falsa aprovacao cientifica de classe de alto risco;
- integracao prematura com Evidence Runtime, Safety Engine ou Clinical Operating Mind.

## Proxima Missao Autorizada

Permanece:

`MISSION A03-002 - SSRI Source Corpus Intake`

## Condicao para Desbloquear A08

O Program A08 so podera ser reaberto quando:

1. Program A03 tiver corpus, revisores e ao menos um piloto SSRI validado;
2. Programs A04, A05, A06 e A07 estiverem desbloqueados ou houver ADR justificando excecao metodologica;
3. o pipeline de populacao, validacao, auditoria e publicacao estiver aprovado para classes de alto risco;
4. houver criterios especificos para interacoes alimentares, washout, switching e safety constraints;
5. houver decisao CTO autorizando expansao para MAOIs.

## Declaracao Final

O Program A08 permanece bloqueado. A proxima execucao segura continua sendo A03-002.

