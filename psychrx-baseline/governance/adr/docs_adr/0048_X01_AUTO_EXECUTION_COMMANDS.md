# ADR 0048 - X01 Auto Execution Commands

## Status

Accepted.

## Date

2026-07-01

## Context

Program X01 created state-driven execution for PsychRx. After Program A03 reached Phase 3.5, the project needs a governed way to execute multiple missions in sequence without asking for each next prompt manually.

Manual execution remains safe but inefficient for long phases.

## Decision

Extend Program X01 with automatic execution commands:

```text
EXECUTE PHASE <PROGRAM_ID>-<PHASE_ID> AUTO
EXECUTE PROGRAM <PROGRAM_ID> AUTO
EXECUTE UNTIL BLOCK
```

These commands may continue across multiple missions only when:

- the gate is approved;
- dependencies are satisfied;
- the next mission is unambiguous;
- tests pass after every mission;
- control documents are updated after every mission;
- no safety, evidence or runtime boundary is violated.

## Mandatory Stop Conditions

Automatic execution must stop at:

- gate;
- blocker;
- failed test;
- failed JSON validation;
- dependency missing;
- ambiguous next mission;
- missing source traceability;
- clinical recommendation;
- prescription;
- runtime consumption attempt;
- ADR-required structural change.

## Impact

The next authorized mission remains:

```text
A03-036 - MECHANISM_CONTENT_EXTRACTION
```

Phase 4 can later be run with:

```text
EXECUTE PHASE A03-04 AUTO
```

## Declaration Final

Automatic execution is allowed only as governed sequence execution. It is not permission to bypass gates.
