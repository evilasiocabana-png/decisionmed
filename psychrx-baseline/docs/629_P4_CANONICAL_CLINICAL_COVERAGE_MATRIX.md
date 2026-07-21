# 629 - P4 Canonical Clinical Coverage Matrix

## Objective

Reconcile every psychiatry theme identified in the WeMeds comparison into one
canonical, testable taxonomy.

## Matrix Contract

The matrix contains exactly 51 unique topics and 51 unique canonical contexts:

| Classification | Count | Meaning |
|---|---:|---|
| `covered` | 17 | Existing PsychRx structural flow or context |
| `partial` | 13 | Safety/context coverage exists but is not a complete module |
| `relevant_gap` | 12 | Registry boundary or absent structured coverage |
| `contextual_only` | 9 | Context only; no pharmacological expansion intended |

Every row records runtime scope, priority, source status and a boundary note.
`covered` does not mean scientifically certified: those rows remain labelled
`structural_coverage_scientific_review_pending` after the P3 audit.

## Validation Invariants

- exact topic count and classification counts;
- unique topic identifiers;
- unique canonical contexts;
- contextual-only entries must remain `context_only` and `no_expansion`;
- no classification can promote a treatment rule.

## Files

- `knowledge_base/coverage/wemeds_psychiatry_coverage_matrix.csv`;
- `application/clinical_coverage_matrix.py`;
- `tests/application/test_clinical_coverage_matrix.py`.

## Declaration Final

All 51 audited themes are accounted for without claiming that identified
scientific or product gaps have been filled.
