# A03-012 - Drug Portfolio Editorial Registry

## Program

Program A03 - Scientific Content Population: SSRIs.

## Mission

MISSION A03-012 - Drug Portfolio Editorial Registry.

## Objective

Create the editorial registry for the SSRI portfolio defined in A03-011, connecting each editorial identifier to the empty Program A03 registries without creating Drug Profiles, interpreting literature, extracting scientific fields or generating clinical content.

## Source Definition

This registry is derived from:

- `KnowledgeBase/SSRIs/Metadata/DRUG_PORTFOLIO_DEFINITION.json`
- `docs/A03-011_DRUG_PORTFOLIO_DEFINITION.md`

## Editorial Scope

The registry records only administrative and editorial metadata:

- editorial identifier;
- drug identifier;
- canonical name;
- portfolio status;
- registry status;
- profile status;
- scientific content status;
- editorial status.

## Core Portfolio Entries

| Editorial ID | Drug ID | Canonical Name | Portfolio Status | Registry Status |
| --- | --- | --- | --- | --- |
| A03_ED_SSRI_FLUOXETINE | SSRI_FLUOXETINE | Fluoxetine | core | registered_metadata_only |
| A03_ED_SSRI_SERTRALINE | SSRI_SERTRALINE | Sertraline | core | registered_metadata_only |
| A03_ED_SSRI_ESCITALOPRAM | SSRI_ESCITALOPRAM | Escitalopram | core | registered_metadata_only |
| A03_ED_SSRI_CITALOPRAM | SSRI_CITALOPRAM | Citalopram | core | registered_metadata_only |
| A03_ED_SSRI_PAROXETINE | SSRI_PAROXETINE | Paroxetine | core | registered_metadata_only |
| A03_ED_SSRI_FLUVOXAMINE | SSRI_FLUVOXAMINE | Fluvoxamine | core | registered_metadata_only |

## Boundary Candidates

| Editorial ID | Candidate | Boundary Status | Ontology Decision | Registry Status |
| --- | --- | --- | --- | --- |
| A03_BOUNDARY_VILAZODONE | Vilazodone | review_required | not_decided | tracked_not_included |
| A03_BOUNDARY_VORTIOXETINE | Vortioxetine | review_required | not_decided | tracked_not_included |

Boundary candidates are tracked only to preserve governance. They are not included as core SSRIs and no ontology decision is made in this mission.

## Explicit Non-Actions

This mission does not:

- create Drug Profiles;
- populate doses;
- populate indications;
- populate mechanisms;
- populate pharmacokinetics or pharmacodynamics;
- populate safety fields;
- classify evidence;
- interpret source documents;
- create therapeutic recommendations;
- authorize runtime consumption.

## Created Registry

The structured registry is:

- `KnowledgeBase/SSRIs/Registries/DRUG_PORTFOLIO_EDITORIAL_REGISTRY.json`

## Next Mission

The next authorized mission is:

- A03-013 - Drug Portfolio Source Binding

This next mission may bind portfolio entries to source-corpus identifiers at registry level only. It must not interpret, extract, normalize scientific claims or populate medication fields.

## Acceptance Status

- Editorial registry created: satisfied.
- All core IDs registered: satisfied.
- Boundary candidates marked `review_required`: satisfied.
- Metadata-only scope preserved: satisfied.
- No Drug Profile populated: satisfied.
- No clinical or scientific content interpreted: satisfied.
- No source document modified: satisfied.
- No extraction, ontology mapping or assertion created: satisfied.

## Declaration Final

A03-012 creates only the editorial registry of the SSRI portfolio. It does not authorize scientific population, clinical interpretation, therapeutic recommendation, prescription or runtime consumption.
