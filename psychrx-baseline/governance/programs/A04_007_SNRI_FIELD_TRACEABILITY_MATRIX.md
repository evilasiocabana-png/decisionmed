# A04-007 - SNRI Field Traceability Matrix

## Program

PROGRAM A04 - Scientific Content Population: SNRIs.

## Mission

A04-007 - SNRI_FIELD_TRACEABILITY_MATRIX.

## Objective

Create the field-level traceability matrix required before any SNRI scientific extraction or field population.

## Created Artifact

- `KnowledgeBase/SNRIs/Traceability/SNRI_FIELD_TRACEABILITY_MATRIX.json`

## Scope

The matrix links each SNRI profile field to:

- planned source anchor slot;
- candidate source IDs;
- required traceability attributes;
- runtime eligibility status;
- field value status.

## Fields Covered

- identification;
- mechanism;
- pharmacokinetics;
- pharmacodynamics;
- indications;
- posology;
- contraindications;
- safety;
- evidence.

## Required Traceability Attributes

Every future populated field must carry:

- source ID;
- source anchor ID;
- source location;
- source section;
- extraction note;
- normalization status;
- scientific review status;
- editorial review status;
- runtime eligibility.

## Field Status

All fields remain:

```text
unpopulated
```

## Runtime Eligibility

```text
not_eligible
```

## Explicit Non-Actions

No content was extracted.

No scientific claim was created.

No profile value was populated.

No evidence was graded.

No therapeutic recommendation was created.

No prescription, dose guidance or clinical decision was created.

## Next Mission

A04-008 - SNRI_EXTRACTION_GATES.

## Final Declaration

The SNRI Field Traceability Matrix exists as a governance artifact. Extraction remains blocked until A04-008 evaluates and records the extraction gates.

