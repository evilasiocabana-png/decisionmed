# 635 - Official Monitoring Source Registry

## Published Sources

| Rule | Trigger | Official source | Section anchor |
| --- | --- | --- | --- |
| `TPC-005` | clinician-selected antidepressant withdrawal | NICE NG222 | 1.4.12-1.4.21 |
| `TPC-012` | lithium in current medication list | NICE CG185 | 1.10.14-1.10.24 |
| `TPC-014` | antipsychotic in current medication list | NICE CG178 | 1.3.5.1-1.3.6.4 |
| `TPC-015` | antipsychotic in current medication list | NICE CG178 | 1.3.5.1-1.3.6.5 |

The machine-readable publication record is
`knowledge_base/decision_support_engine/tables/monitoring_runtime_rules.csv`.

## Review Record

All four rows record:

- `verified_against_official_guideline`;
- `approved_for_non_prescriptive_runtime`;
- `published_monitoring_knowledge_object`;
- source identifier, exact section, URL and review date;
- an explicit boundary against diagnosis, prescribing and dose operations.

## Extracted Monitoring Meaning

- NG222 supports monitoring withdrawal symptoms and return of depressive
  symptoms during staged reduction, with review frequency based on clinical and
  support needs.
- CG185 supports baseline and longitudinal lithium laboratory/clinical review,
  including lithium levels, renal, thyroid, calcium, weight/BMI and
  neurotoxicity surveillance.
- CG178 supports baseline and longitudinal movement, metabolic and physical
  health review with explicit follow-up intervals.

## Declaration Final

The publication registry contains monitoring knowledge, not a medication
recommendation, prescription, individual risk diagnosis or automatic order.
