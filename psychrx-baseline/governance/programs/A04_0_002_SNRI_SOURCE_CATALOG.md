# A04.0-002 - SNRI Source Catalog

## Program

PROGRAM A04.0 - SNRI Scientific Corpus.

## Phase

Phase 2 - Source Catalog.

## Mission

Catalog the source candidates identified in A04.0-001 before corpus intake.

## Objective

Assign catalog identifiers, administrative categories and planned corpus locations to all SNRI source candidates without downloading documents or interpreting scientific content.

## Inputs

- `ScientificCorpus/SNRIs/Manifest/SNRI_SOURCE_DISCOVERY.json`
- `ScientificCorpus/SNRIs/Manifest/SNRI_SOURCE_INDEX.json`

## Outputs

- `ScientificCorpus/SNRIs/Manifest/SNRI_SOURCE_CATALOG.json`
- `ScientificCorpus/SNRIs/Manifest/SNRI_SOURCE_CATALOG_INDEX.json`
- `ScientificCorpus/SNRIs/Manifest/SNRI_SOURCE_CATEGORY_INDEX.json`
- `ScientificCorpus/SNRIs/Manifest/SNRI_SOURCE_CATALOG_STATUS.json`

## Cataloged Categories

| Category | Count |
| --- | ---: |
| Books | 3 |
| Guidelines | 5 |
| Regulatory | 5 |
| Reference | 1 |
| Reviews | 1 |
| RCT | 1 |
| Safety | 3 |

Total cataloged sources: 19.

## Planned Corpus Directories

- `ScientificCorpus/SNRIs/Books/`
- `ScientificCorpus/SNRIs/Guidelines/`
- `ScientificCorpus/SNRIs/Regulatory/`
- `ScientificCorpus/SNRIs/Reviews/`
- `ScientificCorpus/SNRIs/MetaAnalyses/`
- `ScientificCorpus/SNRIs/RCT/`
- `ScientificCorpus/SNRIs/Safety/`
- `ScientificCorpus/SNRIs/Reference/`
- `ScientificCorpus/SNRIs/Metadata/`
- `ScientificCorpus/SNRIs/Manifest/`
- `ScientificCorpus/SNRIs/Indexes/`

## Explicit Non-Actions

No PDFs were opened.

No documents were downloaded.

No guideline, book, label, article, trial or safety communication was interpreted.

No source anchor was created.

No scientific anchor was created.

No mechanism, PK, PD, safety or evidence content was extracted.

No Knowledge Object was created.

No runtime object was created.

## Acceptance Criteria

- All source candidates from A04.0-001 have catalog IDs.
- All source candidates have planned corpus locations.
- Category index exists.
- Catalog status exists.
- No scientific interpretation was performed.
- Program A04 remains blocked.

## Next Mission

A04.0-003 - SNRI_SOURCE_CORPUS_INTAKE.

## Final Declaration

A04.0-002 completed the administrative catalog of SNRI source candidates. The corpus is ready for intake structure creation, but it is not normalized, validated, editorially registered, published or runtime eligible.
