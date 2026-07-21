# 636 - Monitoring Runtime Implementation

## Implementation

`MonitoringGovernanceService` now enforces a dual gate:

```text
theory-to-practice runtime eligibility
+ scientific review
+ editorial review
+ published knowledge object
+ official NICE section anchor
+ patient-state trigger
-> visible MonitoringPlan checklist
```

## Trigger Results

- antidepressant plus `taper_or_withdraw` activates `TPC-005`;
- lithium activates `TPC-012`;
- an antipsychotic activates `TPC-014` and `TPC-015`;
- an unrelated medicine activates none of the four;
- removal of either scientific or editorial approval blocks the affected rule.

The decision-support response receives generic and activated targets together
with rule IDs, official sources, section anchors and the non-prescriptive
boundary.

## Safety Boundary

The implementation does not diagnose an event, prescribe, stop or change a
medicine, calculate a dose/taper or choose a treatment. Medication class lookup
is used only to decide whether a monitoring checklist is relevant.

## Validation

- focused monitoring and coverage tests: 9 passed;
- source trigger smoke scenarios: 4 passed;
- Python compilation: passed;
- diff whitespace audit: passed.

## Declaration Final

The four source-governed rules are operational as physician-review checklists
and remain within the original patient-first PsychRx flow.
