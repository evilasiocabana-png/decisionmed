# ADR 0045 - A03 Phase 3 Refactored Drug Scientific Modeling

## Status

Accepted.

## Date

2026-06-30

## Context

Program A03 entered Phase 3 after Phase 1 and Phase 2 established the SSRI portfolio, registries, directories, templates, traceability and editorial status framework.

The initial Phase 3 queue contained granular missions for identification, nomenclature, classification and metadata. That structure overlapped with responsibilities already covered by Phase 1 and Phase 2.

The CTO decision is to refactor Phase 3 so each mission represents a scientific domain from the Psychopharmacological Agent Model instead of repeating infrastructure.

## Decision

Phase 3 is now governed as Drug Scientific Modeling.

The Phase 3 Sprint 01 sequence is:

```text
A03-021 - Scientific Drug Profile Initialization
A03-022 - Mechanism of Action Modeling
A03-023 - Receptor and Neurotransmitter Modeling
A03-024 - Pharmacokinetic Modeling
A03-025 - Pharmacodynamic Modeling
A03-026 - Indication Modeling
A03-027 - Posology Modeling
A03-028 - Contraindication Modeling
A03-029 - Safety Modeling
A03-030 - Phase 3 Sprint 1 Baseline
```

A03-021 replaces the previous narrower `DRUG_IDENTIFICATION` interpretation. It creates only the structural scientific profile shell for each core SSRI.

## Alternatives Considered

- Keep the granular identification, nomenclature, classification and metadata missions.
- Continue with the old queue and reconcile overlap later.
- Refactor Phase 3 before creating scientific profile artifacts.

## Rationale

The refactored sequence prevents duplicated registries, repeated metadata work and conflicting responsibility boundaries. It also aligns Program A03 with the official Psychopharmacological Agent Model.

## Impact

- `NEXT_MISSION.md` must point from A03-021 to A03-022 after profile initialization.
- Project control documents must describe A03-021 as Scientific Drug Profile Initialization.
- A03-022 becomes the first mission allowed to model mechanism of action.
- Clinical recommendation, prescription and runtime consumption remain prohibited.

## Risks

- Existing prompt drafts may still reference the older granular sequence.
- Agents may confuse profile initialization with scientific content extraction.
- The project must enforce source-level traceability before any populated scientific value is published.

## Documents Affected

- `governance/execution/NEXT_MISSION.md`
- `governance/execution/PROJECT_STATUS.md`
- `PROJECT_STATUS.md`
- `governance/execution/PROJECT_PROGRESS.md`
- `governance/execution/PROJECT_TREE.md`
- `docs/PROJECT_DEPENDENCIES.md`
- `governance/execution/PROJECT_INDEX.md`
- `docs/PROGRAM_A03_STATUS.md`
- `docs/PROGRAM_A03_PROGRESS.md`
- `docs/000_MANIFEST.md`

## Future Review Criteria

Review this ADR before A03-030. If Phase 3 creates duplicated registries or scientific values without field-level traceability, the phase must be paused for correction.

## Declaration Final

Phase 3 is officially refactored into scientific-domain modeling. The next executable unit is the controlled creation of structural Drug Profile shells, not clinical recommendation or runtime behavior.
