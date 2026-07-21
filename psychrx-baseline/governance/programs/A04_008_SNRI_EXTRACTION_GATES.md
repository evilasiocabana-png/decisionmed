# A04-008 - SNRI Extraction Gates

## Program

PROGRAM A04 - Scientific Content Population: SNRIs.

## Mission

A04-008 - SNRI_EXTRACTION_GATES.

## Objective

Evaluate whether Program A04 can proceed to scientific extraction.

## Gate Artifact

- `KnowledgeBase/SNRIs/Traceability/SNRI_EXTRACTION_GATES.json`

## Gate Result

```text
BLOCKED
```

A04-009 - SNRI_MECHANISM_POPULATION_DRAFT may not start yet.

## Passed Gates

- SNRI corpus exists.
- SNRI profile shells exist.
- Source anchor plan exists.
- Field traceability matrix exists.
- Runtime remains disabled.

## Failed Gates

- Definitive source anchors do not exist.
- Drug-specific source section selections do not exist.
- SNRI-specific extraction protocol package does not exist.

## Required Inserted Mission

```text
A04-008A - SNRI_SOURCE_ANCHOR_FINALIZATION
```

## Scope of A04-008A

A04-008A must create definitive drug-specific anchor IDs and section-selection placeholders before any extraction.

It must not extract scientific content.

It must not populate mechanism, PK, PD, safety or evidence fields.

## Runtime Eligibility

```text
not_eligible
```

## Explicit Non-Actions

No scientific extraction was performed.

No SNRI profile field was populated.

No therapeutic recommendation was created.

No prescription or dose guidance was created.

## Final Declaration

Program A04 is blocked before A04-009. The next authorized mission is A04-008A - SNRI_SOURCE_ANCHOR_FINALIZATION.

