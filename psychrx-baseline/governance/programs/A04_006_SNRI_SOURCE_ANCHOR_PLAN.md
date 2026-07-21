# A04-006 - SNRI Source Anchor Plan

## Program

PROGRAM A04 - Scientific Content Population: SNRIs.

## Mission

A04-006 - SNRI_SOURCE_ANCHOR_PLAN.

## Objective

Create the SNRI source anchor plan before any scientific field population.

This mission defines future anchor slots only.

It does not create definitive anchors.

It does not extract source text.

It does not populate scientific fields.

## Inputs

- `ScientificCorpus/SNRIs/Manifest/SNRI_SOURCE_CATALOG.json`
- `ScientificCorpus/SNRIs/Indexes/MASTER_CORPUS_INDEX.json`
- `KnowledgeBase/SNRIs/ProfileShells/SNRI_PROFILE_SHELL_REGISTRY.json`
- `KnowledgeBase/SNRIs/*/Profile/PROFILE_SHELL.json`

## Output

- `KnowledgeBase/SNRIs/Traceability/SNRI_SOURCE_ANCHOR_PLAN.json`

## Drug Scope

- Venlafaxine.
- Desvenlafaxine.
- Duloxetine.
- Levomilnacipran.
- Milnacipran.

## Planned Anchor Slots

The plan defines future anchor slots for:

- identification;
- mechanism;
- pharmacokinetics;
- pharmacodynamics;
- indications;
- posology;
- contraindications;
- safety;
- evidence.

Each slot contains only candidate source IDs and administrative anchor status.

## Anchor Status

All planned slots remain:

```text
planned_pending_source_section_selection
```

No definitive source anchor was created.

## Runtime Eligibility

```text
not_eligible
```

## Explicit Non-Actions

No source text was interpreted.

No scientific claim was extracted.

No drug profile field was populated.

No evidence was graded.

No therapeutic recommendation was created.

No prescription, dose guidance or medication selection was created.

No runtime object was created.

## Gate Impact

A04-006 prepares A04-007.

A04-007 must build the field traceability matrix before extraction can begin.

## Next Mission

A04-007 - SNRI_FIELD_TRACEABILITY_MATRIX.

## Final Declaration

The SNRI Source Anchor Plan exists as an administrative planning artifact only. Scientific population remains blocked until the field traceability matrix and extraction gates are completed.

