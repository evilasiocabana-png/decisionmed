# SSRI Scientific Source Corpus - Source Index

## Status

Raw intake completed.

This index belongs to:

```text
PROGRAM A02.5 - SSRI Source Corpus Intake
MISSION A02.5-002 - SSRI Source Corpus Intake
```

## Purpose

Register the first official SSRI scientific source corpus without extracting clinical knowledge.

## Restrictions

This corpus does not authorize:

- medication field population;
- clinical interpretation;
- evidence extraction;
- ontology mapping;
- therapeutic recommendation;
- prescribing guidance;
- Evidence Runtime consumption;
- Knowledge Layer publication.

## Folder Structure

```text
ScientificCorpus/
    Books/
    Guidelines/
    Regulatory/
    Reviews/
    MetaAnalyses/
    RCT/
    Safety/
    Labels/
    Metadata/
    Manifest/
```

## Registered Candidate Sources

| ID | Source | Type | Status |
| --- | --- | --- | --- |
| SC-SSRI-FDA-FLUOXETINE-001 | Fluoxetine prescribing information | regulatory_label | candidate_registered |
| SC-SSRI-FDA-SERTRALINE-001 | Sertraline prescribing information | regulatory_label | candidate_registered |
| SC-SSRI-FDA-PAROXETINE-001 | Paroxetine prescribing information | regulatory_label | candidate_registered |
| SC-SSRI-FDA-CITALOPRAM-001 | Citalopram prescribing information | regulatory_label | candidate_registered |
| SC-SSRI-FDA-ESCITALOPRAM-001 | Escitalopram prescribing information | regulatory_label | candidate_registered |
| SC-SSRI-FDA-FLUVOXAMINE-001 | Fluvoxamine prescribing information | regulatory_label | candidate_registered |
| SC-SSRI-NICE-NG222-001 | NICE NG222 - Depression in adults | clinical_guideline | candidate_registered |
| SC-SSRI-CANMAT-MDD-2023-001 | CANMAT MDD guideline update | clinical_guideline | candidate_registered |
| SC-SSRI-CANMAT-RESOURCE-2023-001 | CANMAT guideline resource page | guideline_resource | candidate_registered |

## Initial Inventory RC1

The first official document inventory for the corpus is registered in:

- `ScientificCorpus/Manifest/INITIAL_CORPUS_INVENTORY_RC1.json`
- `ScientificCorpus/Manifest/INITIAL_CORPUS_INVENTORY_RC1.md`

This inventory uses only the fields authorized for the current step:

- Source ID;
- official title;
- responsible organization;
- document type;
- edition/version;
- year;
- language;
- license;
- acquisition status;
- checksum;
- physical or logical corpus location.

## Pending Source Families

| ID | Source family | Status |
| --- | --- | --- |
| SC-SSRI-STAHL-ESSENTIAL-001 | Stahl's Essential Psychopharmacology | pending_acquisition |
| SC-SSRI-STAHL-PRESCRIBER-001 | Stahl's Prescriber's Guide | pending_acquisition |
| SC-SSRI-MAUDSLEY-001 | Maudsley Prescribing Guidelines | pending_acquisition |
| SC-SSRI-APA-PRACTICE-GUIDELINE-001 | APA Practice Guideline source family | pending_acquisition |
| SC-SSRI-WFSBP-001 | WFSBP guideline source family | pending_acquisition |
| SC-SSRI-EMA-001 | EMA SSRI regulatory source family | pending_acquisition |
| SC-SSRI-ANVISA-001 | ANVISA SSRI regulatory source family | pending_acquisition |
| SC-SSRI-COCHRANE-001 | Cochrane SSRI review source family | pending_acquisition |
| SC-SSRI-PUBMED-SELECTED-001 | PubMed selected SSRI literature source family | pending_selection |

## Next Mission

```text
MISSION A02.5-003 - Metadata Normalization
```

## Declaration Final

The SSRI Scientific Source Corpus is registered as a raw intake corpus with Initial Inventory RC1 and RC2 defined. It is not normalized, not validated and not ready for knowledge population.
