# Phase Execution Rules - PsychRx

## Status

Official Program X01 rule document.

## Purpose

Define how Codex executes a phase within an authorized program.

## Command

```text
EXECUTE PHASE <PROGRAM_ID> <PHASE_ID>
EXECUTE PHASE <PROGRAM_ID>-<PHASE_ID> AUTO
```

## Required Checks

Before phase execution Codex must verify:

- program is active or authorized;
- previous phase baseline exists;
- phase scope is documented;
- phase missions are ordered;
- the next mission belongs to the requested phase;
- required ADRs exist;
- phase gate is known.

## Phase Execution Boundaries

Codex must not:

- execute missions outside the requested phase;
- merge phase responsibilities;
- create runtime behavior from documentary or scientific modeling phases;
- continue past a phase baseline gate without explicit authorization.

## Auto Phase Rule

When `AUTO` is present, Codex may execute the phase mission sequence without asking after each mission, but must stop at:

- phase baseline;
- blocker;
- dependency gap;
- failed validation;
- source traceability gap;
- safety or runtime boundary.

## Current Phase State

```text
Program: A03
Phase: Phase 3 - Drug Scientific Modeling
Completed: A03-021 through A03-030
Next: A03-036 - MECHANISM_CONTENT_EXTRACTION
Gate: Phase 3.5 completed; Phase 4 ready
```

## Final Declaration

Phase execution exists to keep scientific modeling incremental, auditable and bounded by gates.

