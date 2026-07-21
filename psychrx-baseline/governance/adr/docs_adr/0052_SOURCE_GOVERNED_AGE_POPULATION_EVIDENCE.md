# ADR 0052 - Source-Governed Age-Population Evidence

## Status

Accepted for implementation on 2026-07-20 by founder request.

## Context

Program 27 already derives the canonical age bands `CHILD`, `ADOLESCENT`,
`ADULT` and `OLDER_ADULT`, but special populations remain conservatively
blocked because medication-specific population evidence was not normalized.

The founder requested an exhaustive search in official sources and visible
source abbreviations without changing the patient-first essence of PsychRx.

## Decision

Create a medication population-evidence catalog with one row per medication and
canonical age band. Every row must include an official product-information
locator, population statement, source abbreviation, checksum and review state.

Official sources are searched in this order:

1. DailyMed/FDA human prescription label;
2. EMA product information;
3. Health Canada product monograph;
4. UK Summary of Product Characteristics when the medicine is not represented
   by an appropriate DailyMed label.

## Runtime Boundary

The catalog is eligible for source-transparent display only. It may:

- show the official population statement for the patient's age band;
- identify lack of established paediatric or geriatric evidence;
- show a compact source abbreviation beside the statement;
- keep the official URL and section available for audit.

It may not:

- choose or rank a medicine because of age;
- calculate a dose;
- reuse an adult range for a special population;
- convert an official source excerpt into a prescribing instruction;
- remove the existing special-population review gate.

For this reason every catalog row has `therapeutic_runtime_eligible=false`.

## Consequences

The app can now explain why age-specific review is required with an official
source for all catalogued medications. Separate condition-, formulation- and
population-specific scientific review remains required before any future
therapeutic runtime rule can be enabled.

## Rollback

- tag `restore/pre-age-population-20260720-9cc794b`;
- branch `codex/restore-pre-age-population-20260720`;
- bundle `C:\Users\evcab\PsychRx_pre_age_population_20260720_9cc794b.bundle`.

## Declaration Final

Official population information may clarify the review boundary, but it does
not replace physician judgment or scientific approval of a therapeutic rule.
