# R01 Migration Plan

## Mission

R01-001 - ROADMAP_REFACTORING_TO_200_MISSION_MODEL.

## Migration Policy

No file movement occurs in R01-001.

No historical program is deleted.

No existing ADR is modified.

This plan is conceptual and must be reviewed in R01-002 before execution.

## Steps

1. Approve the 200 mission model.
2. Mark legacy class-specific programs as historical or mapped.
3. Create canonical pipeline templates.
4. Convert A04.0 into `Scientific Corpus Pipeline[SNRIs]`.
5. Convert A04 into `Drug Class Population Pipeline[SNRIs]`.
6. Convert A05-A15 into parameterized planned executions.
7. Update `NEXT_MISSION.md` after CTO review.
8. Resume either R01-002 review or A04.0-005 validation depending on CTO decision.

## Risks

- Loss of detail if compression is too aggressive.
- Confusion between historical mission IDs and pipeline execution IDs.
- Need for clear queue IDs.
- Need for strict gates to prevent unsafe acceleration.

## Required Gates

- Corpus Gate.
- Metadata Gate.
- Source Validation Gate.
- Extraction Protocol Gate.
- Drug Portfolio Gate.
- Scientific Extraction Gate.
- Normalization Gate.
- Scientific Review Gate.
- Editorial Review Gate.
- Publication Gate.
- Runtime Eligibility Gate.

## Final Declaration

Migration must be approved before changing active scientific execution from mission-by-mission to pipeline-by-parameter.
