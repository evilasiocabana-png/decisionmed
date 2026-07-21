# Project Blockers - PsychRx

## Date

2026-07-01

## Active Blockers

### A04-A15 Blocked

Programs A04 through A15 remain blocked by dependency chain.

Current dependency:

```text
A03 must complete and validate before A04 starts.
```

### Runtime Scientific Consumption Blocked

KnowledgeBase SSRI structures cannot be consumed by runtime yet.

Reason:

- scientific fields are structural or pending extraction;
- editorial review is incomplete;
- field-level validation is incomplete;
- publication gate has not approved runtime use.

### Clinical Recommendation Blocked

No recommendation generation is allowed.

Reason:

- Manifest;
- Clinical Constitution;
- Evidence Traceability Policy;
- ADR 0045;
- current mission scope.

### Prescribing Blocked

Automatic prescribing remains permanently prohibited.

## Process Blockers

### Manual Prompt-by-Prompt Execution

The current process depends too much on manual submission of prompts. This increases risk of:

- out-of-order execution;
- repeated mission fragments;
- stale `NEXT_MISSION`;
- inconsistent status updates.

### Documentation Scale

The repository now contains more than one thousand Markdown files. Navigation remains possible, but the cost of context recovery is rising.

## Historical Blockers

### A03 Initial Block

A03 was previously blocked until A02.5 created the SSRI Source Corpus. This is resolved.

### A03-025 Out-of-Order Block

A03-025 was received before A03-022 through A03-024 had been completed. This was resolved after missing missions were executed.

## Current Unblocked Path

```text
A03-026 - INDICATION_MODELING
```

## Blocker Recommendation

Implement a formal `EXECUTE PROGRAM` protocol before continuing many parallel or future programs.

