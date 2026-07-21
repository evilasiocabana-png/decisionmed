# A03-013 - Drug Portfolio Source Binding

## Program

Program A03 - Scientific Content Population: SSRIs.

## Phase

Phase 2 - Drug Portfolio Definition.

## Objective

Create the official administrative binding between the SSRI Drug Portfolio and the Scientific Source Corpus published by Program A02.5.

This mission creates traceability only. It does not create scientific knowledge.

## Binding Scope

The binding connects:

```text
Drug Registry
-> Editorial Registry
-> ScientificCorpus Source IDs
```

No source text was opened, interpreted, summarized or transformed.

## Created Artifacts

- `KnowledgeBase/SSRIs/Traceability/DRUG_SOURCE_BINDING.json`
- `KnowledgeBase/SSRIs/Traceability/DRUG_SOURCE_BINDING_INDEX.json`
- `KnowledgeBase/SSRIs/Traceability/SOURCE_BINDING_REGISTRY.json`
- `KnowledgeBase/SSRIs/Traceability/SOURCE_BINDING_MANIFEST.json`
- `KnowledgeBase/SSRIs/Traceability/TRACEABILITY_STATUS.json`
- `KnowledgeBase/SSRIs/Metadata/SOURCE_REFERENCE_TEMPLATE.json`

## Drugs Bound

| Drug ID | Editorial ID | Status |
| --- | --- | --- |
| SSRI_FLUOXETINE | A03_ED_SSRI_FLUOXETINE | bound_metadata_only |
| SSRI_SERTRALINE | A03_ED_SSRI_SERTRALINE | bound_metadata_only |
| SSRI_ESCITALOPRAM | A03_ED_SSRI_ESCITALOPRAM | bound_metadata_only |
| SSRI_CITALOPRAM | A03_ED_SSRI_CITALOPRAM | bound_metadata_only |
| SSRI_PAROXETINE | A03_ED_SSRI_PAROXETINE | bound_metadata_only |
| SSRI_FLUVOXAMINE | A03_ED_SSRI_FLUVOXAMINE | bound_metadata_only |

## Source Strategy

Each core SSRI is connected to:

- one normalized official label source when available;
- shared book/guideline/regulatory source IDs from the controlled corpus.

This is an administrative source map. It does not state that any source supports any specific scientific field.

## Boundary Candidates

| Candidate | Editorial ID | Status |
| --- | --- | --- |
| Vilazodone | A03_BOUNDARY_VILAZODONE | tracked_review_required_not_included |
| Vortioxetine | A03_BOUNDARY_VORTIOXETINE | tracked_review_required_not_included |

Boundary candidates remain outside the core SSRI portfolio. No ontology decision was made.

## Explicit Non-Actions

This mission did not:

- open PDFs;
- interpret chapters;
- interpret guidelines;
- interpret regulatory documents;
- summarize source content;
- create mechanisms;
- create PK or PD;
- create dose fields;
- create indications;
- create contraindications;
- create interactions;
- create adverse effects;
- create monitoring fields;
- classify evidence;
- grade recommendations;
- create Drug Profiles;
- create Knowledge Graph entries;
- create Evidence Graph entries;
- create Runtime Objects.

## Next Mission

The next mission is:

```text
MISSION A03-014 - PORTFOLIO_DIRECTORY_GENERATION
```

Phase 3 remains blocked until a Phase 2 baseline/gate explicitly authorizes it.

## Declaration Final

A03-013 creates only administrative traceability between the SSRI portfolio and the Scientific Source Corpus. It does not authorize scientific content population, clinical interpretation, recommendations, prescription or runtime consumption.
