# 627 - P3 Runtime Eligibility and Monitoring

## Objective

Prevent pending scientific content from appearing as formally eligible while
preserving the useful structural comparison already present in PsychRx.

## Implementation

- pharmacological ranking options now carry their source-row status;
- local matrix citations expose the real row status instead of claiming a
  reviewed-table quality;
- disease-use eligibility display includes formal-review status;
- Motor 2, disease-use and ranking statuses are reconciled for every response;
- when the active rows are not formally validated, response status is
  `unresolved` and scientific readiness is
  `structural_only_scientific_review_pending`;
- the clinical strategy remains visible for physician review, but it is not
  mislabeled as scientifically runtime eligible;
- `MonitoringGovernanceService` keeps four source-validated but
  `runtime_eligible=false` monitoring rules out of automatic behavior;
- only generic structural monitoring targets remain active until promotion is
  explicitly approved;
- unknown interaction profiles continue to produce an explicit warning.

## Physician Boundary

`unresolved` does not mean that the app has no utility. It means the displayed
comparison is structural and must not be mistaken for a scientifically certified
patient-specific recommendation.

## Declaration Final

Scientific eligibility now follows recorded review status rather than the mere
presence of a row in a CSV file.
