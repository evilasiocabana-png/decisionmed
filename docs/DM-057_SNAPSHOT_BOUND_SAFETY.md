# DM-057 — Snapshot-bound Safety

## Objective

Bind every safety-check result, aggregated safety assessment, human review, and
Reasoning Gate decision to the exact `ClinicalSnapshot` content fingerprint
introduced by DM-056.

## Contract

`SafetyCheckResult` and `SafetyAssessment` now require a SHA-256
`snapshot_fingerprint`. `SafetyCoordinator` rejects results whose fingerprint
does not match the assessment input. `SafetyPreflight` computes the fingerprint
from the immutable snapshot, requires governed evaluators to return that exact
value, and replaces invalid output with a fail-closed `NOT_EVALUATED` result.

The safety-review digest covers both assessment and result bindings. The
Reasoning Gate checks the current snapshot fingerprint before any other ready
state, so changing snapshot content while retaining its trace ID is rejected.
Audit records contain only the fingerprint, never copied clinical values.

## Safety limits

- content identity does not prove clinical correctness;
- no clinical evaluator, rule, inference, or recommendation is added;
- mismatched evaluator output becomes incomplete rather than usable;
- human review, reasoning execution, and clinical execution remain governed and
  fail-closed.

## Architecture

Domain supplies a technology-independent digest. Safety consumes it without
depending on Application or Audit. Reasoning consumes only Domain and Safety
contracts. Application records bounded metadata and does not decide clinical
logic.

## Rollback

Revert the required fingerprint fields and propagation together. Partial
rollback is unsafe because it would restore trace-only matching.
