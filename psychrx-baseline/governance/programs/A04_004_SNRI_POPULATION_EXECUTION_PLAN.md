# A04-004 - SNRI Population Execution Plan

## Program

PROGRAM A04 - Scientific Content Population: SNRIs.

## Mission

A04-004 - SNRI_POPULATION_EXECUTION_PLAN.

## Objective

Define the governed sequence for SNRI scientific content population before any extraction or field population begins.

## Preconditions

- Program A03 completed as SSRI internal draft package.
- Program A04 initialized.
- SNRI official portfolio exists.
- Program A04.0 completed the SNRI Scientific Corpus.
- A04-003 reconciled the former corpus blocker.

## SNRI Portfolio

- Venlafaxine
- Desvenlafaxine
- Duloxetine
- Levomilnacipran
- Milnacipran

## Execution Principle

SNRI population must proceed by reusable pipeline steps and field-level traceability.

No field may be populated without:

- source ID;
- source anchor;
- extraction note;
- normalization status;
- review status;
- editorial status;
- runtime eligibility status.

## Required Sequence

```text
A04-005 - SNRI_PROFILE_SHELLS
A04-006 - SNRI_SOURCE_ANCHOR_PLAN
A04-007 - SNRI_FIELD_TRACEABILITY_MATRIX
A04-008 - SNRI_EXTRACTION_GATES
A04-009 - SNRI_MECHANISM_POPULATION_DRAFT
A04-010 - SNRI_PK_POPULATION_DRAFT
A04-011 - SNRI_PD_POPULATION_DRAFT
A04-012 - SNRI_SAFETY_POPULATION_DRAFT
A04-013 - SNRI_EVIDENCE_BINDING_DRAFT
A04-014 - SNRI_QA_REVIEW
A04-015 - SNRI_PUBLICATION_CANDIDATE
A04-016 - PROGRAM_A04_BASELINE
```

## Gate Before Extraction

A04-005 through A04-008 must complete before any scientific field population begins.

## Runtime Eligibility

All A04 artifacts remain:

```text
not_runtime_eligible
```

until a future runtime eligibility pipeline explicitly changes this status.

## Forbidden During A04

- prescription;
- therapeutic recommendation;
- dose guidance;
- medication selection;
- autonomous clinical decision;
- runtime clinical consumption;
- field population without source anchor;
- evidence grading without traceability.

## Next Mission

A04-005 - SNRI_PROFILE_SHELLS.

## Final Declaration

Program A04 has an execution plan. The next authorized step is to create empty SNRI profile shells with traceability placeholders only.
