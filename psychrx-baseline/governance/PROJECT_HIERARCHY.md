# Project Hierarchy - PsychRx

## Purpose

This document defines the official execution hierarchy for PsychRx.

It is a governance reference only. It does not define clinical content, scientific evidence, prescribing logic, clinical runtime behavior, or therapeutic recommendations.

## Canonical Hierarchy

PsychRx work must be organized using the following hierarchy:

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

For actual Codex execution, the simplified chain is:

```text
Track
-> Program
-> Program Execution Plan
-> Codex
```

The Program Execution Plan is not a replacement for Phase, Sprint, Mission and Task. It is the contract that maps a Program into those executable units so Codex does not need to ask how to execute the Program.

## Hierarchy Definitions

### Vision

The long-term purpose and non-negotiable direction of PsychRx.

The Vision explains why the project exists and what boundaries must never be violated.

Examples:

- preserve clinical safety;
- maintain scientific traceability;
- support clinical reasoning without replacing the physician;
- prohibit autonomous prescribing.

### Track

A major execution lane of the project.

Tracks group programs that share a strategic purpose.

Examples:

- Scientific Knowledge Expansion;
- Clinical Runtime Evolution;
- Clinical Experience Productization;
- Validation and Certification;
- Production Readiness.

### Program

A large coordinated body of work inside a Track.

A Program has a defined objective, dependency set, acceptance gate and completion criteria.

Program is the primary user-facing execution unit. The founder may approve or request execution at Program level without specifying internal missions or repository paths.

When a Program is approved, the CTO decomposes it into Phases, Sprints and Missions, and Codex executes only the authorized Missions and Tasks in sequence.

Every executable Program must have a Program Execution Plan before Codex changes project files.

Examples:

- Program A04 - Scientific Content Population: SNRIs;
- Program R02 - Codex Mission Inbox Pipeline;
- Program X01 - Project Execution Protocol.

### Program Execution Plan

The operational contract between a Program and Codex.

It defines:

- objective;
- scope;
- dependencies;
- gates;
- phases;
- sprints;
- missions;
- tasks;
- acceptance criteria;
- validation commands;
- allowed and prohibited artifact families;
- state-update requirements.

If a Program Execution Plan is missing, Codex must not improvise Program execution.

### Phase

A structured segment of a Program.

A Phase groups related sprints and must end with a clear gate or completion status.

Examples:

- Source Section Selection;
- Mechanism Draft Review;
- Corpus Publication;
- Runtime Baseline.

### Sprint

A small execution cycle within a Phase.

A Sprint groups one or more missions that should be executed together only when dependencies and gates allow it.

### Mission

The official executable unit of work.

Mission is the smallest governed executable unit. Program-level commands must resolve to the next authorized Mission before any file is changed.

Every Mission must have:

- identifier;
- objective;
- scope;
- allowed files or artifact types;
- prohibited actions;
- acceptance criteria;
- validation requirements;
- execution report.

### Task

An implementation or documentation step inside a Mission.

Tasks are not independently executed unless the Mission explicitly authorizes partial execution.

## Mission Traceability Rule

Every Mission must be traceable to:

```text
Track
-> Program
-> Phase
-> Sprint
-> Mission
```

If any part of that chain is missing, the Mission must be treated as incomplete for governance purposes until the missing context is recorded.

## Naming Rule

Mission identifiers must remain stable once committed.

Accepted examples:

- A04-010 - SNRI_MECHANISM_DRAFT_EDITORIAL_REVIEW
- R02.1 - PROJECT_HIERARCHY_STANDARDIZATION
- X01-001 - CODEX_EXECUTION_PROTOCOL

Do not reuse mission identifiers for different scopes.

Do not rename completed missions without an explicit governance record.

## State Resolution Rule

When determining what to execute next, Codex must read the official state documents before relying on inbox order:

1. `governance/execution/EXECUTION_STATE.json`
2. `governance/execution/PROJECT_EXECUTION_CONTEXT.md`
3. `governance/execution/NEXT_BLOCK.md`
4. `governance/execution/NEXT_MISSION.md`
5. `governance/execution/PROJECT_STATUS.md`

Inbox packages may define work to execute, but they do not override blockers, gates, or the official execution state.

## Program-Centric Execution Rule

When the user requests:

```text
EXECUTE PROGRAM <PROGRAM_ID>
NEXT PROGRAM
CONTINUE PROGRAM
```

Codex must treat Program as the planning unit and Mission as the execution unit.

The resolution chain is:

```text
Program
-> Phase
-> Sprint
-> Next authorized Mission
-> Tasks
```

Codex may not execute a Program by bypassing Missions, gates or dependencies.

## Scientific Governance Rule

Scientific population missions must also preserve the scientific chain:

```text
Scientific Source
-> Source Anchor
-> Source Section
-> Field
-> Reviewable Content
-> Draft Knowledge Object
-> Review
-> Publication Candidate
-> Published Knowledge Object
-> Runtime Eligible (future gate only)
```

Draft knowledge is never runtime-eligible by default.

## Clinical Safety Rule

No hierarchy level can authorize:

- autonomous diagnosis;
- therapeutic recommendation;
- prescription;
- dose selection;
- clinical runtime consumption of draft knowledge;
- interface-driven clinical conduct.

These capabilities require explicit future architectural decisions and safety gates.

## Declaration

This document is the canonical hierarchy reference for PsychRx execution governance. Future mission packages, execution reports and status files should reference this hierarchy when describing project state.
