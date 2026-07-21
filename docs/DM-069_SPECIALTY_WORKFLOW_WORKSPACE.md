# DM-069 — Specialty workflow workspace

## Outcome

The generic specialty workflow now uses the same visual language as the DecisionMEd workspace hub. It improves navigation, hierarchy, progress visibility and responsive use while preserving the reference-only contract.

## Safety boundary

- The page continues to obtain only workflow and form-schema metadata from the existing APIs.
- It does not render a textarea, form control or patient-value capture path.
- Step advance remains the pre-existing structural in-memory session operation.
- Knowledge, evidence and schema status remain displayed as reference metadata only.

## Verification

`tests/test_mvp_shell.py` verifies the workflow endpoint, reference-only wording, absence of patient input controls and the governed workspace marker.
