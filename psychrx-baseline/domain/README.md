# Domain Layer

## Purpose

The `domain/` package is the technology-independent Domain Layer of PsychRx.

It is reserved for the core domain model, structural domain abstractions, domain events, domain exceptions, domain services, and repository contracts that will be implemented incrementally during Sprint 7.

## Current Mission

Sprint 7, Mission 051 creates structure only.

This mission intentionally does not implement:

- clinical entities;
- clinical value objects;
- psychopharmacological agents;
- therapeutic rules;
- clinical algorithms;
- database access;
- ORM mapping;
- framework integrations;
- interface behavior.

## Package Layout

```text
domain/
  __init__.py
  entities/
  value_objects/
  events/
  services/
  exceptions/
  repositories/
```

## Dependency Rules

The Domain Layer must remain independent of:

- application orchestration;
- interfaces and dashboards;
- databases;
- frameworks;
- persistence mechanisms;
- evidence storage;
- clinical recommendation logic.

Future domain code may use standard language facilities, but must not depend on infrastructure-specific packages.

## Naming Conventions

Future domain concepts must follow `docs/NAMING_CONVENTIONS.md`.

No new clinical entity may be introduced without the corresponding ontology and architecture updates.
