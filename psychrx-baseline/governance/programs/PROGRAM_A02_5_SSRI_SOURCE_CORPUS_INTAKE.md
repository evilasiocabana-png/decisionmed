# Program A02.5 - SSRI Source Corpus Intake

## Status

Inserted as an intermediate scientific ingestion program.

## Objective

Build the primary scientific source corpus for SSRIs before any scientific field population in Program A03.

This program does not populate medications.

It organizes, normalizes and validates scientific sources so that the Scientific Validation Framework and Knowledge Governance Platform can safely receive future SSRI content.

## Rationale

Program A03 assumes that an official, versioned, traceable source corpus already exists.

During execution, that assumption was found to be false. Therefore, Program A02.5 is inserted between:

```text
Program A02 - Psychopharmacology Library Population
Program A03 - Scientific Content Population: SSRIs
```

This preserves the existing numbering of Programs A03 through A15 while making the missing dependency explicit.

## Scope

Program A02.5 covers:

- source discovery;
- source corpus intake;
- metadata normalization;
- source validation;
- editorial registration;
- corpus publication readiness.

## Out of Scope

Program A02.5 must not:

- populate SSRI medication fields;
- extract therapeutic claims into the Knowledge Layer;
- create dosing guidance;
- create clinical recommendations;
- publish evidence as validated content;
- connect content to runtime engines;
- produce prescription-oriented output.

## Official Sequence

```text
A01 - Official Scientific Knowledge Base
A02 - Psychopharmacology Library Population
A02.5 - SSRI Source Corpus Intake
A03 - Scientific Content Population: SSRIs
A04 - Scientific Content Population: SNRIs
A05 - Scientific Content Population: NDRIs
A06 - Scientific Content Population: NaSSAs
A07 - Scientific Content Population: TCAs
A08 - Scientific Content Population: MAOIs
A09 - Scientific Content Population: Atypical Antidepressants
A10 - First-Generation Antipsychotics
A11 - Second-Generation Antipsychotics
A12 - Mood Stabilizers
A13 - Anxiolytics & Hypnotics
A14 - ADHD Medications
A15 - Cognitive Enhancers & Dementia-Related Psychopharmacology
```

## Missions

### Mission A02.5-001 - Source Discovery

Identify candidate source families for the SSRI corpus.

Status: completed as candidate discovery only, based on the existing A03 Source Acquisition Matrix.

### Mission A02.5-002 - Source Corpus Intake

Register the official SSRI source corpus with identifiers, bibliographic metadata, access status, source type and versioning metadata.

Status: completed as raw source corpus intake.

### Mission A02.5-003 - Metadata Normalization

Normalize DOI, PMID, ISBN, guideline identifiers, regulatory identifiers, publication year, source type and access metadata.

Status: completed as administrative metadata normalization.

### Mission A02.5-004 - Source Validation

Validate that each source can support future field-level extraction.

Status: completed as structural source validation.

### Mission A02.5-005 - Editorial Registration

Assign editorial review metadata and reviewer responsibility for the SSRI corpus.

Status: completed as administrative editorial registration.

### Mission A02.5-006 - Corpus Publication

Publish the corpus as a controlled scientific input for Program A03.

Status: completed as controlled corpus publication.

### Mission A02.5-007 - Program Completion Report

Consolidate Program A02.5 completion and determine whether the A03 gate may move from blocked to next authorized.

Status: completed.

## Relationship With Existing A03 Documents

The existing A03 planning documents remain valid, but their intake responsibilities are now governed by Program A02.5.

The following documents become inputs to A02.5:

- `docs/A03_SOURCE_ACQUISITION_MATRIX.md`;
- `docs/A03_FIELD_LEVEL_TRACEABILITY_TEMPLATE.md`;
- `docs/A03_EDITORIAL_REVIEW_GATE.md`;
- `docs/PROGRAM_A03_BLOCKED_REPORT.md`.

## Current Next Authorized Mission

```text
MISSION A03-011 - Drug Portfolio Definition
```

The previous navigation label:

```text
MISSION A03-002 - SSRI Source Corpus Intake
```

was executed under Program A02.5 as raw source corpus intake. Metadata normalization, source validation, editorial registration, controlled corpus publication and completion reporting are complete. Program A03 Phase 1 structural foundation is complete, and A03-011 is now authorized.

## Acceptance Criteria

Program A02.5 will be considered complete when:

- SSRI source corpus exists;
- official source catalog is registered;
- source metadata are normalized;
- DOI, PMID, ISBN or equivalent identifiers are recorded where applicable;
- source versions are recorded;
- traceability exists per source document;
- editorial registration exists;
- corpus is ready for Program A03 scientific population;
- no medication field is populated before Program A03 is explicitly unblocked.

## Declaration Final

Program A02.5 makes the missing scientific ingestion layer explicit. It protects Program A03 from beginning content population before the SSRI source corpus is official, versioned and traceable.
