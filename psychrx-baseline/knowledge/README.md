# Knowledge Layer

## Purpose

The `knowledge/` package is the technology-independent Knowledge Layer of PsychRx.

It is reserved for structured clinical knowledge infrastructure: base knowledge objects, knowledge models, repository contracts, loaders, validators, and versioning support.

## Current Baseline

Sprint 8, Missions 061-070 created the initial Knowledge Layer infrastructure baseline.

This baseline includes:

- package structure;
- base knowledge object;
- lifecycle status values;
- version primitives;
- repository contracts;
- loader contracts;
- structural validator;
- guideline schema without content;
- evidence schema without content;
- test helpers;
- structural and contract tests.

This baseline intentionally does not implement:

- clinical engines;
- clinical decisions;
- recommendations;
- therapeutic rules;
- guidelines with content;
- evidence with content;
- psychopharmacological knowledge entries;
- AI loading;
- PDF importing;
- parsing;
- database access;
- persistence;
- ORM mapping;
- framework integrations.

## Package Layout

```text
knowledge/
  __init__.py
  core/
  models/
  repositories/
  loaders/
  validators/
  versioning/
```

## Dependency Rules

The Knowledge Layer organizes structured knowledge, but it must not execute clinical decisions.

It must remain independent of:

- user interface behavior;
- dashboard behavior;
- database implementations;
- framework-specific code;
- clinical engine execution;
- hardcoded therapeutic recommendations.

Knowledge may later expose contracts and structured objects to reasoning, safety, evidence, application, and audit layers according to the official architecture.

## Governance Rules

Future knowledge objects must follow:

- `docs/040_KNOWLEDGE_COMPUTING_ARCHITECTURE.md`;
- `docs/042_MODULE_SPECIFICATION.md`;
- `docs/050_ENGINEERING_BLUEPRINT.md`;
- `docs/EVIDENCE_TRACEABILITY_POLICY.md`;
- `docs/NAMING_CONVENTIONS.md`.

No scientific content should enter this package without source, version, status, traceability, validation, and review policy.

By ADR-0002, real scientific content should be populated in `psychrx-knowledge` or in a formally isolated equivalent area prepared for extraction into that repository.
