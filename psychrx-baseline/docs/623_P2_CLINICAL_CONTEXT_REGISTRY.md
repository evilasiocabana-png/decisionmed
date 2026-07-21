# 623 - P2 Clinical Context Registry

## Objective

Create a canonical vocabulary for high-value clinical contexts found in the
coverage audit without turning PsychRx into a disease encyclopedia.

## Registry Scope

The registry contains 23 contexts across:

- acute risk;
- adverse history;
- adverse syndromes;
- substance context;
- diagnostic boundaries;
- population boundaries.

Each entry declares an identifier, label, category, runtime behavior, evidence
status, source anchor, clinical boundary and the permanent
`treatment_rule_allowed = false` restriction.

## Runtime Semantics

- `BLOCK_ROUTINE`: suspend routine ranking and require clinical review;
- `REVIEW_CONTEXT`: preserve and display the context without creating a
  treatment rule;
- unknown context identifier: explicit block instead of silent acceptance.

## Scientific Boundary

Acatisia, parkinsonism medicamentoso, distonia aguda and discinesia tardia are
registered with `source_pending`. Serotonin syndrome and neuroleptic malignant
syndrome remain source-anchored screening contexts. No entry diagnoses a
syndrome or defines treatment.

## Files

- `application/clinical_context_registry.py`;
- `tests/application/test_clinical_context_registry.py`.

## Declaration Final

The missing contexts are now structurally representable without being falsely
declared scientifically complete.
