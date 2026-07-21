# R01 Pipeline Deployment Plan

## Mission

R01-003 - ROADMAP_MIGRATION_EXECUTION_PLAN.

## Purpose

Define how reusable pipelines will replace duplicated class-specific roadmap branches.

## Pipeline Families

| Pipeline | Scope | Typical Parameters | Required Gate |
| --- | --- | --- | --- |
| CorpusPipeline | Scientific source corpus creation | DrugClass, CorpusPath, SourceSet, RegulatoryRegion, Language | Corpus Gate |
| MetadataPipeline | Administrative source metadata | DrugClass, CorpusPath, Language | Metadata Gate |
| ValidationPipeline | Structural source validation | DrugClass, CorpusPath | Source Validation Gate |
| DrugPortfolioPipeline | Metadata-only drug portfolio | DrugClass, DrugList, KnowledgeBasePath | Drug Portfolio Gate |
| ScientificExtractionPipeline | Source-grounded extraction | DrugClass, Corpus, EvidenceSet | Extraction Protocol Gate |
| MechanismPipeline | Mechanism claims | DrugClass, DrugList, SourceAnchors | Scientific Review Gate |
| PKPipeline | Pharmacokinetic claims | DrugClass, DrugList, SourceAnchors | Scientific Review Gate |
| PDPipeline | Pharmacodynamic claims | DrugClass, DrugList, SourceAnchors | Scientific Review Gate |
| SafetyPipeline | Safety warnings and monitoring metadata | DrugClass, DrugList, SourceAnchors | Safety Review Gate |
| InteractionPipeline | Interaction metadata | DrugClass, DrugList, SourceAnchors | Interaction Safety Gate |
| EvidencePipeline | Evidence binding and traceability | DrugClass, EvidenceSet | Evidence Gate |
| PublicationPipeline | Internal publication candidate | DrugClass, PublicationLevel | Editorial Publication Gate |
| RuntimeEligibilityPipeline | Future runtime eligibility review | DrugClass, ScientificStatus | Runtime Eligibility Gate |

## Deployment Sequence

1. Deploy CorpusPipeline.
2. Deploy MetadataPipeline.
3. Deploy ValidationPipeline.
4. Deploy DrugPortfolioPipeline.
5. Deploy ScientificExtractionPipeline.
6. Deploy MechanismPipeline.
7. Deploy PKPipeline.
8. Deploy PDPipeline.
9. Deploy SafetyPipeline.
10. Deploy InteractionPipeline.
11. Deploy EvidencePipeline.
12. Deploy PublicationPipeline.
13. Keep RuntimeEligibilityPipeline locked until clinical governance releases it.

## Command Form

The future command form should be:

```text
EXECUTE PIPELINE <PipelineName> DrugClass=<DrugClass> Phase=<PhaseName>
```

Example:

```text
EXECUTE PIPELINE ValidationPipeline DrugClass=SNRIs Phase=SourceValidation
```

## Stop Conditions

Every pipeline must stop when:

- a gate is missing;
- a source is unavailable;
- traceability is incomplete;
- JSON validation fails;
- tests fail;
- a clinical recommendation would be created;
- runtime eligibility would be implied without approval.

## Active SNRI Transition

The first candidate deployment is:

```text
ValidationPipeline[DrugClass=SNRIs]
```

It corresponds to paused historical mission:

```text
A04.0-005 - SNRI_SOURCE_VALIDATION
```

## Final Declaration

Pipeline deployment must be parameterized, gated and reversible. It must not bypass the state-driven execution protocol.
