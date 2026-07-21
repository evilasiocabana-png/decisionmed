# PROGRAM A04.1 - Evidence Anchoring & Scientific Extraction Foundation

## Status

Proposed - Pending Final Governance Review.

## Track

Track A - Scientific Knowledge Expansion.

## Purpose

Build the infrastructure that transforms scientific sources into traceable, reviewable and future-extractable evidence anchors, without creating scientific knowledge, recommendations or clinical runtime objects.

## Why This Program Exists

Program A04 is blocked because A04-009 cannot start until source sections are formally selected and reviewable.

Program A04.1 is proposed as the governed bridge between source corpus availability and future scientific extraction.

Until the final governance review accepts ADR 0049, this program is a planning and staging artifact, not the official active program.

## Scope

Allowed:

- source inventory review;
- source section mapping;
- source section registration;
- reviewable section approval;
- field-to-section anchoring;
- coverage validation;
- extraction rules;
- evidence object schema;
- extraction validation pipeline;
- readiness and gate reports.

Forbidden:

- scientific content extraction;
- mechanism population;
- pharmacokinetic population;
- pharmacodynamic population;
- indication population;
- safety population;
- evidence grading;
- therapeutic recommendation;
- prescription;
- runtime consumption;
- clinical decision support activation.

## Sprint A04.1-01 - Source Section Selection

### A04.1-001 - SOURCE_INVENTORY_REVIEW

Review the SNRI source inventory, identify duplicates, missing editions, missing years, missing identifiers and source readiness for section selection.

### A04.1-002 - SECTION_MAPPING

Map relevant chapters, sections, subsections, page ranges or locator hints without copying or interpreting content.

### A04.1-003 - SECTION_REGISTRATION

Create the official section catalog with SourceID, SectionID, title, page/location metadata, information type and status.

### A04.1-004 - REVIEWABLE_SECTION_APPROVAL

Approve only sections that are clearly delimited, traceable and independently reviewable.

## Sprint A04.1-02 - Scientific Field Anchoring

### A04.1-005 - DRUG_FIELD_MATRIX

Define which section types can support each psychopharmacological model field.

### A04.1-006 - FIELD_ANCHOR_REGISTRATION

Associate model fields with approved SourceID and SectionID pairs.

### A04.1-007 - COVERAGE_VALIDATION

Classify field coverage as COMPLETE, PARTIAL or EMPTY.

## Sprint A04.1-03 - Scientific Extraction Framework

### A04.1-008 - EXTRACTION_RULES

Define extraction rules without extracting content.

### A04.1-009 - EVIDENCE_OBJECT_SCHEMA

Define the official Evidence Object schema without populating evidence.

### A04.1-010 - EXTRACTION_VALIDATION_PIPELINE

Define validation steps required before extraction.

## Sprint A04.1-04 - Program Readiness

### A04.1-011 - FULL_TRACEABILITY_AUDIT

Audit source-to-section-to-field traceability.

### A04.1-012 - GOVERNANCE_AUDIT

Audit compliance with governance documents.

### A04.1-013 - SCIENTIFIC_READINESS_REPORT

Emit the readiness report for future extraction.

### A04.1-014 - GATE_A04_009

Create the official gate for A04-009:

```text
A04-009 Scientific Extraction
READY
or
BLOCKED
```

## Acceptance Criteria

- No scientific content is extracted.
- No field values are populated.
- No clinical runtime eligibility is created.
- Every selected section must be traceable to a source.
- Every future extractable field must be anchored to a reviewable section.
- A04-009 remains blocked until the final gate explicitly releases it.

## Final Declaration

Program A04.1 is proposed as the evidence anchoring foundation required before SNRI scientific extraction. Its governance status remains pending until the final review of this block.
