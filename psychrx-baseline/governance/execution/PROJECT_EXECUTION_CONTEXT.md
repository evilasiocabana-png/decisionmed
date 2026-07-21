# Project Execution Context - PsychRx

## Purpose

This file is the portable execution context for PsychRx.

Any new chat, Codex run, CTO review or agent handoff must read this document before deciding what to execute next.

The repository, not chat memory, is the source of truth.

## Project

PsychRx.

## Architecture Version

v1.0-draft-enterprise.

## Baseline

Architecture and governance baseline established through Programs 00-26 and Track A foundations.

## Current Primary Execution Lane

Awaiting next governed inbox package or explicit Program execution command.

## Current Program

AWAITING_NEXT_INBOX_PROGRAM.

## Current Phase

No Active Inbox Package.

## Last Completed Program

PROGRAM A03 - Scientific Content Population: SSRIs.

## Last Completed Scientific Package

A03 internal draft SSRI knowledge package.

## Last Completed Governance Mission

R01-001 - ROADMAP_REFACTORING_TO_200_MISSION_MODEL.

R01-002 - ROADMAP_REFACTORING_REVIEW.

R01-003 - ROADMAP_MIGRATION_EXECUTION_PLAN.

R01-004 - ROADMAP_PIPELINE_IMPLEMENTATION.

## Last Completed Missions In Current Program

- A04-003 - SNRI_SOURCE_CORPUS_INTAKE_RECONCILIATION
- A04-004 - SNRI_POPULATION_EXECUTION_PLAN
- A04-005 - SNRI_PROFILE_SHELLS
- A04-006 - SNRI_SOURCE_ANCHOR_PLAN
- A04-007 - SNRI_FIELD_TRACEABILITY_MATRIX
- A04-008 - SNRI_EXTRACTION_GATES
- A04-008A - SNRI_SOURCE_ANCHOR_FINALIZATION
- A04-008B - SNRI_EXTRACTION_PROTOCOL_PACKAGE
- A04-008C - SNRI_SOURCE_SECTION_SELECTION_OR_BLOCKER
- A04-008D - SNRI_SOURCE_TEXT_ACQUISITION_PACKAGE
- A04-008E - SNRI_SOURCE_SECTION_LOCATOR_PLAN
- A04-008F - SNRI_SOURCE_SECTION_SELECTION_GATE
- A04-008G - SNRI_SOURCE_SECTION_SELECTION_EXECUTION
- A04-009 - SNRI_MECHANISM_POPULATION_DRAFT
- A04-010 - SNRI_MECHANISM_SOURCE_TEXT_EXTRACTION
- A04-011 - SNRI_MECHANISM_POPULATION
- A04-012 - SNRI_MECHANISM_DRAFT_EDITORIAL_REVIEW
- A04-013 - SNRI_MECHANISM_PUBLICATION
- A04-014 - SNRI_TRACEABILITY_AUDIT
- A04-015 - SNRI_PROGRAM_COMPLETION_REPORT
- A04-016 - A04_PROGRAM_GATE_VALIDATION

## Recent Paused Scientific Missions

- A04-001 - SNRI_PROGRAM_INITIALIZATION
- A04-002 - SNRI_OFFICIAL_PORTFOLIO
- A04.0-001 - SNRI_SOURCE_DISCOVERY
- A04.0-002 - SNRI_SOURCE_CATALOG
- A04.0-003 - SNRI_SOURCE_CORPUS_INTAKE
- A04.0-004 - SNRI_SOURCE_METADATA_NORMALIZATION

## Current Mission

AWAITING_NEXT_INBOX_PACKAGE.

## Last Completed Scientific Pipeline

PIPE-A04-0-SNRI-VALIDATION-001 - ValidationPipeline[DrugClass=SNRIs].

Historical alias: A04.0-005 - SNRI_SOURCE_VALIDATION.

## Last Completed Missions In Current Program

- A04.0-005 - SNRI_SOURCE_VALIDATION, completed as PIPE-A04-0-SNRI-VALIDATION-001
- A04.0-006 - SNRI_EDITORIAL_REGISTRATION
- A04.0-007 - SNRI_CORPUS_PUBLICATION
- A04.0-008 - PROGRAM_A04_0_COMPLETION_GATE

## Blocker

The previous A04 source-section blocker was resolved for the mechanism field by A04-008G.

A04-009 created unresolved, traceable, non-runtime mechanism draft slots and did not populate mechanism claims.

A04-010 created reviewable source-text records for all A04-008G selected mechanism sections.

A04-011 through A04-016 completed Program A04 as an internal non-runtime mechanism package.

R02.2 reconciled the A04 mechanism sequence:

```text
A04 complete
```

PK, PD, safety, evidence grading, recommendation, prescription and clinical runtime remain blocked.

## Next Authorized Action

AWAITING_NEXT_INBOX_PACKAGE.

No executable inbox package is present. Future Program execution must resolve through an official Program Execution Plan in `governance/programs/`.

Program Execution Library:

```text
governance/programs/PROGRAM_EXECUTION_LIBRARY.md
governance/programs/PROGRAM_EXECUTION_LIBRARY_INDEX.json
```

The mandatory traceability chain for mechanism section selection exists:

```text
Specific source
-> Specific section
-> Psychopharmacological field
-> Reviewable content
-> Reviewable source-text record
-> Unresolved mechanism draft slot
```

## Next Block

Read:

```text
governance/execution/NEXT_BLOCK.md
```

## Secondary Runtime Architecture Lane

Program 10 - Clinical Runtime has been extended by prompt bundles after its original baseline.

Current Program 10 architectural documentation state:

- Phase 1 reconciled with existing runtime.
- Phase 2 Clinical Workflow Runtime completed as structural read-only implementation.
- Phase 3 Clinical Context Runtime completed as architectural specification, Missions 254-274.

Important:

Mission 275 is not historical unless a future execution document explicitly creates it.

Before starting Program 10 Phase 4, consolidate Phase 3 into a single architecture document or create an explicit Phase 4 authorization.

## Dependencies Satisfied

- Program 00 - Governance
- Program 01 - Scientific Architecture
- Program 02 - Clinical Operating Mind
- Program 03 - Knowledge Graph
- Program 04 - Drug Intelligence
- Program 05 - Clinical Kernel
- Program 06 - Software Platform
- Program 07 - Clinical Workspace
- Program 08 - Clinical Kernel Integration
- Program 09 - Knowledge Population
- Program 10 - Clinical Runtime original baseline
- Program 11 - Safety Engine
- Program 12 - Evidence Runtime
- Program 13 - Therapeutic Optimization Engine
- Program 14 - Clinical Explanation Engine
- Program 15 - Clinical Snapshot Engine
- Program 16 - Clinical Timeline Engine
- Program 17 - Clinical Navigation Engine
- Program 18 - Clinical Operating Mind
- Program 19 - Clinical Quality and Error Reduction Engine
- Program 20 - Clinical Research Platform
- Program 21 - Scientific Validation Framework
- Program 22 - Knowledge Governance Platform
- Program X01 - Project Execution Protocol
- Program A01 - Official Scientific Knowledge Base
- Program A02 - Psychopharmacology Library Population
- Program A02.5 - SSRI Source Corpus Intake
- Program A03 - SSRI Scientific Content Population

## Documents To Read First

1. `governance/execution/PROJECT_EXECUTION_CONTEXT.md`
2. `governance/execution/NEXT_BLOCK.md`
3. `governance/execution/NEXT_MISSION.md`
4. `governance/execution/PROJECT_CURRENT_STATE.md`
5. `governance/execution/PROJECT_STATUS.md`
6. `governance/execution/PROJECT_PROGRESS.md`
7. `governance/roadmap/MASTER_DEVELOPMENT_PLAN.md`
8. relevant ADRs

## Relevant Current Reports

- `docs/PROGRAM_A03_COMPLETION_REPORT.md`
- `docs/PROGRAM_A04_BLOCKED_REPORT.md`
- `docs/PROGRAM_A04_0_SNRI_SCIENTIFIC_CORPUS.md`
- `docs/A04_001_002_PROGRAM_INITIALIZATION_AND_PORTFOLIO.md`
- `docs/A04_003_BLOCKED_SOURCE_CORPUS_REQUIRED.md`
- `docs/A04_0_001_SNRI_SOURCE_DISCOVERY.md`
- `docs/A04_0_001_EXECUTION_REPORT.md`
- `docs/A04_0_002_SNRI_SOURCE_CATALOG.md`
- `docs/A04_0_002_EXECUTION_REPORT.md`
- `docs/A04_0_003_SNRI_SOURCE_CORPUS_INTAKE.md`
- `docs/A04_0_003_EXECUTION_REPORT.md`
- `docs/A04_0_004_SNRI_SOURCE_METADATA_NORMALIZATION.md`
- `docs/A04_0_004_EXECUTION_REPORT.md`
- `docs/A04_0_005_SNRI_SOURCE_VALIDATION.md`
- `docs/A04_0_005_EXECUTION_REPORT.md`
- `docs/A04_0_006_SNRI_EDITORIAL_REGISTRATION.md`
- `docs/A04_0_006_EXECUTION_REPORT.md`
- `docs/A04_0_007_SNRI_CORPUS_PUBLICATION.md`
- `docs/A04_0_007_EXECUTION_REPORT.md`
- `docs/A04_0_008_PROGRAM_A04_0_COMPLETION_GATE.md`
- `docs/A04_0_008_EXECUTION_REPORT.md`
- `docs/PROGRAM_A04_0_COMPLETION_REPORT.md`
- `docs/A04_003_SNRI_SOURCE_CORPUS_INTAKE_RECONCILIATION.md`
- `docs/A04_003_EXECUTION_REPORT.md`
- `docs/A04_004_SNRI_POPULATION_EXECUTION_PLAN.md`
- `docs/A04_004_EXECUTION_REPORT.md`
- `docs/A04_005_SNRI_PROFILE_SHELLS.md`
- `docs/A04_005_EXECUTION_REPORT.md`
- `docs/A04_006_SNRI_SOURCE_ANCHOR_PLAN.md`
- `docs/A04_006_EXECUTION_REPORT.md`
- `docs/A04_007_SNRI_FIELD_TRACEABILITY_MATRIX.md`
- `docs/A04_007_EXECUTION_REPORT.md`
- `docs/A04_008_SNRI_EXTRACTION_GATES.md`
- `docs/A04_008_EXECUTION_REPORT.md`
- `docs/A04_008A_SNRI_SOURCE_ANCHOR_FINALIZATION.md`
- `docs/A04_008A_EXECUTION_REPORT.md`
- `docs/A04_008B_SNRI_EXTRACTION_PROTOCOL_PACKAGE.md`
- `docs/A04_008B_EXECUTION_REPORT.md`
- `docs/A04_008C_SNRI_SOURCE_SECTION_SELECTION_OR_BLOCKER.md`
- `docs/A04_008C_EXECUTION_REPORT.md`
- `docs/A04_008D_SNRI_SOURCE_TEXT_ACQUISITION_PACKAGE.md`
- `docs/A04_008D_EXECUTION_REPORT.md`
- `docs/A04_008E_SNRI_SOURCE_SECTION_LOCATOR_PLAN.md`
- `docs/A04_008E_EXECUTION_REPORT.md`
- `docs/A04_008F_SNRI_SOURCE_SECTION_SELECTION_GATE.md`
- `docs/A04_008F_EXECUTION_REPORT.md`
- `governance/execution/CODEX_EXECUTION_QUEUE.md`
- `governance/roadmap/PROGRAM_R01_ROADMAP_REFACTORING.md`
- `governance/roadmap/R01_EXECUTION_REPORT.md`
- `governance/roadmap/R01_200_MISSION_MODEL.md`
- `governance/roadmap/R01_PROGRAM_MAPPING.md`
- `governance/roadmap/R01_ROADMAP_REVIEW.md`
- `governance/roadmap/R01_GAP_ANALYSIS.md`
- `governance/roadmap/R01_EQUIVALENCE_MATRIX.md`
- `governance/roadmap/R01_FINAL_RECOMMENDATION.md`
- `governance/roadmap/R01_MIGRATION_EXECUTION_PLAN.md`
- `governance/roadmap/R01_MIGRATION_PHASES.md`
- `governance/roadmap/R01_PIPELINE_DEPLOYMENT_PLAN.md`
- `governance/roadmap/R01_DEPRECATION_PLAN.md`
- `governance/roadmap/R01_PROGRAM_CONVERSION_MATRIX.md`
- `governance/roadmap/R01_MIGRATION_CHECKLIST.md`
- `governance/roadmap/R01_MIGRATION_RISKS.md`
- `governance/roadmap/R01_EXECUTION_SEQUENCE.md`
- `governance/roadmap/R01_PIPELINE_IMPLEMENTATION.md`
- `governance/roadmap/R01_PIPELINE_EXECUTION_ID_POLICY.md`
- `governance/roadmap/R01_ACTIVE_ROADMAP_STATUS.md`
- `governance/roadmap/R01_004_EXECUTION_REPORT.md`
- `governance/programs/PROGRAM_10_PHASE_3_BASELINE.md`

## Permanent Prohibitions

- Do not prescribe.
- Do not recommend treatment.
- Do not make clinical decisions.
- Do not enable clinical runtime consumption of draft knowledge.
- Do not populate scientific fields without source corpus.
- Do not bypass Evidence Traceability Policy.
- Do not let interface decide clinical conduct.
- Do not rely on chat memory as project state.

## Mode

State-driven execution.

## Official Project State - Single Source of Truth

The official PsychRx state is never determined by conversation memory.

The official project state is determined exclusively by repository documents:

- `PROJECT_STATUS.md`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/PROJECT_PROGRESS.md`
- `governance/execution/NEXT_MISSION.md`
- `governance/execution/NEXT_BLOCK.md`
- `governance/execution/PROJECT_INDEX.md`
- `governance/execution/PROJECT_TREE.md`
- `governance/execution/PROJECT_EXECUTION_CONTEXT.md`
- `governance/execution/EXECUTION_LOG.md`
- `PROGRAM_STATUS.md`, when present
- `MISSION_STATUS.md`, when present

If there is any divergence between a conversation and official project documents, repository documentation always prevails.

## Session Start Protocol

At the start of any new chat, before producing execution guidance or changing files, the CTO/Codex agent must:

1. Read the official project state.
2. Identify active program, active phase, active sprint and active mission.
3. Verify dependencies, blockers, gates and related ADRs.
4. Determine the next unit of work from repository state.
5. Only then start execution.

Never start a mission from memory alone.

## Execution Protocol

PsychRx works in State Driven mode, never Conversation Driven mode.

Mandatory flow:

```text
VALIDATE STATE
↓
VALIDATE DEPENDENCIES
↓
VALIDATE GATES
↓
EXECUTE CURRENT MISSION
↓
RUN TESTS
↓
UPDATE STATUS
↓
UPDATE NEXT_MISSION
↓
CONTINUE WITH NEXT AUTHORIZED MISSION IN THE SAME PROGRAM
```

The former single-mission `STOP` rule is removed.

CTO/Codex agents are now authorized to execute a full active program continuously, from the current authorized mission through the program completion gate, provided every intermediate mission passes its acceptance criteria.

This continuous execution authorization applies inside the currently authorized program and also to the next complete program package present in `codex/inbox/` when predecessor dependencies are satisfied.

An inbox program package is sufficient operational authorization for complete program execution.

No separate human confirmation is required before executing a complete program package from `codex/inbox/`.

This rule does not bypass tests, dependency checks, gates, traceability, source sufficiency, JSON validity, editorial review, runtime restrictions or clinical safety prohibitions.

An agent must continue automatically to the next mission when all of the following are true:

1. the current mission is complete;
2. acceptance criteria are satisfied;
3. tests pass;
4. documentation is updated;
5. traceability is preserved;
6. no blocker exists;
7. the next mission is part of the same program, or the next complete program package is present in `codex/inbox/` and predecessor dependencies are satisfied.

An agent must stop immediately when any of the following occurs:

1. tests fail;
2. a blocker is detected;
3. traceability is incomplete;
4. source material is insufficient for the requested population;
5. a gate fails;
6. a mission would cross into a prohibited scope;
7. a mission would start a new program without a completed transition gate.

Never skip steps.

Never assume state from chat memory.

## Program-Level Continuous Execution Policy

When the founder asks to execute the current program, complete the current program, execute the remaining missions, or says `inbox`, the CTO/Codex agent is authorized to execute the next valid complete program package in `codex/inbox/` in order, without asking for separate confirmation before or after each mission.

For Program A04, this means the agent may execute:

```text
A04-011 - SNRI_MECHANISM_POPULATION
-> A04-012 - SNRI_MECHANISM_DRAFT_EDITORIAL_REVIEW
-> A04-013 - SNRI_MECHANISM_PUBLICATION
-> A04-014 - SNRI_TRACEABILITY_AUDIT
-> A04-015 - SNRI_PROGRAM_COMPLETION_REPORT
-> A04-016 - A04_PROGRAM_GATE_VALIDATION
```

A04 may be marked complete only after A04-016 is accepted.

A05 may start only after A04-016 passes and the official project state explicitly authorizes A05.

For future programs, the same continuous execution policy applies when a complete program package is present in `codex/inbox/` and predecessor dependencies pass.

## Gate Protocol

Every phase transition must have a gate.

Every gate must answer:

- Did the current phase finish?
- Were all acceptance criteria met?
- Did all tests pass?
- Are all JSON files valid?
- Was documentation updated?
- Is editorial approval present when required?

If any answer is no, the next phase remains blocked.

## Scientific Population Protocol

No scientific knowledge enters the Official Knowledge Base without following this sequence:

```text
Scientific Source
↓
Source Anchor
↓
Content Extraction
↓
Normalization
↓
Scientific Review
↓
Editorial Review
↓
Draft Knowledge Object
↓
Publication Candidate
↓
Published Knowledge Object
↓
Runtime Eligible (future)
```

Draft objects can never be used by Clinical Runtime.

## Safety Protocol

Even if scientific knowledge is complete, the following remain forbidden:

- automatic prescription;
- therapeutic recommendation;
- dose suggestion;
- medication selection;
- runtime clinical alert;
- Decision Engine;
- active Clinical Runtime;
- Therapeutic Optimization Engine for real clinical conduct.

These capabilities can only be released after formal architectural decision and governance document updates.

## Continuity Protocol

When the founder writes only:

```text
Proximo
```

the CTO/Codex agent must:

1. Read official project state.
2. Identify the active mission.
3. Validate blockers.
4. Execute the next authorized unit of work; if program-level execution is requested or already authorized, continue through the active program until its completion gate or blocker.
5. Never repeat completed missions.
6. Never alter architecture without authorization.
7. Never improvise roadmap.
8. Update project continuity documents.

## Final Declaration

PsychRx must continue from repository state, not from conversation memory.

PsychRx now supports continuous execution of the active authorized program, with strict gates, tests, traceability, and permanent clinical safety prohibitions preserved.
