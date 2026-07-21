# DM-048 — Safety result explanations

## Objective

Make every safety-check result explainable, including fail-closed outcomes that
were not evaluated.

## Contract

`SafetyCheckResult.explanation` is required and non-empty for `PASSED`, `FINDING`,
and `NOT_EVALUATED` outcomes. Future evaluators must therefore state what their
result means instead of returning an opaque status.

`SafetyPreflight` supplies bounded technical explanations when it does not invoke
an evaluator because the snapshot is incomplete or specialty-incompatible, and
when an evaluator fails or violates its result contract. Exception messages are
not copied into results.

## Safety limits

The new text is an explanation contract, not clinical knowledge. This mission
adds no risk rule, threshold, diagnosis, strategy, prescription, recommendation,
application endpoint, or clinical execution permission.

## Rollback

Remove the required field and restore the prior preflight constructors and tests.
No schema, catalog, or persisted data changes.
