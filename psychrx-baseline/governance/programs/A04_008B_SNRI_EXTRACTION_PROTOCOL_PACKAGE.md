# A04-008B - SNRI Extraction Protocol Package

## Program

PROGRAM A04 - Scientific Content Population: SNRIs.

## Mission

A04-008B - SNRI_EXTRACTION_PROTOCOL_PACKAGE.

## Objective

Create the extraction protocol package required before SNRI scientific extraction.

## Created Artifact

- `KnowledgeBase/SNRIs/Traceability/SNRI_EXTRACTION_PROTOCOL_PACKAGE.json`

## Protocol Scope

The package defines:

- required inputs before extraction;
- allowed extraction states;
- required fields per extracted claim;
- hard blockers;
- extraction order;
- fields excluded from the current extraction wave.

## Current Gate Result

```text
BLOCKED
```

A04-009 - SNRI_MECHANISM_POPULATION_DRAFT may not start yet.

## Blocking Reason

Source section selection is still missing for SNRI drug-field anchors.

## Required Next Action

```text
A04-008C - SNRI_SOURCE_SECTION_SELECTION_OR_BLOCKER
```

This mission must either:

1. select source sections from available source texts; or
2. formally block extraction until source texts are available.

## Explicit Non-Actions

No scientific content was extracted.

No source section was selected.

No SNRI profile field was populated.

No evidence was graded.

No therapeutic recommendation was created.

No prescription or dose guidance was created.

## Runtime Eligibility

```text
not_eligible
```

## Final Declaration

The extraction protocol package exists, but A04-009 remains blocked until source sections are selected or source text availability is formally resolved.

