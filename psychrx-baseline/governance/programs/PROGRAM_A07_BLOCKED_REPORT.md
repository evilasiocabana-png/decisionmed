# Program A07 Blocked Report - Scientific Content Population: TCAs

## Status

Bloqueado.

## Programa Solicitado

Track A - Scientific Knowledge Expansion

Program A07 - Scientific Content Population: TCAs

## Objetivo do Programa

Popular cientificamente a classe dos antidepressivos triciclicos:

- Amitriptyline;
- Nortriptyline;
- Clomipramine;
- Imipramine;
- Desipramine;
- Doxepin;
- Trimipramine.

## Dependencia Declarada no Proprio Programa

O Program A07 depende obrigatoriamente de:

- Track A - Program A06;
- Program 21 - Scientific Validation Framework;
- Program 22 - Knowledge Governance Platform.

## Estado Real das Dependencias

Program 21 e Program 22 estao concluidos.

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

O Program A07 nao pode ser executado agora.

Executar A07 antes de A03, A04, A05 e A06 violaria:

- ordem oficial de populacao;
- dependencias declaradas pelo proprio Program A07;
- Evidence Traceability Policy;
- Scientific Validation Framework;
- Knowledge Governance Platform;
- Publication Gate;
- ADR 0031 - A03 Scientific Content Population Gate;
- ADR 0032 - Block A04 Until A03 Validation;
- ADR 0033 - Block A05 Until A04 Validation;
- ADR 0034 - Block A06 Until A05 Validation;
- NEXT_MISSION atual.

## Missoes A07 Bloqueadas

- A07-001 - Amitriptyline Scientific Population
- A07-002 - Clomipramine Scientific Population
- A07-003 - Imipramine Scientific Population
- A07-004 - Nortriptyline Population
- A07-005 - Desipramine Population
- A07-006 - Doxepin & Trimipramine Population
- A07-007 - Transporter Mapping
- A07-008 - Receptor Affinity Matrix
- A07-009 - Metabolite Mapping
- A07-010 - Cardiac Safety Population
- A07-011 - Anticholinergic Profile
- A07-012 - Overdose Profile
- A07-013 - Knowledge Graph Integration
- A07-014 - Evidence Runtime Validation
- A07-015 - Semantic Validation
- A07-016 - Scientific Quality Review
- A07-017 - Coverage Analysis
- A07-018 - Consistency Analysis
- A07-019 - Scientific Audit
- A07-020 - Replay Support
- A07-021 - Scientific Trace
- A07-022 - Scientific Tests
- A07-023 - Scientific Documentation
- A07-024 - ADR TCA Scientific Population

## Risco Evitado

- populacao de TCAs antes de validar o pipeline SSRI;
- criacao de campos de seguranca cardiaca, toxicidade em overdose e carga anticolinergica sem corpus versionado;
- falsa aprovacao editorial;
- publicacao de conteudo farmacologico de alta complexidade sem trace por campo;
- integracao prematura com Evidence Runtime ou Clinical Operating Mind.

## Proxima Missao Autorizada

Permanece:

`MISSION A03-002 - SSRI Source Corpus Intake`

## Condicao para Desbloquear A07

O Program A07 so podera ser reaberto quando:

1. Program A03 tiver corpus, revisores e ao menos um piloto SSRI validado;
2. Programs A04, A05 e A06 estiverem desbloqueados ou houver ADR justificando excecao metodologica;
3. o pipeline de populacao, validacao, auditoria e publicacao estiver aprovado para classes complexas;
4. houver decisao CTO autorizando expansao para TCAs.

## Declaracao Final

O Program A07 permanece bloqueado. A proxima execucao segura continua sendo A03-002.

