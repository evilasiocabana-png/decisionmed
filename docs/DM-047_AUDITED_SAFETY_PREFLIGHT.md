# DM-047 — Audited safety preflight

## Objective

Make every internal safety preflight completion or unexpected failure auditable
before any future application use, while preserving module boundaries.

## Contract

`SafetyPreflightApplicationService` invokes `SafetyPreflight` and appends a
tamper-evident `DomainEvent` before returning its assessment. Audit failure
prevents an unaudited result from being returned. Unexpected preflight failures
are recorded and re-raised.

Audit payloads contain only bounded technical metadata: status, specialty,
snapshot version, counts, trace, and exception type. They exclude subject
references, observations, clinical values, and exception messages.

## Safety limits

- no application endpoint or interface is added;
- no clinical evaluator or rule is added;
- no persistent or medico-legal audit storage is claimed;
- clinical execution remains false;
- no diagnosis, strategy, prescription, or recommendation is produced.

## Architecture

The orchestration lives in Application, which may depend on Safety, Domain, and
Audit. Safety does not gain a forbidden dependency on Audit.

## Rollback

Remove the application service, export, tests, and this document. No schema,
catalog, or persisted data changes.
