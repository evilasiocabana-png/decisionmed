# Program A04.0 - SNRI Scientific Corpus

## Track

Track A - Scientific Knowledge Expansion.

## Status

New intermediate program required to unblock Program A04.

## Objective

Create the official SNRI scientific source corpus before scientific population of SNRI knowledge objects.

This program is equivalent in role to Program A02.5 for SSRIs.

## Rationale

Program A04 cannot safely populate SNRI mechanism, pharmacokinetics, pharmacodynamics, safety, evidence, QA or publication artifacts without an SNRI-specific scientific corpus.

The current blocker is:

`A04-003 - SNRI_SOURCE_CORPUS_INTAKE`

Program A04.0 formalizes the corpus work needed to resolve that blocker.

## Scope

SNRI portfolio:

- Venlafaxine
- Desvenlafaxine
- Duloxetine
- Levomilnacipran
- Milnacipran

## Phases

### Phase 1 - Source Discovery

Identify candidate sources for the SNRI corpus.

### Phase 2 - Source Catalog and Corpus Intake

Catalog and register raw source metadata without interpreting scientific content.

### Phase 3 - Metadata Normalization

Normalize administrative metadata such as title, organization, year, identifiers and access status.

### Phase 4 - Source Validation

Validate source existence, accessibility, duplicates and required fields.

### Phase 5 - Editorial Registration

Register editorial status and review readiness.

### Phase 6 - Corpus Publication

Publish the source corpus as a controlled internal corpus package.

## Missions

```text
A04.0-001 - SNRI_SOURCE_DISCOVERY
A04.0-002 - SNRI_SOURCE_CATALOG
A04.0-003 - SNRI_SOURCE_CORPUS_INTAKE
A04.0-004 - SNRI_METADATA_NORMALIZATION
A04.0-005 - SNRI_SOURCE_VALIDATION
A04.0-006 - SNRI_EDITORIAL_REGISTRATION
A04.0-007 - SNRI_CORPUS_PUBLICATION
A04.0-008 - PROGRAM_A04_0_COMPLETION_GATE
```

## Allowed Work

- source discovery;
- raw source intake;
- administrative metadata;
- identifiers;
- access status;
- source location;
- duplication marking;
- validation reports;
- editorial registration;
- controlled corpus publication.

## Forbidden Work

- mechanism extraction;
- PK extraction;
- PD extraction;
- safety extraction;
- evidence grading;
- therapeutic recommendation;
- prescription;
- runtime clinical consumption;
- comparison between SSRIs and SNRIs;
- clinical interpretation.

## Expected Artifacts

- `ScientificCorpus/SourceTextIntake/SNRIs/SNRI_SOURCE_DISCOVERY.json`
- `ScientificCorpus/SNRIs/Manifest/SNRI_SOURCE_DISCOVERY.json`
- `ScientificCorpus/SNRIs/Manifest/SNRI_SOURCE_INDEX.json`
- `ScientificCorpus/SNRIs/Manifest/SNRI_SOURCE_STATUS.json`
- `ScientificCorpus/SNRIs/Manifest/SNRI_SOURCE_CATALOG.json`
- `ScientificCorpus/SNRIs/Manifest/SNRI_SOURCE_CORPUS_MANIFEST.json`
- `ScientificCorpus/SNRIs/Indexes/MASTER_CORPUS_INDEX.json`
- `ScientificCorpus/SourceTextIntake/SNRIs/SNRI_SOURCE_INVENTORY_RC1.json`
- `ScientificCorpus/SourceTextIntake/SNRIs/SNRI_SOURCE_INVENTORY_RC1.md`
- `ScientificCorpus/SourceTextIntake/SNRIs/SNRI_NORMALIZED_SOURCE_REGISTRY.json`
- `ScientificCorpus/SourceTextIntake/SNRIs/SNRI_SOURCE_VALIDATION_REPORT.md`
- `ScientificCorpus/SourceTextIntake/SNRIs/SNRI_EDITORIAL_REGISTRATION.json`
- `ScientificCorpus/SourceTextIntake/SNRIs/SNRI_CORPUS_PUBLICATION_MANIFEST.json`
- `docs/PROGRAM_A04_0_COMPLETION_REPORT.md`

## Dependency

Program A04.0 depends on:

- Program A03 completed as internal draft package;
- Program 21 Scientific Validation Framework;
- Program 22 Knowledge Governance Platform;
- Evidence Traceability Policy.

## Unlock Condition

Program A04 can resume after:

- A04.0-008 passes;
- SNRI corpus publication manifest exists;
- source validation report exists;
- editorial registration exists.

## Final Declaration

Program A04.0 is the official intermediate program required to unblock Program A04. It creates only the SNRI source corpus and does not populate scientific knowledge fields.
