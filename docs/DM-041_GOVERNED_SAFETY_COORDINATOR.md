# DM-041 — Governed safety coordinator

## Objective

Remove the raw check-ID path from `SafetyCoordinator` so aggregation can only be
configured through governed, version-compatible provider bindings.

## Contract

The coordinator now requires a `SafetyCheckProviderRegistry` with complete
coverage. Missing or incompatible bindings fail construction. Results that cite
validated evidence outside their check specification remain incomplete with an
explicit `undeclared_evidence` reason.

## Safety limits

This mission aggregates externally produced structural results only. It defines
no evaluator, clinical threshold, contraindication, interaction, diagnosis, or
treatment recommendation. Every assessment continues to deny clinical execution
and can reach at most human review.

## Rollback

Restore raw expected check identifiers in the coordinator and remove the
provider/specification evidence checks. No catalog schema or data changes.
