# R01 Pipeline Parameterization Plan

## Mission

R01-001 - ROADMAP_REFACTORING_TO_200_MISSION_MODEL.

## Generic Parameters

All reusable scientific pipelines must support:

- `DrugClass`
- `DrugList`
- `CorpusPath`
- `KnowledgeBasePath`
- `SourceSet`
- `RegulatoryRegion`
- `PublicationStatus`
- `EditorialStatus`
- `RuntimeEligibility`

## Pipelines

### 1. Corpus Pipeline

Creates or updates a scientific corpus for a drug class.

Parameters:

```text
DrugClass
DrugList
CorpusPath
SourceSet
RegulatoryRegion
```

### 2. Metadata Pipeline

Normalizes administrative metadata.

### 3. Source Validation Pipeline

Validates source IDs, paths, manifests, duplicates and missing metadata.

### 4. Drug Portfolio Pipeline

Creates metadata-only portfolio records.

### 5. Scientific Extraction Pipeline

Extracts source-grounded claims only after corpus and extraction gates.

### 6. Mechanism Pipeline

Structures mechanism claims with source anchors.

### 7. Pharmacokinetic Pipeline

Structures PK claims with source anchors.

### 8. Pharmacodynamic Pipeline

Structures PD claims with source anchors.

### 9. Indication Pipeline

Structures indication claims without creating recommendations.

### 10. Posology Pipeline

Structures posology information without prescribing.

### 11. Contraindication Pipeline

Structures contraindication knowledge for later safety review.

### 12. Safety Pipeline

Structures adverse effects, warnings and monitoring metadata.

### 13. Interaction Pipeline

Structures interaction knowledge after source validation.

### 14. Evidence Integration Pipeline

Connects scientific objects to evidence metadata.

### 15. Publication Pipeline

Moves reviewed objects from draft to publication candidate.

## Command Examples

```text
EXECUTE PIPELINE CorpusPipeline DrugClass=SNRIs
EXECUTE PIPELINE DrugClassPopulation DrugClass=SNRIs
EXECUTE PIPELINE MechanismPipeline DrugClass=SSRIs
EXECUTE PIPELINE PKPipeline DrugClass=SNRIs
EXECUTE UNTIL GATE
EXECUTE UNTIL BLOCK
VERIFY PIPELINE STATE
REPORT PIPELINE STATUS
```

## Final Declaration

Parameterized pipelines allow one framework to execute safely across multiple drug classes without duplicating roadmap structure.
