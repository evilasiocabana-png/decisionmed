# Project Duplications - PsychRx

## Date

2026-07-01

## Summary

The project contains historical duplication. Most duplication is not harmful yet, but it increases navigation cost.

## Identified Duplications

### Numbering Duplications

Early documentation contains repeated numbers, especially:

- `007_ARQUITETURA_DO_MVP.md`
- `007_MOTOR_DE_ESTABILIZACAO.md`
- multiple `008_*` documents;
- multiple `009_*` documents;
- multiple `010_*` documents;
- multiple `011_*` documents;
- multiple `012_*` documents;
- multiple `013_*` documents;
- multiple `014_*` documents;
- repeated `031_*` and `044_*` themes.

These are historical and should not be renumbered without ADR.

### Baseline Duplications

Several programs have both numbered baseline documents and unnumbered baseline documents.

Examples:

- `177_PROGRAM_07_BASELINE.md` and `PROGRAM_07_BASELINE.md`.
- `199_PROGRAM_08_BASELINE.md` and `PROGRAM_08_BASELINE.md`.
- similar patterns across Programs 09-17.

### Status Duplications

There is both:

- root `PROJECT_STATUS.md`;
- `governance/execution/PROJECT_STATUS.md`.

This is intentional but requires synchronization discipline.

### Historical Gate Language

Some historical documents preserve superseded next mission references. These have mostly been corrected or superseded, but the pattern should be watched.

## Not Duplications

The following are parallel control artifacts and should remain:

- `PROJECT_TREE.md`
- `PROJECT_INDEX.md`
- `PROJECT_PROGRESS.md`
- `PROJECT_DEPENDENCIES.md`
- `NEXT_MISSION.md`

## Recommendation

Do not delete or renumber now.

Instead:

1. create a future `DOCUMENT_SUPERSEDENCE_REGISTER.md`;
2. mark obsolete next-mission statements as historical;
3. preserve all ADR-governed history.

