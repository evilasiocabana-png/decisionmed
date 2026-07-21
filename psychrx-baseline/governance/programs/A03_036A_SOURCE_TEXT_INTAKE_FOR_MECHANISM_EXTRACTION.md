# A03-036A - Source Text Intake for Mechanism Extraction

## Status

Completed as controlled source-anchor intake.

## Objective

Register source-text locations and section anchors that allow the next mission, A03-036 - Mechanism Content Extraction, to extract mechanism content without relying on memory, unstated sources or unsourced synthesis.

## Scope Executed

This mission registered administrative anchors for the SSRI mechanism domain using the regulatory label source family already present in the corpus.

The mission did not store source text and did not extract mechanism content.

## Files Created

- `ScientificCorpus/SourceTextIntake/Mechanism/SOURCE_TEXT_INTAKE_MANIFEST.json`
- `ScientificCorpus/SourceTextIntake/Mechanism/MECHANISM_SOURCE_ANCHORS.json`
- `ScientificCorpus/SourceTextIntake/Mechanism/MECHANISM_EXTRACTION_READINESS.json`
- `KnowledgeBase/SSRIs/Mechanism/SourceTextIntake/STATUS.json`

## Anchor Intake Result

Ready for controlled extraction:

- Fluoxetine
- Paroxetine
- Escitalopram
- Fluvoxamine

Requires editorial review before extraction:

- Sertraline, because the original registry setid returned 404 and a current DailyMed candidate was identified by search.
- Citalopram, because the checked SPL XML did not expose a Mechanism of Action heading.

## What Was Not Done

- No mechanism statement was extracted.
- No clinical recommendation was created.
- No therapeutic strategy was created.
- No prescription was created.
- No runtime clinical object was created.
- No evidence ranking was performed.

## Next Mission

```text
A03-036 - MECHANISM_CONTENT_EXTRACTION
```

A03-036 may proceed only for anchors marked `extraction_allowed_next_mission=true`.

## Declaration

A03-036A converts the previous blocker into a usable source-anchor layer. The PsychRx project may now continue Phase 4 with controlled mechanism extraction for the ready anchors only.
