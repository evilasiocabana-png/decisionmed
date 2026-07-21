# A04-008F - SNRI Source Section Selection Gate

## Program

PROGRAM A04 - Scientific Content Population: SNRIs.

## Mission

A04-008F - SNRI_SOURCE_SECTION_SELECTION_GATE.

## Objective

Evaluate whether selected and reviewable source sections exist before A04-009.

## Gate Artifact

- `KnowledgeBase/SNRIs/Traceability/SNRI_SOURCE_SECTION_SELECTION_GATE.json`

## Gate Result

```text
BLOCKED
```

A04-009 - SNRI_MECHANISM_POPULATION_DRAFT may not start.

## Passed Gates

- Source text locators exist.
- Runtime remains disabled.

## Failed Gates

- No source sections have been selected.
- No selected sections are reviewable.

## Blocking Reason

Source section locators exist, but no source sections have been selected and reviewed.

## Required Next Action

Manual or governed source-section selection must occur before scientific extraction.

## Explicit Non-Actions

No source text was interpreted.

No scientific claim was extracted.

No SNRI profile field was populated.

No evidence was graded.

No therapeutic recommendation was created.

No prescription, dose guidance or clinical decision was created.

## Runtime Eligibility

```text
not_eligible
```

## Final Declaration

Program A04 is blocked before A04-009 until selected and reviewable source sections exist.

