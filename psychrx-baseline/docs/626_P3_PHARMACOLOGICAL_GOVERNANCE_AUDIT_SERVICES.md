# 626 - P3 Pharmacological Governance Audit Services

## Objective

Make pharmacological coverage and scientific review status measurable at runtime
without mutating evidence tables.

## Implemented Audit

`PharmacologicalCoverageAuditService` reconciles:

- 83 medications in the pharmacological matrix;
- 38 canonical interaction profiles and 6 explicit name aliases;
- 39 medications resolved to an interaction profile;
- 44 named interaction-profile gaps;
- 347 disease-use rows, all pending formal review;
- 1,444 Motor 2 rows;
- 1,398 Motor 2 rows pending formal review;
- 23 rows pending condition-range research;
- 23 rows with selected official ranges mapped but not formally validated;
- zero formally validated Motor 2 rows;
- 436 rows without a condition-specific range;
- 16 theory-to-practice rules, 4 monitoring-related and zero monitoring rules
  currently runtime eligible.

## Access

The read-only authenticated endpoint `/api/coverage-audit` exposes the same
report. Interaction gaps are named rather than hidden behind an aggregate.

## Boundary

The audit does not fill a missing interaction, validate a dose range or promote
a source. Explicit aliases normalize names only and contain no clinical claim.

## Declaration Final

The current pharmacological evidence debt is now deterministic, testable and
machine-readable.
