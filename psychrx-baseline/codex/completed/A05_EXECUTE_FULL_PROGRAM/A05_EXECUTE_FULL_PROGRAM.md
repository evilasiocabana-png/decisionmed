# Codex Mission - Execute Full Program A05

## Repository

evilasiocabana-png/PsychRx

## Mission

Execute the full authorized Program A05 from the current next mission through the final program gate.

## Required Reading

Before making changes, read:

1. `governance/execution/NEXT_MISSION.md`
2. `governance/execution/NEXT_BLOCK.md`
3. `governance/programs/A05_PROGRAM_EXECUTION_PLAN.md`
4. `governance/execution/PROJECT_EXECUTION_CONTEXT.md`
5. `governance/MASTER_ROADMAP.md`

## Starting Point

Start at:

```text
A05-001 - NDRI_PROGRAM_INITIALIZATION
```

## Continuous Execution Authorization

Execute all remaining missions in Program A05 in order, without stopping for separate user confirmation after each mission, provided every gate passes.

Program sequence:

```text
A05-001 - NDRI_PROGRAM_INITIALIZATION
A05-002 - NDRI_OFFICIAL_PORTFOLIO
A05-003 - NDRI_SOURCE_DISCOVERY
A05-004 - NDRI_SOURCE_CORPUS_INTAKE
A05-005 - NDRI_SOURCE_VALIDATION
A05-006 - NDRI_POPULATION_EXECUTION_PLAN
A05-007 - NDRI_PROFILE_SHELLS
A05-008 - NDRI_FIELD_TRACEABILITY_MATRIX
A05-009 - NDRI_EXTRACTION_GATES
A05-010 - NDRI_SOURCE_SECTION_SELECTION
A05-011 - NDRI_SOURCE_TEXT_EXTRACTION
A05-012 - NDRI_CONTENT_POPULATION
A05-013 - NDRI_DRAFT_EDITORIAL_REVIEW
A05-014 - NDRI_INTERNAL_PUBLICATION
A05-015 - NDRI_TRACEABILITY_AUDIT
A05-016 - NDRI_PROGRAM_COMPLETION_REPORT
A05-017 - A05_PROGRAM_GATE_VALIDATION
```

## Stop Conditions

Stop immediately and register a blocker if any of the following occur:

- tests fail;
- traceability gap is found;
- required source material is missing;
- JSON is invalid;
- scope conflict occurs;
- an attempted change would enable runtime use;
- an attempted change would create prescription, recommendation, dose suggestion, or patient-facing clinical guidance;
- a gate fails.

## Scope Boundaries

Allowed:

- create A05 governance files;
- create source discovery and corpus metadata files;
- create traceability matrices;
- create extraction gates;
- create exact source-text records only when selected sections are reviewable;
- populate only authorized scientific fields from exact source-text records;
- mark insufficient fields as `UNRESOLVED`;
- publish internal non-runtime artifacts;
- audit traceability;
- update project state and logs after each accepted mission.

Forbidden:

- prescription;
- therapeutic recommendation;
- dose suggestion;
- patient-specific medication selection;
- clinical runtime eligibility;
- active runtime consumption;
- unsourced claims;
- skipping gates;
- starting A06 before A05 final gate.

## Required Updates

After each accepted mission, update relevant governance files, including when present:

- `governance/execution/NEXT_MISSION.md`
- `governance/execution/NEXT_BLOCK.md`
- `governance/execution/PROJECT_EXECUTION_CONTEXT.md`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/PROJECT_PROGRESS.md`
- `governance/execution/EXECUTION_LOG.md`
- `governance/MASTER_ROADMAP.md`

## Validation

Run the repository test suite:

```text
python -m unittest discover -s tests -t .
```

If tests cannot be run in the environment, document that limitation explicitly and do not claim tests passed.

## Final Output

When complete, report:

1. missions executed;
2. files created;
3. files modified;
4. tests run and results;
5. blockers, if any;
6. traceability status;
7. final A05 gate status;
8. next authorized action.
