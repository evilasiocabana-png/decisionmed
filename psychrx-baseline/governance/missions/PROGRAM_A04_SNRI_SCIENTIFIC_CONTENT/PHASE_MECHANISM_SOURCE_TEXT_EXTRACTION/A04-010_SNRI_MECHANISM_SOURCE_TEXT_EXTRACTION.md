# A04-010 - SNRI Mechanism Source Text Extraction

## Objective

Extract short exact source-text fragments from the A04-008G selected SNRI mechanism sections.

## Scope

This mission is limited to source-text extraction for the mechanism field.

It does not populate mechanism claims, create therapeutic recommendations, prescribe, grade evidence or enable runtime use.

## Sources

- DailyMed official label records.
- Drugs@FDA approved labeling PDFs.

## Sections Used

- Clinical Pharmacology.
- 12.1 Mechanism of Action where available.

## Artifacts Created

- `KnowledgeBase/SNRIs/SourceText/SNRI_MECHANISM_SOURCE_TEXT_EXTRACTS.json`
- `KnowledgeBase/SNRIs/SourceText/SNRI_MECHANISM_SOURCE_TEXT_EXTRACTS.md`
- `KnowledgeBase/SNRIs/Traceability/SNRI_MECHANISM_SOURCE_TEXT_TRACEABILITY.json`

## Review Criteria

A source-text record is reviewable when it contains:

- selected section ID;
- drug ID;
- official source title;
- official source URL;
- section locator;
- short exact source-text fragment;
- extraction status;
- review status;
- runtime-ineligible marker.

## Blocked Items

The following remain blocked:

- PK extraction;
- PD extraction;
- safety extraction;
- evidence grading;
- recommendation;
- prescription;
- clinical runtime.

## Criterion To Release A04-011

A04-011 may start because each A04-008G selected mechanism section now has a reviewable source-text record.

## Declaration

A04-010 is complete as exact source-text extraction only. It does not create clinical knowledge suitable for runtime use.
