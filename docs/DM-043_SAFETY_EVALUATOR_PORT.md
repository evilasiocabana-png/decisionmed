# DM-043 — Safety evaluator port

## Objective

Define the formal boundary a future safety-check implementation must satisfy,
without supplying an implementation or clinical rule.

## Contract

`SafetyCheckEvaluator` identifies its governed check and exact specification
version. Its only operation receives an immutable `ClinicalSnapshot`, requires an
explicit trace, and returns a `SafetyCheckResult` for fail-closed aggregation.

The protocol cannot be instantiated and no evaluator is registered by this
mission.

## Safety limits

There is no threshold, interaction, contraindication, diagnosis, recommendation,
patient-data interface, provider implementation, or clinical execution grant.
Future implementations still require sourced clinical knowledge, safety tests,
human scientific review, and regulatory validation.

## Rollback

Remove the protocol module, export, tests, and this document. No schema or data
migration is involved.
