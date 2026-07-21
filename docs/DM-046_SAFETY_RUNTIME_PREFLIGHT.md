# DM-046 — Safety runtime preflight

## Objective

Create the first internal, fail-closed orchestration path from a governed
`ClinicalSnapshot` to `SafetyAssessment`, without adding a clinical rule or an
application/interface entry point.

## Contract

`SafetyPreflight` starts only with complete evaluator coverage. It invokes each
registered evaluator only when the snapshot is structurally complete and its
specialty matches every governed check. Evaluator exceptions, wrong result types,
wrong check identities, and wrong traces are normalized to `NOT_EVALUATED` so the
coordinator returns an incomplete assessment.

A successful structural run reaches only `READY_FOR_HUMAN_REVIEW`; clinical
execution remains false.

## Safety limits

- no real evaluator or clinical rule is added;
- no patient-data API or persistence is added;
- no result is exposed to the application or interface;
- no strategy, diagnosis, prescription, or recommendation is produced;
- audit integration remains a separate required mission before application use.

## Architecture

The increment remains inside the Safety Layer and depends only on Domain and
Evidence contracts, as allowed by the layer rules and ADR 0014.

## Rollback

Remove the preflight module, export, tests, and this document. No schema,
catalog, or persisted data changes.
