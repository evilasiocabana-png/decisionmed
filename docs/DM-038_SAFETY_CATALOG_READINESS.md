# DM-038 — Safety catalog and readiness

## Objective

Load governed safety-check specifications from the external catalog and make
platform readiness distinguish absence, draft metadata, and validated current
specifications.

## Catalog contract

- Catalog schema version is `7.0.0`.
- `safety-checks.json` is a fourth integrity-protected catalog file.
- Every item must match `SafetyCheckSpecification` exactly.
- Evidence references are resolved by `SafetyCheckRegistry` during loading.
- Empty item collections are valid but remain explicitly blocked.

## Readiness

The safety gate reports:

- `no_safety_specifications` when the registry is empty;
- `unvalidated_safety_specifications` when any item is not validated;
- review lifecycle failures when validated metadata is stale or incomplete;
- `safety_specifications_current` only for a non-empty, fully validated and
  current registry.

Counts expose total, validated, overdue, and unscheduled specifications.

## Safety limits

Catalog presence does not implement an evaluator, process patient data, produce
findings, or bind the specialty `safety` runtime capability. Clinical execution
remains disabled even when metadata is current.

## Migration and rollback

Platform and private catalog must move together to schema `7.0.0`. Rollback must
restore both repositories to schema `6.0.0`; mixed generations fail closed.
