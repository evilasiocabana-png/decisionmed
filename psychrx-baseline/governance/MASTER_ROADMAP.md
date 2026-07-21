# Master Roadmap - PsychRx

## Purpose

This document is the master roadmap for the PsychRx Project Operating System.

It consolidates the active execution hierarchy and indexes current roadmap items without replacing historical governance documents.

This is an organizational document only. It does not define clinical runtime behavior, scientific claims, therapeutic recommendations, prescribing logic, diagnostic logic, or patient-facing guidance.

## Canonical Hierarchy

PsychRx execution follows the hierarchy defined in `governance/PROJECT_HIERARCHY.md`:

```text
Vision
-> Track
-> Program
-> Phase
-> Sprint
-> Mission
-> Task
```

## Vision

PsychRx exists to support clinical reasoning in psychopharmacology through structured, traceable and explainable knowledge governance.

PsychRx does not replace the physician, does not prescribe autonomously and does not consume draft scientific knowledge in clinical runtime.

## Active State Summary

Current primary execution lane:

```text
Track A - Scientific Knowledge Expansion
No active program
Phase - No Active Inbox Package
Sprint - Awaiting Governance Package
Mission - AWAITING_NEXT_INBOX_PACKAGE
```

Historical note:

Older documents may still mention `BLOCKED - A04_SOURCE_SECTION_SELECTION_REQUIRED`. That blocker is historical for the mechanism field and was resolved by A04-008G.

A15-017 has passed. Program A15 is complete as an internal non-runtime mechanism package.

Track B B01 through B08 have also been completed as governance artifacts only.

Track C C01 through C08 have been completed as product and UX governance artifacts only.

Track D D01 through D08 have been completed as validation and certification governance artifacts only.

Track E E01 through E08 have been completed as production readiness governance artifacts only.

No further inbox package is currently present.

The next mission is controlled by:

- `governance/execution/EXECUTION_STATE.json`
- `governance/execution/NEXT_MISSION.md`
- `governance/execution/NEXT_BLOCK.md`

## Program Execution Library

The official Program Execution Library is available at:

```text
governance/programs/PROGRAM_EXECUTION_LIBRARY.md
governance/programs/PROGRAM_EXECUTION_LIBRARY_INDEX.json
```

Programs must resolve through:

```text
Track
-> Program
-> Program Execution Plan
-> Codex
```

The library is plan-only. Its existence does not execute or complete any Program.

## Canonical A04 Mechanism Sequence

```text
A04 complete
```

Full A04 completion sequence:

```text
governance/programs/A04_PROGRAM_COMPLETION_EXECUTION_PLAN.md
```

Restrictions that remain active:

- no PK extraction;
- no PD extraction;
- no safety extraction;
- no evidence grading;
- no therapeutic recommendation;
- no prescription;
- no clinical runtime consumption.

## Track Index

### Track A - Scientific Knowledge Expansion

Purpose:

Build controlled scientific knowledge packages with traceability, review and publication gates.

Current active program:

- Awaiting the next governed inbox package.

Completed or baselined programs:

- Program A01 - Official Scientific Knowledge Base.
- Program A02 - Psychopharmacology Library Population.
- Program A02.5 - SSRI Source Corpus Intake.
- Program A03 - Scientific Content Population: SSRIs.
- Program A04.0 - SNRI Scientific Corpus.
- Program A04 - Scientific Content Population: SNRIs.

Blocked future programs:

- Program A06 - Scientific Content Population: NaSSAs.
- Program A07 - Scientific Content Population: TCAs.
- Program A08 - Scientific Content Population: MAOIs.
- Program A09 - Scientific Content Population: Atypical Antidepressants.
- Program A10 - Scientific Content Population: First-Generation Antipsychotics.
- Program A11 - Scientific Content Population: Second-Generation Antipsychotics.
- Program A12 - Scientific Content Population: Mood Stabilizers.
- Program A13 - Scientific Content Population: Anxiolytics and Hypnotics.
- Program A14 - Scientific Content Population: ADHD Medications.
- Program A15 - Scientific Content Population: Cognitive Enhancers and Dementia-Related Psychopharmacology.

### Track B - Clinical Runtime Evolution

Purpose:

Define and validate structural runtime capabilities only after knowledge governance gates allow them.

Status:

Completed as governance artifacts B01 through B08. Not active for clinical conduct. Runtime clinical consumption remains prohibited for draft knowledge.

### Track C - Clinical Experience Productization

Purpose:

Develop the clinician-facing experience while keeping clinical decisions with the physician.

Status:

Completed as product and UX governance artifacts C01 through C08. Clinical Workspace baseline exists in read-only form. Functional UX implementation requires a future governed package.

### Track D - Validation and Certification

Purpose:

Validate governance, scientific traceability, safety boundaries and certification readiness.

Status:

Completed as validation and certification governance artifacts D01 through D08. No certification, regulatory compliance or release authorization is granted.

### Track E - Production Readiness

Purpose:

Prepare deployment, operations, monitoring and compliance.

Status:

Completed as production readiness governance artifacts E01 through E08. No deployment, compliance claim or production release is authorized.

## Program Index

### Foundation and Platform Programs

| Program | Status | Notes |
| --- | --- | --- |
| Program 00 - Governance | Completed | Foundational governance baseline. |
| Program 01 - Scientific Architecture | Completed/Baselined | Scientific architecture baseline. |
| Program 02 - Clinical Operating Mind | Completed/Baselined | Conceptual reasoning architecture. |
| Program 03 - Knowledge Graph | Completed/Baselined | Conceptual knowledge graph. |
| Program 04 - Drug Intelligence | Partial | Early conceptual baseline. |
| Program 05 - Clinical Kernel | Partial | Structural planning only. |
| Program 06 - Software Platform | Completed/Baselined | Read-only localhost baseline. |
| Program 07 - Clinical Workspace | Completed/Baselined | Read-only clinical workspace baseline. |
| Program 08 - Clinical Kernel Integration | Completed/Baselined | Structural read-only integration. |
| Program 09 - Knowledge Population | Completed/Baselined | Knowledge population baseline. |
| Program 10 - Clinical Runtime | Completed/Baselined | Structural read-only runtime baseline. |
| Program 11 - Safety Engine | Completed/Baselined | Structural read-only safety baseline. |
| Program 12 - Evidence Runtime | Completed/Baselined | Structural read-only evidence baseline. |
| Program 13 - Therapeutic Optimization Engine | Completed/Baselined | Structural read-only baseline; no real recommendation. |
| Program 14 - Clinical Explanation Engine | Completed/Baselined | Structural read-only explanation baseline. |
| Program 15 - Clinical Snapshot Engine | Completed/Baselined | Structural read-only snapshot baseline. |
| Program 16 - Clinical Timeline Engine | Completed/Baselined | Structural read-only timeline baseline. |
| Program 17 - Clinical Navigation Engine | Completed/Baselined | Structural read-only navigation baseline. |
| Program 18 - Clinical Operating Mind | Completed/Baselined | Structural read-only baseline. |
| Program 19 - Clinical Quality and Error Reduction Engine | Completed/Baselined | Structural read-only baseline. |
| Program 20 - Clinical Research Platform | Completed/Baselined | Structural read-only baseline. |
| Program 21 - Scientific Validation Framework | Completed/Baselined | Scientific governance baseline. |
| Program 22 - Knowledge Governance Platform | Completed/Baselined | Knowledge governance baseline. |
| Program 23 - Digital Clinical Twin Platform | Completed/Baselined | Strategic architecture baseline only. |
| Program 24 - Clinical Simulation Platform | Completed/Baselined | Strategic architecture baseline only. |
| Program 25 - Clinical Intelligence Platform | Completed/Baselined | Strategic architecture baseline only. |
| Program 26 - PsychRx Platform Maturity and Certification | Completed/Baselined | Transition gate planning. |

### Operating System Programs

| Program | Status | Notes |
| --- | --- | --- |
| Program X01 - Project Execution Protocol | Completed | State-driven execution protocol. |
| Program R01 - Roadmap Refactoring | Completed | Pipeline model active. |
| Mission R02 - Codex Mission Inbox Pipeline | Completed | Inbox/processing/completed/failed workflow. |
| Mission R02.1 - Project Hierarchy Standardization | Completed | Canonical hierarchy created. |
| Mission R02.2 - A04 Roadmap Reconciliation | Completed | A04 sequence reconciled. |
| Mission R03-001 - PPOS Governance Simplification | Completed | Created this master roadmap. |
| Mission R03-002 - Project State Implementation | Completed | Created the project state entry point. |
| Mission R03-003 - Program-Centric Execution Model | Completed | Defines Program as the primary user-facing execution unit. |

### Scientific Knowledge Programs

| Program | Status | Notes |
| --- | --- | --- |
| A01 - Official Scientific Knowledge Base | Completed | Scientific knowledge base baseline. |
| A02 - Psychopharmacology Library Population | Completed | Metadata-only baseline. |
| A02.5 - SSRI Source Corpus Intake | Completed | SSRI corpus intake and publication. |
| A03 - Scientific Content Population: SSRIs | Completed as internal draft | Runtime remains prohibited. |
| A04.0 - SNRI Scientific Corpus | Completed | SNRI corpus exists. |
| A04 - Scientific Content Population: SNRIs | Completed | Internal non-runtime mechanism package complete. Gate: `governance/programs/A04_PROGRAM_GATE_VALIDATION.md`. |
| A05 - Scientific Content Population: NDRIs | Completed | Internal non-runtime mechanism package complete. Gate: `governance/programs/A05_PROGRAM_GATE_VALIDATION.md`. |
| A06 - Scientific Content Population: NaSSAs | Completed | Internal non-runtime mechanism package complete. Gate: `governance/programs/A06_PROGRAM_GATE_VALIDATION.md`. |
| A07 - Scientific Content Population: TCAs | Completed | Internal non-runtime mechanism package complete. Gate: `governance/programs/A07_PROGRAM_GATE_VALIDATION.md`. |
| A08 - Scientific Content Population: MAOIs | Completed | Internal non-runtime mechanism package complete. Gate: `governance/programs/A08_PROGRAM_GATE_VALIDATION.md`. |
| A09 - Scientific Content Population: Atypical Antidepressants | Completed | Internal non-runtime mechanism package complete. Gate: `governance/programs/A09_PROGRAM_GATE_VALIDATION.md`. |
| A10 - Scientific Content Population: First-Generation Antipsychotics | Completed | Internal non-runtime mechanism package complete. Gate: `governance/programs/A10_PROGRAM_GATE_VALIDATION.md`. |
| A11 - Scientific Content Population: Second-Generation Antipsychotics | Completed | Internal non-runtime mechanism package complete. Gate: `governance/programs/A11_PROGRAM_GATE_VALIDATION.md`. |
| A12 - Scientific Content Population: Mood Stabilizers | Completed | Internal non-runtime mechanism package complete. Gate: `governance/programs/A12_PROGRAM_GATE_VALIDATION.md`. |
| A13 - Scientific Content Population: Anxiolytics and Hypnotics | Completed | Internal non-runtime mechanism package complete. Gate: `governance/programs/A13_PROGRAM_GATE_VALIDATION.md`. |
| A14 - Scientific Content Population: ADHD Medications | Completed | Internal non-runtime mechanism package complete. Gate: `governance/programs/A14_PROGRAM_GATE_VALIDATION.md`. |
| A15 - Scientific Content Population: Cognitive Enhancers and Dementia-Related Psychopharmacology | Completed | Internal non-runtime mechanism package complete. Gate: `governance/programs/A15_PROGRAM_GATE_VALIDATION.md`. |
| Track B - Clinical Runtime Evolution | Completed as governance artifacts | B01-B08 executed; clinical runtime remains prohibited. |
| Track C - Clinical Experience Productization | Completed as product and UX governance artifacts | C01-C08 executed; UI conduct logic and clinical runtime remain prohibited. |
| Track D - Validation and Certification | Completed as validation and certification governance artifacts | D01-D08 executed; certification, compliance and release authorization are not granted. |
| Track E - Production Readiness | Completed as production readiness governance artifacts | E01-E08 executed; deployment, patient data processing, compliance and release authorization are not granted. |

## Active Mission Index

```text
Track: Scientific Knowledge Expansion
Program: AWAITING_NEXT_INBOX_PROGRAM
Phase: No Active Inbox Package
Sprint: Awaiting Governance Package
Mission: AWAITING_NEXT_INBOX_PACKAGE
Task: wait for a governed inbox package
```

## Mission Execution Rule

Any mission package in `codex/inbox/` must be validated against the official state before execution.

Inbox order does not override:

- active blockers;
- active gates;
- `EXECUTION_STATE.json`;
- `NEXT_MISSION.md`;
- `NEXT_BLOCK.md`;
- safety prohibitions.

## Preservation Rule

This master roadmap does not delete, replace or invalidate historical governance files.

Historical detail remains in:

- `governance/execution/`
- `governance/roadmap/`
- `governance/programs/`
- `governance/missions/`
- `docs/`

## Declaration

`governance/MASTER_ROADMAP.md` is the high-level roadmap entry point for PsychRx. It simplifies navigation while preserving the existing governance system and the state-driven execution model.
