# DM-035 — Catalog-backed evidence capability

## Objective

Make specialty composition reflect a governed catalog that is already loaded.
When a validated catalog structure contains a form schema for a specialty, the
resolver receives that specialty's structural `evidence` capability binding.

## Contract

- The application derives specialty keys only from loaded form schemas whose
  evidence and knowledge references already passed catalog validation.
- The binding contract version is `0.1.0`, matching the specialty manifest.
- Duplicate keys are collapsed and invalid identifiers fail closed.
- The API exposes `available_capabilities` alongside missing and incompatible
  capabilities.

For the current catalog, cardiology gains only `cardiology.evidence`. Its other
six required capabilities remain missing, so composition remains blocked.

## Safety

A structural binding means only that governed metadata is present and
compatible. It does not mean the draft content is scientifically validated,
does not clear readiness gates, and never enables clinical execution.

## Rollback

Reverting this mission returns planned specialties to reporting all capability
bindings as missing. Catalog data and schema versions are unaffected.
