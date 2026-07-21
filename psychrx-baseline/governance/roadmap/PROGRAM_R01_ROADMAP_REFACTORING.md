# Program R01 - Roadmap Refactoring

## Reference

REF: CQ-R01-001

## Mission

R01-001 - ROADMAP_REFACTORING_TO_200_MISSION_MODEL.

## Type

Operational Governance / Roadmap Compression.

## Status

Completed as a governance refactoring package.

## Objective

Refactor the PsychRx roadmap from a class-by-class mission expansion model into a reusable, parameterized pipeline model with no more than 200 total missions.

## Scope

This program does not execute scientific content, clinical runtime, recommendation logic, prescription logic or architecture changes.

It creates a roadmap governance layer that preserves historical documents while compressing future work into reusable pipelines.

## Principle

The project must not create a full new program for every pharmacological class.

Instead of duplicating:

- A03 - SSRIs
- A04 - SNRIs
- A05 - NDRIs
- A06 - NaSSAs
- A07 - TCAs
- A08 - MAOIs

PsychRx will use parameterized pipelines such as:

```text
Scientific Corpus Pipeline[DrugClass]
Drug Class Population Pipeline[DrugClass]
Evidence Integration Pipeline[DrugClass]
Publication Pipeline[DrugClass]
```

## Status of Existing Work

All previous programs remain preserved.

No historical file is deleted.

No existing ADR is modified.

No existing scientific artifact is destroyed.

## New Control Model

The roadmap is now governed by:

- reusable frameworks;
- parameterized pipelines;
- formal gates;
- state-driven execution;
- queue references;
- no more than 200 target missions.

## Next Mission

R01-002 - ROADMAP_REFACTORING_REVIEW.

## Final Declaration

Program R01 compresses the future roadmap without altering clinical architecture, scientific content or runtime eligibility.
