# ADR 0047 - A03 Phase 3.5 Scientific Knowledge Acquisition

## Status

Accepted.

## Date

2026-07-01

## Context

Program A03 completed Phase 3 Sprint 1 as structural scientific modeling. Phases 4 through 9 were requested, but execution was blocked because those phases require source-derived scientific content.

Without a shared acquisition layer, each future mission could interpret sources differently.

## Decision

Insert Phase 3.5 into Program A03:

```text
Phase 3.5 - Scientific Knowledge Acquisition
```

This phase governs how scientific source material moves into structured knowledge fields.

## Missions

```text
A03-031 - Extraction Protocol
A03-032 - Extraction Schema
A03-033 - Normalization Rules
A03-034 - Scientific Review Workflow
A03-035 - Extraction Baseline
```

## Boundary

Phase 3.5 creates process, schemas and governance only.

It does not populate:

- mechanism values;
- PK values;
- PD values;
- safety values;
- evidence grades;
- recommendations;
- prescriptions;
- runtime rules.

## Consequence

Phases 4 through 9 remain blocked until A03-035 is complete.

## Declaration Final

Phase 3.5 is the official Scientific Knowledge Acquisition layer for Program A03.
