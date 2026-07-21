# Program Execution Rules - PsychRx

## Status

Official Program X01 rule document.

## Purpose

Define how Codex executes a full program command safely.

Program is the primary user-facing execution unit. Mission remains the smallest governed executable unit.

## Command

```text
EXECUTE PROGRAM <PROGRAM_ID>
EXECUTE PROGRAM <PROGRAM_ID> AUTO
```

## Required Resolution

Codex must identify:

- requested program;
- program status;
- active phase;
- next authorized mission;
- completed missions;
- blocked missions;
- dependency chain;
- mandatory gates;
- ADRs governing the program.

Codex must resolve every Program command into the next state-approved mission or the next complete program package in `codex/inbox/` before changing files.

## Execution Limit

By default, Codex executes only one mission per cycle unless the user explicitly requests `EXECUTE UNTIL GATE`.

With `EXECUTE PROGRAM <PROGRAM_ID> AUTO`, Codex may continue beyond one mission only while the next mission remains inside the same program, dependencies are satisfied and validation passes.

With any auto command, Codex must stop when:

- a gate is reached;
- a test fails;
- a dependency is missing;
- an ADR is required;
- scientific interpretation exceeds mission scope;
- a safety, prescription or runtime boundary is touched.

## Program Blocking

A program is blocked when:

- its predecessor is incomplete;
- its required baseline is missing;
- its dependency graph is unresolved;
- its ADR is missing;
- its next mission is not listed in `NEXT_MISSION.md`;
- it conflicts with project governance.

## Current Program State

```text
Active program: Program A04 - Scientific Content Population: SNRIs
Completed predecessor: Program A04 - Scientific Content Population: SNRIs
Active program package: Program A07 - Scientific Content Population: TCAs
Next executable package: codex/inbox/A07_EXECUTE_FULL_PROGRAM.md
Auto candidate: EXECUTE NEXT INBOX PROGRAM PACKAGE
```

## Final Declaration

Program execution is always sequence-bound, dependency-bound and gate-bound.

