# A03-031 - Extraction Protocol

## Program

Program A03 - Scientific Content Population: SSRIs.

## Phase

Phase 3.5 - Scientific Knowledge Acquisition.

## Mission

Define the official protocol for extracting scientific information from the approved SSRI corpus into structured knowledge fields.

## Purpose

Ensure that every future field value is extracted through the same method, with traceability, review and validation.

## Extraction Flow

```text
Source
-> Candidate Passage
-> Extraction Claim
-> Field Mapping
-> Source Binding
-> Normalization
-> Scientific Review
-> Validation
-> Knowledge Object
-> Publication Gate
```

## Mandatory Principles

- no source-free field;
- no value without traceability;
- no recommendation;
- no prescription;
- no runtime consumption;
- no field publication without review;
- no silent conflict resolution.

## Allowed Extraction Targets

- mechanism fields;
- PK fields;
- PD fields;
- indication fields;
- posology fields;
- contraindication fields;
- safety fields;
- evidence binding fields.

## Prohibited Outputs

- patient-specific guidance;
- therapeutic strategy;
- prescribing instruction;
- runtime rule;
- clinical decision;
- automated alert;
- unreviewed scientific claim.

## Next Mission

`A03-032 - EXTRACTION_SCHEMA`

## Declaration Final

A03-031 creates the scientific extraction protocol required before Phases 4 through 9 can be executed.
