# R01 Migration Risks

## Mission

R01-003 - ROADMAP_MIGRATION_EXECUTION_PLAN.

## Risk Register

| Risk | Severity | Mitigation |
| --- | --- | --- |
| Historical mission IDs become confused with pipeline execution IDs | High | Keep both IDs visible in queue and reports. |
| Old roadmap documents appear deleted or invalid | Medium | Mark as historical or legacy, never delete. |
| Pipeline compression hides safety gates | High | Gate map required for every pipeline. |
| Scientific corpus work resumes without validation | High | Keep A04.0-005 paused until R01-004. |
| Runtime eligibility is implied by publication | Critical | RuntimeEligibilityPipeline remains locked. |
| Drug classes with special risks use generic flow unsafely | High | Require class-specific safety gate overlays. |
| Agents execute from chat memory | High | Continue State Driven Protocol and NEXT_MISSION enforcement. |
| R01 planning is mistaken for migration execution | Medium | R01-003 explicitly does not migrate. |

## High-Risk Drug Class Overrides

The following classes require additional safety gate overlays before pipeline execution:

- TCAs;
- MAOIs;
- FGAs;
- SGAs;
- mood stabilizers;
- anxiolytics and hypnotics;
- ADHD medications;
- cognitive enhancers in older adults.

## Runtime Risk

No object produced by corpus, extraction, evidence or publication pipelines becomes runtime eligible automatically.

Runtime eligibility requires a later formal gate and clinical governance approval.

## Traceability Risk

Every future pipeline execution must preserve:

- source ID;
- source path;
- source anchor;
- extraction record;
- normalization status;
- scientific review status;
- editorial review status;
- publication status.

## Final Declaration

R01 reduces operational complexity, but only if gates and traceability remain explicit.
