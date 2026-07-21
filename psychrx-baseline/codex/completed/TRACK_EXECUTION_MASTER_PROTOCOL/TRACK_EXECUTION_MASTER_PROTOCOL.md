# Codex Mission - Track Execution Master Protocol

## Purpose

This file defines how a track-level request must be handled when the founder asks to execute a full track from GitHub/Codex inbox.

The founder must not be required to guess program names, file names, phases, sprints or mission identifiers.

When a track execution request is placed in `codex/inbox`, the Codex executor must open the file and complete the requested track end-to-end according to repository governance.

## Required Behavior

When the requested track is identified, Codex must:

1. Read the current project state from governance files.
2. Identify the requested track and all programs belonging to that track.
3. Create any missing `PROGRAM_EXECUTION_PLAN.md` documents.
4. Create missing phases, sprints, missions, gates and acceptance criteria.
5. Execute each program in order.
6. Run available tests after each accepted program or gate.
7. Update project state and roadmap after each accepted program.
8. Continue automatically until the entire requested track is complete.
9. Stop only on a real blocker.
10. Produce a final report.

## Stop Conditions

Stop immediately only if one of these occurs:

- failed tests;
- failed gate;
- invalid project state;
- missing required source material;
- incomplete traceability;
- conflicting governance instruction;
- unsafe scope expansion;
- attempted clinical runtime enablement without authorization.

## Permanent Prohibitions

The following are always prohibited unless a later formal governance decision explicitly changes them:

- prescribing;
- therapeutic recommendation;
- dose suggestion;
- patient-specific medication selection;
- patient-facing clinical guidance;
- clinical runtime enablement for real clinical conduct;
- unsourced scientific claims.

## Track-Level Command Contract

If an inbox file says:

```text
Execute Track B
```

Codex must understand this as:

```text
Create missing program execution plans for Track B.
Execute B01 through B08 in order.
Update governance after each program.
Run tests and validate gates.
Stop only on blocker.
```

If an inbox file says:

```text
Execute Track C
```

Codex must apply the same pattern to all Track C programs.

The same applies to Tracks D and E.

## Required Final Output

At completion, Codex must report:

1. track executed;
2. programs executed;
3. files created;
4. files modified;
5. tests run;
6. test results;
7. gates passed;
8. blockers, if any;
9. final project state;
10. next authorized action.

## Declaration

A track-level inbox request is a complete execution instruction, not merely a planning note.

Codex must not ask the founder to provide internal file names or mission names when the requested track is clear.
