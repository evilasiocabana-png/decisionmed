# State Resolution Protocol - PsychRx

## Status

Official Program X01 state-resolution protocol.

## Purpose

Define how Codex determines the true current state before executing any command.

## Source Priority

When resolving state, Codex must inspect:

1. `governance/execution/NEXT_MISSION.md`
2. `governance/execution/PROJECT_STATUS.md`
3. `PROJECT_STATUS.md`
4. `governance/execution/PROJECT_PROGRESS.md`
5. `governance/execution/PROJECT_TREE.md`
6. `docs/PROJECT_DEPENDENCIES.md`
7. Program-specific status documents
8. ADRs
9. Execution reports

## Conflict Resolution

If documents disagree:

1. Do not execute.
2. Identify conflicting documents.
3. Prefer ADRs and explicit gate decisions.
4. Create or update a blocker report.
5. Ask for CTO decision when the conflict changes sequence, scope or safety.

## State Labels

Allowed labels:

- pending;
- active;
- completed;
- blocked;
- superseded;
- historical;
- gate;
- validation_required.

## Current Resolved State

```text
Program: A03
Phase: Phase 3 - Drug Scientific Modeling
Current authorized state: CTO_GATE_REVIEW - A03_PHASE_3_SPRINT_1_BASELINE_REVIEW
A03-021 through A03-030 have been completed as structural modeling and baseline.
```

## Final Declaration

State resolution is mandatory before execution. Codex must act from project state, not conversation memory alone.

