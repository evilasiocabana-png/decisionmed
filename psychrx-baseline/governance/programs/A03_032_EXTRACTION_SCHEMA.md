# A03-032 - Extraction Schema

## Program

Program A03 - Scientific Content Population: SSRIs.

## Phase

Phase 3.5 - Scientific Knowledge Acquisition.

## Mission

Define the canonical extraction object used to capture scientific information before normalization and review.

## Extraction Object Fields

- extraction_id;
- source_id;
- source_location;
- source_type;
- drug_id;
- target_domain;
- target_field;
- extracted_text_reference;
- extraction_claim;
- extraction_status;
- reviewer_status;
- normalization_status;
- conflict_status;
- publication_status;

## Required Status Values

- draft;
- extracted;
- awaiting_normalization;
- awaiting_review;
- validated;
- rejected;
- conflicting;
- deprecated.

## Boundary

This schema defines how extraction records are represented. It does not extract content from sources.

## Next Mission

`A03-033 - NORMALIZATION_RULES`

## Declaration Final

A03-032 defines the structure required for controlled scientific extraction records.
