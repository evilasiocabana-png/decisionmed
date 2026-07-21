# 630 - P4 Context Normalization and UI Alignment

## Objective

Align explicit PsychRx context selections with the canonical coverage taxonomy
while preserving the original consultation workflow.

## Implementation

- exact normalization maps only a context explicitly selected or submitted;
- no symptoms, diagnosis or treatment are inferred from the normalized label;
- each decision-support response exposes its coverage classification and source
  status when matched;
- unmatched contexts remain explicitly outside the 51-topic matrix;
- `/api/clinical-coverage` exposes the validated matrix and summary;
- the UI displays only the four aggregate counts in a collapsible audit card;
- the UI does not expose a WeMeds-like disease library or `Apply to case` flow.

## Product Boundary

The coverage matrix is an engineering/governance instrument. It does not replace
the patient-first sequence, and it does not become a second clinical approach.

## Declaration Final

Internal context names, response metadata and the visible coverage audit now use
one canonical vocabulary without changing the essence of PsychRx.
