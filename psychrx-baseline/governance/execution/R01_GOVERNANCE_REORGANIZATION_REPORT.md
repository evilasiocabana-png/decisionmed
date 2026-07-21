# R01 Governance Reorganization Report

## Mission

R01 - Governance Repository Reorganization.

## Scope

This mission reorganized governance documents only. It did not alter functional code, clinical runtime, algorithms, tests, scientific content, schemas, safety rules or knowledge base data.

## Files Created

- `governance/README.md`
- `governance/execution/EXECUTION_STATE.json`
- `governance/execution/BLOCKED_ITEMS.md`
- `governance/execution/GATES.md`
- `governance/execution/R01_GOVERNANCE_REORGANIZATION_REPORT.md`

## Folders Created

- `governance/`
- `governance/constitution/`
- `governance/manifesto/`
- `governance/adr/`
- `governance/roadmap/`
- `governance/programs/`
- `governance/missions/`
- `governance/execution/`

## Files Moved

Governance files were moved with `git mv` into:

- `governance/constitution/`
- `governance/manifesto/`
- `governance/adr/docs_adr/`
- `governance/roadmap/`
- `governance/programs/`
- `governance/missions/`
- `governance/execution/`

Detailed move history is preserved in Git.

## Duplicate Files Found

- root `PROJECT_STATUS.md` and former `governance/execution/PROJECT_STATUS.md`
- root `NEXT_MISSION.md` and former `governance/execution/NEXT_MISSION.md`

The root variants were preserved with `.root.md` suffixes under `governance/execution/`.

## Decisions Taken

- `governance/execution/PROJECT_EXECUTION_CONTEXT.md` was treated as the clearest current execution-state source.
- `EXECUTION_STATE.json` was initialized with Program A04 active and A04-009 blocked.
- The outdated root `NEXT_MISSION.md` was not overwritten; it was preserved as historical input.

## Active Blockers

- `A04_SOURCE_SECTION_SELECTION_REQUIRED`

A04-009 cannot start until selected and reviewable SNRI source sections exist.

## Final Governance State

The operational source of truth is now:

`governance/execution/EXECUTION_STATE.json`

Current status:

```text
PROGRAM A04 - Scientific Content Population: SNRIs
Blocked - Source Section Selection Required
A04-009 - SNRI_MECHANISM_POPULATION_DRAFT blocked
```

## Validations

Executed:

- `python -m unittest discover -s tests -t .`

Result:

- 149 tests passed.

Documentation path check:

- Remaining governance-like file in `docs/`: `docs/PROGRAM_07_BASELINE.md`.
- This file is a compatibility pointer required by existing tests.
- Canonical Program 07 baseline location is `governance/programs/PROGRAM_07_BASELINE.md`.

Functional code modification check:

- No functional code files were modified.

## Recommended Next Steps

1. Review whether root pointer files should be added for GitHub discoverability.
2. Update remaining internal references from old `docs/` governance paths to `governance/`.
3. Do not execute A04-009 until the A04 source section selection gate is resolved.
