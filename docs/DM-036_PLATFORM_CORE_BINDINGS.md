# DM-036 — Platform core capability bindings

## Objective

Reflect two specialty-neutral providers that already exist in DecisionMEd:
the immutable clinical snapshot contract and the metadata-only audit ledger.

## Contract

- Every registered specialty receives namespaced `clinical-snapshot` and
  `audit` bindings at contract version `0.1.0`.
- Provider descriptors are `decisionmed.domain.clinical-snapshot` and
  `decisionmed.audit.ledger`.
- Specialty keys are validated, deduplicated, and ordered deterministically.
- Catalog-backed evidence bindings remain independent.

With the current catalog, cardiology has three structural capabilities:
snapshot, evidence, and audit. Safety, reasoning, explanation, and monitoring
remain missing, so the specialty stays blocked.

## Safety and privacy

These descriptors do not expose the snapshot store, accept patient values, or
create a medical record. Audit events remain metadata-only. All resolver states
continue to return `clinical_execution_allowed = false`.

## Rollback

Reverting this mission makes the two providers appear missing again without
changing data, catalog schemas, or persisted state.
