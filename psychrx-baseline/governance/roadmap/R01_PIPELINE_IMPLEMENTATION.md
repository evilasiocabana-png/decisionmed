# R01 Pipeline Implementation

## Mission

R01-004 - ROADMAP_PIPELINE_IMPLEMENTATION.

## Queue

SEQ: 000129

Queue ID: CQ-R01-004

## Purpose

Activate the parameterized pipeline execution model planned by R01-003 and decide how the paused scientific mission A04.0-005 resumes.

This mission is governance-only.

It does not create scientific content, validate corpus content, interpret evidence, alter runtime behavior, prescribe, recommend treatment or enable clinical decision automation.

## Decision

The compressed roadmap model is approved for operational use.

Future repeated scientific population work should use parameterized pipelines instead of duplicating full class-specific roadmap programs.

Historical mission IDs remain valid as traceability aliases.

## Active Pipeline Model

The following pipeline families become active execution models:

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

Pipeline executions must declare:

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

## Active Queue Transition

The paused historical mission:

```text
A04.0-005 - SNRI_SOURCE_VALIDATION
```

is resumed through:

```text
ValidationPipeline[DrugClass=SNRIs]
```

Execution ID:

```text
PIPE-A04-0-SNRI-VALIDATION-001
```

Historical alias:

```text
A04.0-005 - SNRI_SOURCE_VALIDATION
```

## Legacy Labeling

Class-specific future branches A05 through A15 remain preserved as historical roadmap artifacts.

They are marked operationally as:

```text
MAPPED_TO_PARAMETERIZED_PIPELINE
```

They are not deleted, renamed, moved or deprecated as documents.

## Gate Rules

Pipeline execution must stop when any of the following are missing:

- source corpus;
- source IDs;
- metadata normalization;
- validation gate;
- editorial status;
- traceability map;
- publication status;
- runtime eligibility decision.

Draft scientific objects remain runtime-ineligible.

## Prohibitions

Pipeline activation does not authorize:

- prescription;
- therapeutic recommendation;
- clinical runtime consumption of draft knowledge;
- dose guidance;
- medication selection;
- clinical decision automation;
- evidence grading without source traceability;
- scientific content population without the appropriate pipeline mission.

## Batch Result

R01-004 activates the operational roadmap migration and releases the next mission as a pipeline execution:

```text
PIPE-A04-0-SNRI-VALIDATION-001
ValidationPipeline[DrugClass=SNRIs]
Historical alias: A04.0-005 - SNRI_SOURCE_VALIDATION
```

## Final Declaration

The R01 compressed roadmap is now the active operational execution model for repeated future scientific work. Historical mission IDs remain preserved for traceability.
