# DM-050 — Preflight evidence gate

## Objective

Prevent evaluator invocation when governed evidence is missing, unvalidated, or
out of date, and prevent a preflight from substituting a different evidence
registry after specifications were registered.

## Contract

`SafetyCheckRegistry` exposes its exact `EvidenceRegistry` dependency.
`SafetyPreflight` requires object identity with that registry and rechecks every
specification source before invoking evaluators. Evidence lifecycle failure
produces explained `NOT_EVALUATED` results with zero evaluator calls.

The coordinator retains its post-result evidence checks as defense in depth.

## Safety limits

This mission changes only technical governance gates. It adds no evidence
content, clinical rule, threshold, diagnosis, strategy, prescription,
recommendation, endpoint, or clinical execution permission.

## Rollback

Remove the registry accessor and pre-invocation evidence checks, then restore the
prior tests. No schema, catalog, or persisted data changes.
