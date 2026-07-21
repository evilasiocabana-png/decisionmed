# ADR 0044 - Insert Program A02.5 SSRI Source Corpus Intake

## ID

0044

## Date

2026-06-30

## Status

Accepted.

## Context

Program A03 was previously defined as the scientific content population program for SSRIs.

During execution, Program A03 was blocked because it assumed the existence of an official, versioned and traceable SSRI source corpus.

The existing repository contains candidate source discovery and planning documents, but not a completed corpus intake and validation pipeline.

## Decision

Insert an intermediate program:

```text
PROGRAM A02.5 - SSRI Source Corpus Intake
```

This program sits between:

```text
Program A02 - Psychopharmacology Library Population
Program A03 - Scientific Content Population: SSRIs
```

Program A02.5 owns the source corpus intake workflow:

- source discovery;
- source corpus intake;
- metadata normalization;
- source validation;
- editorial registration;
- corpus publication.

## Numbering Decision

Program A02.5 is intentionally used instead of renumbering A03 through A15.

This preserves existing roadmap references and avoids cascading document churn.

## Mission Mapping

The previous navigation item:

```text
MISSION A03-002 - SSRI Source Corpus Intake
```

is reclassified as:

```text
MISSION A02.5-002 - SSRI Source Corpus Intake
```

The mission substance remains the same. Only its program ownership changes.

## Alternatives Considered

1. Keep source corpus intake inside Program A03.

Rejected. It keeps Program A03 overloaded and obscures the dependency between ingestion and population.

2. Renumber all subsequent programs.

Rejected. It would create unnecessary churn across A03 through A15.

3. Insert Program A02.5.

Accepted. It makes the missing ingestion layer explicit while preserving existing numbering.

## Impact

Program A03 remains blocked until Program A02.5 is complete.

Programs A04 through A15 remain blocked by their existing dependency chain.

NEXT_MISSION must point to:

```text
MISSION A02.5-002 - SSRI Source Corpus Intake
```

No SSRI content is populated by this ADR.

## Documents Affected

- `docs/PROGRAM_A02_5_SSRI_SOURCE_CORPUS_INTAKE.md`
- `docs/A02_5-001_SOURCE_DISCOVERY.md`
- `governance/execution/NEXT_MISSION.md`
- `governance/execution/PROJECT_TREE.md`
- `docs/PROJECT_DEPENDENCIES.md`
- `governance/execution/PROJECT_STATUS.md`
- `PROJECT_STATUS.md`
- `governance/execution/PROJECT_PROGRESS.md`
- `governance/execution/PROJECT_INDEX.md`

## Review Criteria

This ADR should be reviewed if:

- Program A02.5 completes corpus publication;
- Program A03 is unblocked;
- a future Track A governance document changes the scientific ingestion model;
- source corpus responsibilities move to a dedicated external repository.

## Declaration Final

Program A02.5 is now the official bridge between psychopharmacology metadata and SSRI scientific content population. It prevents Program A03 from beginning before the source corpus is official, versioned and traceable.
