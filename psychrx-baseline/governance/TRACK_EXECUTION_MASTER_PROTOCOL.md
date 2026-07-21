# Track Execution Master Protocol - PsychRx

## Purpose

This protocol defines how Codex must handle a track-level execution request in `codex/inbox`.

The founder should not need to provide internal file names, phase names, sprint identifiers or mission identifiers when the requested Track is clear.

## Command Meaning

When an inbox package says:

```text
Execute Track <ID>
```

Codex must interpret that as a complete track execution request.

## Required Execution Chain

```text
Track
-> Programs
-> Program Execution Plans
-> Codex execution
-> Gates
-> Tests
-> Governance update
```

## Required Behavior

Codex must:

1. Pull the latest repository state before reading inbox.
2. Read the current project state from governance files.
3. Identify the requested Track and all Programs belonging to that Track.
4. Read or create missing Program Execution Plans.
5. Execute Programs in order only when gates and dependencies allow.
6. Run tests and JSON validation after accepted gates.
7. Update governance after each accepted Program.
8. Continue automatically until the Track is complete.
9. Stop only on a real blocker.
10. Archive the inbox package with an execution report.

## Stop Conditions

Codex must stop immediately on:

- failed tests;
- failed gate;
- invalid project state;
- missing required source material;
- incomplete traceability;
- conflicting governance instruction;
- unsafe scope expansion;
- attempted clinical runtime enablement without authorization.

## Permanent Prohibitions

The following remain prohibited unless a future formal governance decision explicitly changes them:

- prescribing;
- therapeutic recommendation;
- dose suggestion;
- patient-specific medication selection;
- patient-facing clinical guidance;
- clinical runtime enablement for real clinical conduct;
- unsourced scientific claims;
- production deployment;
- patient data processing;
- regulatory compliance claim;
- certification claim;
- release authorization.

## Already Satisfied Track Requests

If an inbox package requests a Track that is already complete, Codex must:

1. verify the Track gate and Program Execution Plans;
2. validate tests;
3. archive the package as completed/already satisfied;
4. preserve the existing project state;
5. not re-execute completed Programs.

## Declaration

A clear track-level inbox request is a complete execution instruction. Codex must not ask the founder to provide internal mission names when the Track is clear.

