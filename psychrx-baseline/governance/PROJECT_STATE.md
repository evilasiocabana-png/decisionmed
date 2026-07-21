# Project State - PsychRx

## Purpose

This document is the primary entry point for answering:

```text
Where are we?
```

It is part of the PsychRx Project Operating System (PPOS).

It summarizes the current project state and points to the canonical roadmap instead of duplicating all roadmap content.

## Source Of Truth

Primary state document:

```text
governance/PROJECT_STATE.md
```

Machine-readable execution state:

```text
governance/execution/EXECUTION_STATE.json
```

Master roadmap:

```text
governance/MASTER_ROADMAP.md
```

Detailed next mission:

```text
governance/execution/NEXT_MISSION.md
```

Detailed next block:

```text
governance/execution/NEXT_BLOCK.md
```

## Historical Document Warning

Some older repository documents still mention previous blocker states, including:

```text
BLOCKED - A04_SOURCE_SECTION_SELECTION_REQUIRED
```

Those references are historical unless they appear in this file, `EXECUTION_STATE.json`, `NEXT_MISSION.md`, `NEXT_BLOCK.md`, or `MASTER_ROADMAP.md`.

Current state always prevails over historical status reports.

## Current Hierarchy

```text
Vision
-> Track
-> Program
-> Phase
-> Sprint
-> Mission
-> Task
```

## Operational Execution Chain

```text
Track
-> Program
-> Program Execution Plan
-> Codex
```

The Program Execution Library is available at:

```text
governance/programs/PROGRAM_EXECUTION_LIBRARY.md
governance/programs/PROGRAM_EXECUTION_LIBRARY_INDEX.json
```

The library is plan-only. It does not execute or complete any Program by itself.

## Current Position

Vision:

```text
Support clinical reasoning in psychopharmacology through structured, traceable and explainable knowledge governance without replacing the physician.
```

Track:

```text
Awaiting next governed inbox package
```

Program:

```text
AWAITING_NEXT_INBOX_PROGRAM
```

Phase:

```text
No Active Inbox Package
```

Sprint:

```text
Awaiting Governance Package
```

Current mission:

```text
AWAITING_NEXT_INBOX_PACKAGE
```

Mission status:

```text
blocked_waiting_for_next_inbox_package
```

## Last Completed Mission

Scientific lane:

```text
TRACK_E_COMPLETE_EXECUTION - E01 through E08
```

Governance lane:

```text
R03-002 - PROJECT_STATE_IMPLEMENTATION
```

## Next Mission

```text
AWAITING_NEXT_INBOX_PACKAGE
```

## Current Canonical Sequence

```text
A15 completed as an internal non-runtime mechanism package
-> Track B B01 through B08 completed as governance artifacts only
-> Track C C01 through C08 completed as product and UX governance artifacts only
-> Track D D01 through D08 completed as validation and certification governance artifacts only
-> Track E E01 through E08 completed as production readiness governance artifacts only
-> waiting for next governed inbox package
```

Next execution package:

```text
AWAITING_NEXT_INBOX_PACKAGE
```

## Active Restrictions

The following remain prohibited:

- summary of source text;
- paraphrase of source text;
- inference from source text;
- mechanism claim population outside A04-011 scope;
- pharmacokinetic extraction;
- pharmacodynamic extraction;
- safety extraction;
- evidence grading;
- therapeutic recommendation;
- prescription;
- clinical runtime use;
- runtime eligibility for draft knowledge.

## Resolved Historical Blocker

The previous blocker:

```text
A04_SOURCE_SECTION_SELECTION_REQUIRED
```

was resolved for the mechanism field by:

```text
A04-008G - SNRI_SOURCE_SECTION_SELECTION_EXECUTION
```

## Current Runtime Eligibility

```text
not_eligible
```

No SNRI knowledge package is eligible for clinical runtime.

## Program A04 Result

```text
completed_internal_non_runtime_mechanism_package
```

A04 completed a controlled SNRI mechanism package with traceability from selected source sections to source-text records, populated mechanism fields, editorial review, internal publication and traceability audit.

A15 has now been completed by the final gate `governance/programs/A15_PROGRAM_GATE_VALIDATION.md`.

Track B has now been completed as governance artifacts by `governance/tracks/TRACK_B_CLINICAL_RUNTIME_EVOLUTION/TRACK_B_GATE_VALIDATION.json`.

Track C has now been completed as product and UX governance artifacts by `governance/tracks/TRACK_C_CLINICAL_EXPERIENCE_PRODUCTIZATION/TRACK_C_GATE_VALIDATION.json`.

Track D has now been completed as validation and certification governance artifacts by `governance/tracks/TRACK_D_VALIDATION_CERTIFICATION/TRACK_D_GATE_VALIDATION.json`.

Track E has now been completed as production readiness governance artifacts by `governance/tracks/TRACK_E_PRODUCTION_READINESS/TRACK_E_GATE_VALIDATION.json`.

Program Execution Library has now been created as plan-only governance by `governance/programs/PROGRAM_EXECUTION_LIBRARY.md`.

## Track B State

```text
completed_governance_artifacts_only
```

Clinical runtime remains not enabled.

## Track C State

```text
completed_product_ux_governance_artifacts_only
```

Clinical UX implementation remains not enabled by this track.

## Track D State

```text
completed_validation_certification_governance_artifacts_only
```

Certification, regulatory compliance and release authorization remain not granted.

## Track E State

```text
completed_production_readiness_governance_artifacts_only
```

Production deployment, patient data processing, compliance certification and release authorization remain not granted.

## Completed Governance Operating System Missions

- R02 - Codex Mission Inbox Pipeline.
- R02.1 - Project Hierarchy Standardization.
- R02.2 - A04 Roadmap Reconciliation.
- R03-001 - PPOS Governance Simplification.
- R03-002 - Project State Implementation.
- R03-003 - Program-Centric Execution Model.

## How To Continue

Before executing anything, Codex must read:

1. `governance/PROJECT_STATE.md`
2. `governance/execution/EXECUTION_STATE.json`
3. `governance/execution/NEXT_MISSION.md`
4. `governance/execution/NEXT_BLOCK.md`
5. `governance/MASTER_ROADMAP.md`

Then it may execute only the next authorized mission or a governance inbox package that does not override the scientific lane.

## Last Source Text Extraction

```text
A04-010 - SNRI_MECHANISM_SOURCE_TEXT_EXTRACTION
```

created reviewable source-text records for the A04-008G selected mechanism sections.

No summary, paraphrase, inference, recommendation, prescription or runtime eligibility was created.

## Declaration

The project has completed Track E as production readiness governance artifacts only and is blocked only by absence of a new governed inbox package. Clinical runtime, prescription, recommendation and unsourced scientific content remain prohibited.
