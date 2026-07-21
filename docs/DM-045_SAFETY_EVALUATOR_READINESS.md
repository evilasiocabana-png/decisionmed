# DM-045 — Safety evaluator readiness

## Objective

Prevent provider descriptors from being mistaken for registered evaluator
implementations in the technical readiness report.

## Readiness contract

After validated specifications and compatible provider coverage, the safety gate
now also requires a non-empty, complete `SafetyCheckEvaluatorRegistry`. Reasons
distinguish absent and incomplete evaluator registration. Counts expose registered
and missing evaluators.

The evaluator registry must reference the exact provider registry configured for
readiness; mixed registries are rejected.

## Safety limits

No evaluator is supplied, invoked, or exposed through the application. Technical
completeness still denies clinical execution and does not represent scientific,
clinical, or regulatory validation.

## Rollback

Remove evaluator injection and restore provider-only readiness. No catalog schema
or persisted data changes.
