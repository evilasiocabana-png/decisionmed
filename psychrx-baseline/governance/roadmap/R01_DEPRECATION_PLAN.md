# R01 Deprecation Plan

## Mission

R01-003 - ROADMAP_MIGRATION_EXECUTION_PLAN.

## Purpose

Define how duplicated roadmap artifacts will be labeled after migration approval.

No document is removed in R01-003.

## Deprecation Labels

| Label | Meaning |
| --- | --- |
| ACTIVE | The document is part of the current execution model. |
| HISTORICAL | The document records past design or execution. |
| MAPPED | The document is represented by a new pipeline or framework. |
| LEGACY | The document should not drive future execution unless explicitly reactivated. |
| DEPRECATED | The document has been superseded for operational planning. |
| PAUSED | The mission is valid but temporarily not executable. |
| BLOCKED | The mission cannot execute until a dependency is satisfied. |
| MIGRATED | The mission or program has an approved replacement in the new model. |

## What Can Be Deprecated Later

- duplicated future drug-class roadmaps;
- repeated source corpus mission templates;
- repeated metadata normalization templates;
- repeated evidence and publication templates;
- class-specific roadmap scaffolds that are fully represented by pipelines.

## What Cannot Be Deprecated Automatically

- Constitution, Manifesto and foundational principles;
- ADRs;
- safety policies;
- evidence traceability policy;
- clinical safety contract;
- completed execution reports;
- source corpus records;
- scientific audit records;
- runtime safety restrictions.

## Preservation Rule

Deprecation is not deletion.

Every legacy document remains available for audit, historical review and reconstruction.

## R01-004 Requirement

R01-004 must approve any label change from ACTIVE to LEGACY, DEPRECATED or MIGRATED.

## Final Declaration

The old roadmap must be preserved as historical evidence. The new roadmap may become operational only through explicit approval.
