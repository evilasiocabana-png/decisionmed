# Codex Mission - Execute Full Program A09

## Target Program

A09 - Scientific Content Population: Atypical Antidepressants.

## Mission

Create and execute the complete Program A09 sequentially from initialization through final program gate.

## Program Structure

```text
TRACK A
└── PROGRAM A09 - Scientific Content Population: Atypical Antidepressants

Phase 1 - Program Initialization
  A09-001 - Program Initialization
  A09-002 - Official Portfolio

Phase 2 - Scientific Source Governance
  A09-003 - Source Discovery
  A09-004 - Source Corpus Intake
  A09-005 - Source Validation

Phase 3 - Population Preparation
  A09-006 - Population Execution Plan
  A09-007 - Profile Shells
  A09-008 - Field Traceability Matrix
  A09-009 - Extraction Gates
  A09-010 - Source Section Selection

Phase 4 - Scientific Population
  A09-011 - Source Text Extraction
  A09-012 - Content Population

Phase 5 - Review and Publication
  A09-013 - Draft Editorial Review
  A09-014 - Internal Publication
  A09-015 - Traceability Audit
  A09-016 - Program Completion Report
  A09-017 - Program Gate Validation
```

## Scope

Drug class:

- Atypical antidepressants.

Initial expected portfolio:

- trazodone.

The official portfolio must be confirmed by A09-002 before source discovery and population.

## Execution Rules

Execute A09 in the same controlled pattern used for A05-A08.

Create the A09 governance structure if needed, then execute all A09 missions in order.

Stop only on:

- failed tests;
- invalid JSON;
- missing traceability;
- missing source material;
- scope conflict;
- failed gate;
- attempted runtime authorization;
- attempted prescription, recommendation, dose suggestion or patient-specific clinical guidance.

## Permanent Restrictions

Do not enable:

- clinical runtime consumption;
- therapeutic recommendation;
- prescription;
- dose suggestion;
- patient-specific medication selection;
- patient-facing clinical guidance;
- unsourced scientific claims.

## Required Reading

- `governance/execution/PROJECT_EXECUTION_CONTEXT.md`
- `governance/execution/NEXT_BLOCK.md`
- `governance/execution/NEXT_MISSION.md`
- `governance/MASTER_ROADMAP.md`

## Validation

Run:

```text
python -m unittest discover -s tests -t .
```

## Final Report

Report:

1. missions executed;
2. files created;
3. files modified;
4. tests run and results;
5. blockers, if any;
6. traceability status;
7. final A09 gate status;
8. next authorized action.
