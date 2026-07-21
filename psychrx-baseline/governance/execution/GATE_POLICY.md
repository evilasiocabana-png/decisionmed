# Gate Policy - PsychRx

## Status

Official Program X01 gate policy.

## Purpose

Define when Codex must stop execution.

## Gate Types

### Dependency Gate

Stops execution when predecessor work is incomplete.

### ADR Gate

Stops execution when a structural decision is required.

### Scientific Gate

Stops execution when a mission would interpret, normalize or publish scientific content outside authorized scope.

### Safety Gate

Stops execution when a mission may create recommendation, prescription, runtime decision behavior or unsafe clinical output.

### Baseline Gate

Stops execution at the end of a program, phase or sprint for formal review.

### Validation Gate

Stops execution when tests, schema checks, structural checks or acceptance criteria fail.

## Mandatory Stop Conditions

Codex must stop when:

- dependencies are missing;
- the next mission is ambiguous;
- tests fail;
- an ADR is required;
- a document is frozen;
- a clinical recommendation appears;
- runtime consumption is attempted;
- publication gate is missing;
- scientific source traceability is absent.

## Current Known Gate

```text
A03-030 - PHASE_3_SPRINT_1_BASELINE
```

## Auto Execution Gate Rule

Automatic execution must stop at every baseline or gate unless the gate has already been approved and the next phase is explicitly marked ready in project controls.

## Final Declaration

Gates preserve the integrity of the PsychRx roadmap by preventing premature execution.
