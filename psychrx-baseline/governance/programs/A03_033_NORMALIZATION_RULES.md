# A03-033 - Normalization Rules

## Program

Program A03 - Scientific Content Population: SSRIs.

## Phase

Phase 3.5 - Scientific Knowledge Acquisition.

## Mission

Define how extracted scientific claims are normalized before entering knowledge objects.

## Normalization Scope

Normalization may standardize:

- terminology;
- drug identifiers;
- source identifiers;
- field names;
- units;
- routes;
- population labels;
- jurisdiction labels;
- evidence source references.

## Prohibited Normalization

Normalization must not:

- infer missing clinical meaning;
- convert text into recommendation;
- resolve conflicts without review;
- add unstated indication;
- add unstated contraindication;
- create dose guidance;
- create safety alert.

## Conflict Handling

Conflicts must be marked as:

- `conflict_candidate`;
- `requires_review`;
- `source_disagreement`;
- `jurisdictional_difference`;
- `version_difference`.

## Next Mission

`A03-034 - SCIENTIFIC_REVIEW_WORKFLOW`

## Declaration Final

A03-033 defines normalization as controlled semantic formatting, not clinical interpretation.
