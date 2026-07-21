# DM-044 — Safety evaluator registry

## Objective

Make future evaluator identity verifiable against governed provider descriptors
without invoking or exposing an evaluator through the application.

## Contract

`SafetyCheckEvaluatorRegistry` accepts only objects that satisfy the formal port
and exactly match the descriptor's check ID, provider ID, and specification
version. It reports missing registrations and is complete only when every
provider descriptor has one evaluator object.

Registration is identity-only: the registry never calls `evaluate`.

## Safety limits

No real evaluator is supplied or registered. Completeness never grants clinical
execution, and no clinical rule, patient-data interface, recommendation, or
runtime capability is added.

## Rollback

Remove the registry module, protocol provider property, exports, tests, and this
document. No catalog or persisted data changes.
