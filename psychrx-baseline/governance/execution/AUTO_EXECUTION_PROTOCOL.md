# Auto Execution Protocol - PsychRx

## Status

Official extension of Program X01.

## Purpose

Allow Codex to execute a phase or program across multiple missions without repeated manual prompts, while preserving gates, tests, traceability and clinical safety.

## Commands

```text
EXECUTE PHASE <PROGRAM_ID>-<PHASE_ID> AUTO
EXECUTE PROGRAM <PROGRAM_ID> AUTO
EXECUTE UNTIL BLOCK
```

## Execution Loop

```text
Resolve current state
-> verify gate and dependencies
-> execute next mission
-> validate JSON when applicable
-> run tests
-> update control documents
-> resolve next mission
-> continue if allowed
-> stop at block or gate
```

## Required After Every Mission

- update `governance/execution/PROJECT_CURRENT_STATE.md`;
- update `governance/execution/NEXT_MISSION.md`;
- update other control documents only when status, dependencies, gates, artifacts or roadmap changed;
- record an execution report only for completed missions, new blockers, gates or baselines;
- run validation.

## Stop Conditions

Codex must stop immediately when:

- tests fail;
- JSON validation fails;
- next mission is ambiguous;
- dependency is missing;
- gate is reached;
- ADR is required;
- scientific source traceability is missing;
- clinical recommendation is introduced;
- prescription is introduced;
- runtime consumption is attempted;
- a document is frozen.

## Current Auto-Eligible State

```text
Program: A04
Completed predecessor: A04
Program: A05
Phase: Program Initialization
Next mission: A05-001 - NDRI_PROGRAM_INITIALIZATION
Gate status: A05 authorized
Auto command candidate: EXECUTE PROGRAM A05 AUTO
```

## Boundary

Auto execution does not allow:

- skipping mission numbers;
- creating clinical decisions;
- generating prescriptions;
- bypassing review;
- publishing unreviewed knowledge;
- consuming knowledge in runtime.

## Declaration Final

Auto execution is a disciplined loop, not a relaxation of governance.
