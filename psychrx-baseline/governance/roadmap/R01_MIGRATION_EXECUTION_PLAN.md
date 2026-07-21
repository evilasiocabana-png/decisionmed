# R01 Migration Execution Plan

## Mission

R01-003 - ROADMAP_MIGRATION_EXECUTION_PLAN.

## Purpose

Define the official execution plan for migrating PsychRx from the historical mission-by-mission roadmap to a compact model based on reusable frameworks and parameterized pipelines.

This document is a migration plan only.

It does not migrate files, delete documentation, alter clinical architecture, create scientific content, activate runtime behavior or change any ADR.

## Migration Principle

The new roadmap must preserve:

- all governance gates;
- all safety prohibitions;
- all scientific traceability requirements;
- all existing historical artifacts;
- all completed baselines;
- all paused scientific work;
- all runtime restrictions.

Compression is operational only. It reduces duplicated future execution structure without erasing historical work.

## Migration Phases

### Phase 1 - Freeze Current Roadmap

Record the current roadmap as historical baseline.

Outputs:

- current roadmap state preserved;
- active and paused missions identified;
- A04.0-005 kept paused, not cancelled.

### Phase 2 - Create Generic Frameworks

Define reusable framework missions for governance, clinical architecture, software platform, knowledge framework, clinical workspace and runtime shell.

Outputs:

- framework mission ranges confirmed;
- non-compressible governance gates preserved.

### Phase 3 - Create Parameterized Pipelines

Define reusable scientific pipelines that receive parameters instead of creating one full program per drug class.

Outputs:

- canonical pipeline list;
- parameter schema;
- gate map for each pipeline.

### Phase 4 - Migrate Existing Programs

Map historical programs to the new pipeline model.

Outputs:

- program conversion matrix;
- status labels: historical, mapped, migrated, paused, superseded by pipeline.

### Phase 5 - Validate Equivalence

Confirm that the new model preserves the old model without functional, scientific, architectural or traceability loss.

Outputs:

- equivalence validation;
- gap analysis;
- CTO recommendation.

### Phase 6 - Deprecate Old Roadmap Operationally

Mark duplicated future program templates as legacy for execution purposes.

No file is deleted.

Outputs:

- deprecation plan;
- no deletion policy;
- legacy label rules.

### Phase 7 - Publish New Roadmap

Publish the compressed model as the active execution roadmap after R01-004 approval.

Outputs:

- active roadmap switch;
- updated NEXT_MISSION;
- updated project state.

## Pipelines To Deploy

- CorpusPipeline
- MetadataPipeline
- ValidationPipeline
- DrugPortfolioPipeline
- ScientificExtractionPipeline
- MechanismPipeline
- PKPipeline
- PDPipeline
- SafetyPipeline
- InteractionPipeline
- EvidencePipeline
- PublicationPipeline
- RuntimeEligibilityPipeline

## Canonical Parameters

- DrugClass
- DrugList
- Corpus
- CorpusPath
- KnowledgeBasePath
- GuidelineSet
- EvidenceSet
- RegulatoryRegion
- Language
- PublicationLevel
- ScientificStatus
- RuntimeEligibility

## Active Queue Preservation

The paused mission remains:

```text
A04.0-005 - SNRI_SOURCE_VALIDATION
```

R01-003 does not resume it.

R01-004 must decide whether A04.0-005 resumes under its historical ID or under the new parameterized pipeline execution ID.

## Migration Decision Needed In R01-004

R01-004 must decide:

1. whether the pipeline model becomes active;
2. whether A04.0-005 is resumed directly or converted to ValidationPipeline[DrugClass=SNRIs];
3. how historical mission IDs and pipeline execution IDs coexist;
4. whether old roadmap branches are marked legacy or mapped.

## Validation Answers

Does the new roadmap cover 100% of the old roadmap?

Yes, conditionally. R01-002 found no critical loss, and this plan preserves all gates and historical artifacts.

Is there functional loss?

No functional loss is planned. Future execution units are compressed but capabilities are retained.

Is there architectural loss?

No. Foundational, workspace, runtime, safety, evidence and release governance remain represented.

Is there scientific loss?

No. Scientific corpus, extraction, review, evidence, QA and publication gates remain explicit.

Is there documentary loss?

No. Existing documents remain historical artifacts.

Is there traceability loss?

No. Pipeline execution must preserve source IDs, anchors, editorial status and runtime eligibility status.

## Final Declaration

R01-003 defines how migration should occur. It does not execute the migration. R01-004 is required before the compressed roadmap can become the active operational model.
