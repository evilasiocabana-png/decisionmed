# DM-049 — Safety runtime lifecycle gates

## Objective

Recheck governed review lifecycles at runtime so a specification or evidence
source that expires after registration cannot continue to participate silently.

## Contract

Before invoking evaluators, `SafetyPreflight` verifies that every governed
specification is still validated, scheduled, and not overdue. A stale
specification produces `NOT_EVALUATED` results and no evaluator call.

`SafetyCoordinator` now distinguishes evidence that is validated but overdue
from evidence that was never validated. Either state keeps the assessment
from reaching readiness and emits an explicit structural reason.

## Safety limits

This is a lifecycle gate only. It adds no clinical source, rule, threshold,
diagnosis, strategy, prescription, recommendation, endpoint, or clinical
execution permission.

## Rollback

Remove the runtime lifecycle checks, their tests, and this document. No schema,
catalog, or persisted data changes.
