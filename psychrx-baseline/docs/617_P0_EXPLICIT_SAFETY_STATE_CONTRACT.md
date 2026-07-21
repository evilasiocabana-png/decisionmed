# 617 - P0 Explicit Safety State Contract

## Objective

Ensure that missing safety data is never interpreted as a negative finding.

## Implementation

- created `ClinicalSafetyAssessmentService`;
- defined eight essential safety domains;
- added canonical safe, present and unresolved states;
- made adherence and adverse-effect assessment conditional on current medication;
- expanded `ClinicalSafetyPayload` without removing existing fields;
- preserved structural, non-prescriptive behavior.

## Acceptance

- missing `suicide` produces `Suicidio: Nao avaliado`;
- all essential domains must be explicit;
- a present risk blocks routine strategy;
- no-current-medication marks adherence and adverse effects not applicable;
- dedicated unit tests cover each invariant.

## Files

- `application/clinical_safety_assessment.py`;
- `application/clinical_decision_support_contract.py`;
- `tests/application/test_clinical_safety_assessment.py`.

## Declaration Final

The P0 safety-state contract treats absence of information as uncertainty, in
accordance with the Clinical Safety Contract.
