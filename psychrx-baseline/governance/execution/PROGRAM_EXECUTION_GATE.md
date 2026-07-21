# Program Execution Gate

## Objective

Define when program-level execution must stop.

## Gate Types

### Dependency Gate

Stop when a required previous mission, phase, program, ADR or validation artifact is missing.

### Safety Gate

Stop when a mission would create:

- prescription;
- recommendation;
- clinical decision;
- safety claim without source;
- runtime consumption before publication.

### Evidence Gate

Stop when a scientific field requires source extraction, evidence classification or editorial review not authorized by the current mission.

### Baseline Gate

Stop at baseline missions such as:

```text
PHASE BASELINE
PROGRAM BASELINE
PUBLICATION GATE
```

### Validation Gate

Stop if:

- tests fail;
- JSON is invalid;
- control documents conflict;
- mission output contradicts governance.

### Human Decision Gate

Stop when the next step requires CTO choice.

## Current Known Gate

Program A03 should stop at:

```text
A03-030 - PHASE_3_SPRINT_1_BASELINE
```

for review before continuing deeper scientific content population.

## Declaration Final

The Program Execution Gate prevents autonomous drift across scientific, clinical and governance boundaries.
