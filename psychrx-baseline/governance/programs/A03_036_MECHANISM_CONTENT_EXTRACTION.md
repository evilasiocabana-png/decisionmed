# A03-036 - Mechanism Content Extraction

## Status

Completed as partial controlled extraction.

## Scope

This mission extracted preliminary mechanism claims only from anchors marked `extraction_allowed_next_mission=true` in:

`ScientificCorpus/SourceTextIntake/Mechanism/MECHANISM_SOURCE_ANCHORS.json`

## Extracted

- Fluoxetine
- Paroxetine
- Escitalopram
- Fluvoxamine

## Not Extracted

- Sertraline: pending editorial confirmation of the replacement DailyMed setid.
- Citalopram: pending identification of a valid Mechanism of Action section anchor.

## Files Created

- `KnowledgeBase/SSRIs/Mechanism/Extractions/MECHANISM_EXTRACTION_REGISTRY.json`
- `KnowledgeBase/SSRIs/Fluoxetine/Mechanism/MECHANISM_EXTRACTION.json`
- `KnowledgeBase/SSRIs/Paroxetine/Mechanism/MECHANISM_EXTRACTION.json`
- `KnowledgeBase/SSRIs/Escitalopram/Mechanism/MECHANISM_EXTRACTION.json`
- `KnowledgeBase/SSRIs/Fluvoxamine/Mechanism/MECHANISM_EXTRACTION.json`

## Boundaries

No recommendation, prescription, dosing guidance, safety alert, patient-specific advice or runtime rule was created.

All extracted claims remain `awaiting_review`, `awaiting_normalization` and `not_published`.

## Next Mission

```text
A03-037 - MECHANISM_REVIEW_AND_NORMALIZATION
```

## Declaration

A03-036 created the first controlled SSRI mechanism extraction records in the PsychRx KnowledgeBase while preserving source traceability and preventing runtime clinical use.
