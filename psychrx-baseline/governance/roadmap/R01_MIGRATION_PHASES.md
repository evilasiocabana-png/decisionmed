# R01 Migration Phases

## Mission

R01-003 - ROADMAP_MIGRATION_EXECUTION_PLAN.

## Phase Overview

| Phase | Name | Purpose | Output | Execution Status |
| --- | --- | --- | --- | --- |
| 1 | Freeze Current Roadmap | Preserve current state before migration | Historical baseline | Planned |
| 2 | Generic Frameworks | Define reusable non-drug-class program frameworks | Framework map | Planned |
| 3 | Parameterized Pipelines | Define reusable scientific pipelines | Pipeline model | Planned |
| 4 | Program Migration | Map old programs to pipelines | Conversion matrix | Planned |
| 5 | Equivalence Validation | Verify no loss | Review package | Planned |
| 6 | Legacy Deprecation | Mark duplicated plans as legacy without deletion | Deprecation labels | Planned |
| 7 | Roadmap Publication | Publish active compressed roadmap | Active roadmap | Blocked until R01-004 |

## Phase 1 - Freeze Current Roadmap

Required actions:

- record current active program;
- record current paused scientific mission;
- preserve all existing project status files;
- prevent accidental deletion of legacy documents.

Completion criteria:

- current state is reproducible from repository documents;
- paused mission A04.0-005 remains visible.

## Phase 2 - Generic Frameworks

Required actions:

- preserve governance framework;
- preserve clinical architecture framework;
- preserve software platform framework;
- preserve clinical workspace framework;
- preserve runtime shell framework.

Completion criteria:

- no foundational capability disappears;
- non-compressible safety and release gates remain explicit.

## Phase 3 - Parameterized Pipelines

Required actions:

- define pipeline list;
- define pipeline inputs and outputs;
- define required parameters;
- define gate rules per pipeline.

Completion criteria:

- each repeated class-specific program maps to one or more pipelines;
- each pipeline has explicit stop conditions.

## Phase 4 - Program Migration

Required actions:

- mark historical programs;
- map future drug class programs to pipeline executions;
- preserve completed execution reports;
- preserve active blocked reports.

Completion criteria:

- every original program has a status;
- no active or paused work is lost.

## Phase 5 - Equivalence Validation

Required actions:

- compare original and compressed roadmap;
- verify clinical architecture;
- verify scientific governance;
- verify gates;
- verify traceability.

Completion criteria:

- no critical gaps;
- migration recommendation ready for R01-004.

## Phase 6 - Legacy Deprecation

Required actions:

- label duplicated future roadmaps as legacy for execution;
- keep historical documents accessible;
- define replacement pipeline.

Completion criteria:

- old documents are preserved;
- agents know which model is active.

## Phase 7 - Roadmap Publication

Required actions:

- update project state;
- update NEXT_MISSION;
- update PROJECT_TREE;
- publish compressed roadmap as active model.

Completion criteria:

- R01-004 approval exists;
- active execution lane is unambiguous.

## Final Declaration

The migration is a controlled phase transition. It must not be treated as a file cleanup or roadmap deletion.
