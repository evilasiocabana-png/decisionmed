# A03-011 - Drug Portfolio Definition

## Status

Completed.

## Mission

Define the detailed editorial structure of the SSRI drug portfolio for Program A03.

This mission does not populate Drug Profiles, interpret literature, create clinical claims or decide therapeutic recommendations.

## Scope

The portfolio is divided into:

- core SSRI portfolio;
- boundary candidates;
- excluded items;
- future review queue.

## Core SSRI Portfolio

| Drug ID | Canonical Name | Portfolio Status | Profile Status | Scientific Content |
| --- | --- | --- | --- | --- |
| SSRI_FLUOXETINE | Fluoxetine | core | not_created | not_populated |
| SSRI_SERTRALINE | Sertraline | core | not_created | not_populated |
| SSRI_ESCITALOPRAM | Escitalopram | core | not_created | not_populated |
| SSRI_CITALOPRAM | Citalopram | core | not_created | not_populated |
| SSRI_PAROXETINE | Paroxetine | core | not_created | not_populated |
| SSRI_FLUVOXAMINE | Fluvoxamine | core | not_created | not_populated |

## Boundary Candidates

| Candidate | Boundary Status | Ontology Decision |
| --- | --- | --- |
| Vilazodone | review_required | not_decided |
| Vortioxetine | review_required | not_decided |

Boundary candidates are preserved for future review. This mission does not classify them as SSRIs and does not exclude them permanently.

## Excluded Items

No excluded medication list is created in this mission.

## Required Future Artifacts Per Core Drug

Each future core drug will require separate gated artifacts before any field can be populated:

- identity record;
- source traceability map;
- evidence placeholder;
- mechanism placeholder;
- PK/PD placeholder;
- safety placeholder;
- interaction placeholder;
- contraindication placeholder;
- monitoring placeholder;
- editorial review record.

All placeholders remain uncreated in this mission.

## Portfolio Rules

1. A drug can be listed as editorial metadata without a Drug Profile.
2. A Drug Profile cannot be populated without source traceability.
3. Boundary candidates require explicit ontology review before inclusion or exclusion.
4. Portfolio inclusion does not imply clinical recommendation.
5. Portfolio inclusion does not imply approval for runtime consumption.
6. Portfolio inclusion does not imply prescription guidance.

## Acceptance Criteria Validation

| Criterion | Result |
| --- | --- |
| Drug Portfolio Definition documented | satisfied |
| Portfolio remains editorial, not clinical | satisfied |
| Boundary candidates remain without ontology decision | satisfied |
| No Drug Profile populated | satisfied |
| No clinical content interpreted | satisfied |
| No scientific content interpreted | satisfied |
| No source document modified | satisfied |
| No extraction created | satisfied |
| No ontology mapping created | satisfied |
| No assertion created | satisfied |

## Next Mission

```text
MISSION A03-012 - Drug Portfolio Editorial Registry
```

## Declaration Final

The SSRI drug portfolio is defined as editorial metadata only. No SSRI has been clinically modeled, scientifically populated or made available for recommendations.
