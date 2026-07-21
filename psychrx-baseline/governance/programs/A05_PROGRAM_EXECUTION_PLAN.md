# A05 Program Execution Plan

## Metadata

Project: PsychRx

Track: A - Scientific Knowledge Expansion

Program: A05 - Scientific Content Population: NDRIs

Status: authorized

Date: 2026-07-05

## Purpose

Create the official execution structure for Program A05 after completion of Program A04.

Program A05 governs scientific content population for NDRIs as internal, traceable, non-runtime scientific knowledge.

This document authorizes the program structure only. It does not create therapeutic recommendations, prescriptions, runtime eligibility, patient-facing guidance, or clinical decision logic.

## Class Scope

Drug class:

```text
NDRIs - Norepinephrine-Dopamine Reuptake Inhibitors
```

Initial expected portfolio:

```text
bupropion
```

The official portfolio must be confirmed by A05-002 before source discovery and population.

## Execution Mode

Program-level continuous execution is authorized for A05 once A05 is the active program in repository state.

The CTO/Codex agent may execute all A05 missions in order without requesting separate confirmation after each mission, provided every gate passes.

The agent must stop immediately on:

- failed tests;
- traceability gap;
- missing source material;
- invalid JSON;
- blocker;
- scope conflict;
- safety boundary violation;
- attempted runtime authorization.

## Permanent Restrictions

Throughout Program A05, the following remain prohibited:

- therapeutic recommendation;
- prescription;
- dose suggestion;
- medication selection for a patient;
- active clinical runtime use;
- runtime eligibility;
- patient-facing guidance;
- automated clinical decision logic;
- unsourced scientific claims.

## Program Sequence

### A05-001 - NDRI_PROGRAM_INITIALIZATION

Purpose:

Initialize Program A05 governance, scope, folders, manifests and execution reports.

Allowed:

- create A05 governance skeleton;
- create A05 documentation index;
- register program status;
- confirm non-runtime restrictions.

Forbidden:

- scientific claim population;
- runtime changes;
- recommendation or prescription.

Acceptance criteria:

- A05 is registered as active;
- A05 restrictions are documented;
- next mission is A05-002.

### A05-002 - NDRI_OFFICIAL_PORTFOLIO

Purpose:

Define the official NDRI drug portfolio for A05.

Allowed:

- identify candidate NDRI drugs;
- create official portfolio list;
- mark uncertain candidates as excluded or unresolved.

Forbidden:

- content extraction;
- mechanism/PK/PD/safety population;
- recommendations.

Acceptance criteria:

- official A05 NDRI portfolio exists;
- every included/excluded item has rationale;
- next mission is A05-003.

### A05-003 - NDRI_SOURCE_DISCOVERY

Purpose:

Discover authoritative scientific and regulatory sources for A05 NDRI content.

Allowed:

- source discovery;
- source metadata collection;
- source classification;
- locator registration.

Forbidden:

- claim population;
- paraphrase as content;
- runtime use.

Acceptance criteria:

- source discovery report exists;
- candidate sources are classified;
- next mission is A05-004.

### A05-004 - NDRI_SOURCE_CORPUS_INTAKE

Purpose:

Register the A05 source corpus as metadata-only or accessible source records.

Allowed:

- source intake;
- metadata normalization;
- locator storage;
- corpus manifest.

Forbidden:

- claim extraction;
- recommendation;
- prescription.

Acceptance criteria:

- source corpus manifest exists;
- sources are reviewable or have locators;
- next mission is A05-005.

### A05-005 - NDRI_SOURCE_VALIDATION

Purpose:

Validate source authority, accessibility, relevance and suitability for NDRI population.

Allowed:

- validation pipeline;
- source approval/rejection;
- gap report;
- blocker registration.

Forbidden:

- scientific claim creation;
- runtime authorization.

Acceptance criteria:

- validated source list exists;
- rejected sources are explained;
- next mission is A05-006.

### A05-006 - NDRI_POPULATION_EXECUTION_PLAN

Purpose:

Define field-by-field population sequence and gates for NDRI scientific content.

Allowed:

- population plan;
- field order;
- traceability policy;
- gate definitions.

Forbidden:

- actual scientific population;
- runtime use.

Acceptance criteria:

- A05 execution plan exists;
- first population field is authorized only after source-section selection;
- next mission is A05-007.

### A05-007 - NDRI_PROFILE_SHELLS

Purpose:

Create unresolved, non-runtime profile shells for each official NDRI drug.

Allowed:

- shell creation;
- unresolved markers;
- traceability placeholders.

Forbidden:

- populated claims without source text;
- runtime eligibility.

Acceptance criteria:

- every portfolio drug has a profile shell;
- all scientific fields are unresolved until sourced;
- next mission is A05-008.

### A05-008 - NDRI_FIELD_TRACEABILITY_MATRIX

Purpose:

Create a traceability matrix mapping sources, sections, drugs and fields.

Allowed:

- traceability matrix;
- field mapping;
- required source-section chain.

Forbidden:

- claim creation;
- unsourced population.

Acceptance criteria:

- matrix exists;
- each planned field has source requirements;
- next mission is A05-009.

### A05-009 - NDRI_EXTRACTION_GATES

Purpose:

Define gates that control when exact source-text extraction may start.

Allowed:

- extraction gate definitions;
- source-section readiness checks;
- blocker policy.

Forbidden:

- extraction before gate approval;
- population before extraction.

Acceptance criteria:

- extraction gate file exists;
- required chain is enforced;
- next mission is A05-010.

### A05-010 - NDRI_SOURCE_SECTION_SELECTION

Purpose:

Select specific source sections for the first authorized A05 field.

Allowed:

- source-section selection;
- locator verification;
- field-specific readiness.

Forbidden:

- extraction;
- paraphrase;
- inference;
- clinical use.

Acceptance criteria:

- selected source sections exist;
- selected sections are reviewable;
- next mission is A05-011.

### A05-011 - NDRI_SOURCE_TEXT_EXTRACTION

Purpose:

Extract exact source text from selected A05 source sections.

Allowed:

- exact source-text extraction;
- reviewable excerpt storage;
- source-section linkage.

Forbidden:

- summary;
- paraphrase;
- inference;
- claim population;
- recommendation;
- prescription;
- runtime use.

Acceptance criteria:

- exact source-text records exist;
- every record has traceability;
- next mission is A05-012.

### A05-012 - NDRI_CONTENT_POPULATION

Purpose:

Populate the first authorized NDRI scientific field only from A05-011 exact source-text records.

Allowed:

- controlled field population;
- unresolved markers where source text is insufficient;
- claim-to-source traceability.

Forbidden:

- unsourced inference;
- PK/PD/safety unless specifically authorized by field gate;
- recommendation;
- prescription;
- runtime use.

Acceptance criteria:

- populated field has source traceability;
- insufficient content remains UNRESOLVED;
- next mission is A05-013.

### A05-013 - NDRI_DRAFT_EDITORIAL_REVIEW

Purpose:

Review the A05 populated draft for editorial, scientific and traceability quality.

Allowed:

- review;
- correction requests;
- approval or blocker.

Forbidden:

- runtime eligibility;
- recommendation;
- prescription.

Acceptance criteria:

- review report exists;
- issues are resolved or registered;
- next mission is A05-014.

### A05-014 - NDRI_INTERNAL_PUBLICATION

Purpose:

Publish the reviewed A05 package as internal, non-runtime scientific knowledge.

Allowed:

- internal publication;
- publication manifest;
- status update.

Forbidden:

- runtime consumption;
- therapeutic recommendation;
- prescription.

Acceptance criteria:

- internal publication package exists;
- runtime status remains not eligible;
- next mission is A05-015.

### A05-015 - NDRI_TRACEABILITY_AUDIT

Purpose:

Audit traceability across source, section, extracted text, populated field and publication package.

Allowed:

- traceability audit;
- gap report;
- unresolved issue list.

Forbidden:

- new scientific claims.

Acceptance criteria:

- no claim lacks traceability;
- gaps are resolved or blocking;
- next mission is A05-016.

### A05-016 - NDRI_PROGRAM_COMPLETION_REPORT

Purpose:

Summarize Program A05 completion status, artifacts and restrictions.

Allowed:

- completion report;
- restriction summary;
- next-governance recommendation.

Forbidden:

- runtime authorization.

Acceptance criteria:

- completion report exists;
- restrictions are explicit;
- next mission is A05-017.

### A05-017 - A05_PROGRAM_GATE_VALIDATION

Purpose:

Validate the final Program A05 gate.

Program A05 can be marked complete only if A05-017 is accepted.

Gate must verify:

- A05-001 through A05-016 completed;
- tests passed;
- traceability preserved;
- JSON files valid;
- documentation updated;
- runtime remains prohibited unless a future gate explicitly changes it.

Acceptance criteria:

- A05 final gate report exists;
- Program A05 is either complete or blocked with explicit reason;
- next program remains unauthorized until a future governance update.

## Required State Updates Per Mission

After each accepted mission, update the relevant state files:

- `governance/execution/EXECUTION_STATE.json`
- `governance/execution/PROJECT_EXECUTION_CONTEXT.md`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/NEXT_MISSION.md`
- `governance/execution/NEXT_BLOCK.md`
- `governance/execution/PROJECT_PROGRESS.md`, if present
- `governance/execution/EXECUTION_LOG.md`, if present
- `governance/MASTER_ROADMAP.md`

## Declaration

Program A05 is now structurally defined and may be activated by governance state update.

A05 remains non-runtime, non-prescriptive and traceability-bound.