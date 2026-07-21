# A02.5-001 - Source Discovery

## Objective

Formally record the initial SSRI source discovery step for Program A02.5.

This document does not validate sources and does not extract clinical or therapeutic claims.

## Input Used

The existing candidate source matrix was used as the discovery input:

```text
docs/A03_SOURCE_ACQUISITION_MATRIX.md
```

## Candidate Regulatory Sources

| Medication | Candidate source family | Status |
| --- | --- | --- |
| Fluoxetine | DailyMed/FDA label | candidate_source |
| Sertraline | DailyMed/FDA label | candidate_source |
| Paroxetine | DailyMed/FDA label | candidate_source |
| Citalopram | DailyMed/FDA label | candidate_source |
| Escitalopram | DailyMed/FDA label | candidate_source |
| Fluvoxamine | DailyMed/FDA label | candidate_source |

## Candidate Guideline Sources

| Source family | Status |
| --- | --- |
| NICE depression guideline | candidate_source |
| CANMAT MDD guideline | candidate_source |
| CANMAT guideline resource page | candidate_source |

## Pending Source Families

The following source families still require corpus intake, bibliographic identification and validation:

- Stahl's Essential Psychopharmacology;
- Maudsley Prescribing Guidelines;
- APA Practice Guideline;
- WFSBP;
- EMA;
- ANVISA;
- Cochrane reviews;
- PubMed-selected primary or secondary literature.

## Discovery Status

Source discovery is sufficient to open the corpus intake mission.

It is not sufficient to populate any SSRI scientific field.

## Restrictions

This mission does not authorize:

- field extraction;
- medication population;
- dose guidance;
- indication mapping;
- interaction mapping;
- adverse effect mapping;
- recommendation generation;
- Evidence Runtime consumption;
- clinical use.

## Next Mission

```text
MISSION A02.5-002 - SSRI Source Corpus Intake
```

## Declaration Final

Mission A02.5-001 records candidate source discovery only. The PsychRx scientific corpus remains unvalidated until A02.5-002 and subsequent validation missions are completed.
