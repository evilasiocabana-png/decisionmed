# R01 Gap Analysis

## Mission

R01-002 - ROADMAP_REFACTORING_REVIEW.

## Summary

No critical functional, scientific, architectural or runtime governance gap was found in the compressed model.

Several operational gaps must be resolved before migration.

## No-Loss Areas

| Area | Gap Found | Notes |
| --- | --- | --- |
| Architecture | No | Programs 00-05 preserve the architectural foundation. |
| Governance | No | Program 00 and Program 13 preserve governance and release controls. |
| Scientific Corpus | No | Program 06 covers corpus pipeline. |
| Knowledge Population | No | Program 08 covers drug class population. |
| Drug Profiles | No | Program 08 covers drug profile modeling. |
| Evidence | No | Program 09 covers evidence integration. |
| Safety | No | Program 10 covers safety and constraints. |
| Publication | No | Program 11 covers QA and publication. |
| Runtime | No | Programs 04, 12 and 13 preserve runtime and release governance. |
| Clinical Workspace | No | Program 03 preserves workspace. |
| Clinical Kernel | No | Programs 02 and 04 preserve kernel/runtime shell concepts. |

## Operational Gaps

### Gap 1 - Pipeline Templates Not Yet Executable

The compressed model names pipelines, but does not yet define a detailed execution template for each pipeline.

Resolution:

R01-003 must create migration execution templates.

### Gap 2 - Active Queue Transition

The current active scientific queue is paused at:

```text
A04.0-005 - SNRI_SOURCE_VALIDATION
```

Resolution:

R01-003 must decide whether to resume A04.0-005 first or migrate it into `SourceValidationPipeline[DrugClass=SNRIs]`.

### Gap 3 - Queue ID Policy Needs Expansion

`CQ-R01-002` exists, but future pipeline executions need a consistent naming pattern.

Resolution:

R01-003 should define queue IDs for pipeline executions.

### Gap 4 - Historical vs Active Roadmap Labeling

The repository must clearly mark the old roadmap as historical or mapped, not deleted.

Resolution:

R01-003 should propose labels and control-file updates.

## Risk Assessment

| Risk | Severity | Mitigation |
| --- | --- | --- |
| Over-compression hides class-specific complexity | Medium | Preserve safety and class-specific gates. |
| Confusion between old mission IDs and new pipeline executions | Medium | Use queue IDs and mapping tables. |
| Premature migration disrupts A04.0 | Low | Pause migration until R01-003 is approved. |
| Runtime accidentally enabled | Critical | Runtime Eligibility Gate remains explicit and blocked. |

## Final Declaration

The compressed model has no critical gap, but it is not executable until R01-003 defines the migration execution plan.
