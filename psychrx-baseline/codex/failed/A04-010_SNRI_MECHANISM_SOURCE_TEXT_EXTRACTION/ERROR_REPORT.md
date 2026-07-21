# Error Report

## Data

2026-07-04

## Package

A04-010_SNRI_MECHANISM_SOURCE_TEXT_EXTRACTION

## Status

failed_governance_scope_mismatch

## Motivo

The inbox package requests:

```text
A04-010 - SNRI_MECHANISM_SOURCE_TEXT_EXTRACTION
```

However, the official repository state authorizes:

```text
A04-010 - SNRI_MECHANISM_DRAFT_EDITORIAL_REVIEW
```

The official state is defined by:

- `governance/execution/EXECUTION_STATE.json`
- `governance/execution/NEXT_MISSION.md`
- `governance/execution/NEXT_BLOCK.md`

The package attempts to advance directly to source-text extraction before the required editorial review mission recorded in the official state.

## Etapa Onde Falhou

State validation before execution.

## Arquivos Envolvidos

- `codex/failed/A04-010_SNRI_MECHANISM_SOURCE_TEXT_EXTRACTION/A04-010_SNRI_MECHANISM_SOURCE_TEXT_EXTRACTION.md`
- `governance/execution/EXECUTION_STATE.json`
- `governance/execution/NEXT_MISSION.md`
- `governance/execution/NEXT_BLOCK.md`

## Stacktrace

Not applicable. This was a governance validation failure, not a runtime exception.

## Recomendacao

Create a corrected inbox package for:

```text
A04-010 - SNRI_MECHANISM_DRAFT_EDITORIAL_REVIEW
```

The corrected package should review:

- the A04-009 draft structure;
- source-section traceability;
- unresolved claim status;
- readiness for a future source-text extraction mission.

Only after that review passes should a later mission authorize exact source-text extraction.

## Safety Confirmation

No scientific content was extracted.

No summaries, paraphrases or mechanism claims were created.

No clinical runtime, prescribing logic, diagnostic logic, recommendation logic, PK, PD, safety or evidence grading was modified.
