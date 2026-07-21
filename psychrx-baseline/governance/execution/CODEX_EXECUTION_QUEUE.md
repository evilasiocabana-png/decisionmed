# Codex Execution Queue

## Purpose

Provide a global sequential reference for Codex executions across all PsychRx programs.

The queue identifier does not replace mission IDs. It makes the execution order searchable across programs, phases and tracks.

## Format

```text
SEQ: 000125
QUEUE ID: CQ-000125
Mission: A04.0-004
```

## Current Entries

| SEQ | Queue ID | Mission | Status |
| --- | --- | --- | --- |
| 000125 | CQ-000125 | A04.0-004 - SNRI_SOURCE_METADATA_NORMALIZATION | completed |
| 000126 | CQ-R01-001 | R01-001 - ROADMAP_REFACTORING_TO_200_MISSION_MODEL | completed |
| 000127 | CQ-R01-002 | R01-002 - ROADMAP_REFACTORING_REVIEW | completed |
| 000128 | CQ-R01-003 | R01-003 - ROADMAP_MIGRATION_EXECUTION_PLAN | completed |
| 000129 | CQ-R01-004 | R01-004 - ROADMAP_PIPELINE_IMPLEMENTATION | completed |
| 000130 | PIPE-A04-0-SNRI-VALIDATION-001 | ValidationPipeline[DrugClass=SNRIs] / A04.0-005 - SNRI_SOURCE_VALIDATION | completed |
| 000131 | CQ-A04-0-006 | A04.0-006 - SNRI_EDITORIAL_REGISTRATION | completed |
| 000132 | CQ-A04-0-007 | A04.0-007 - SNRI_CORPUS_PUBLICATION | completed |
| 000133 | CQ-A04-0-008 | A04.0-008 - PROGRAM_A04_0_COMPLETION_GATE | completed |
| 000134 | CQ-A04-003 | A04-003 - SNRI_SOURCE_CORPUS_INTAKE_RECONCILIATION | completed |
| 000135 | CQ-A04-004 | A04-004 - SNRI_POPULATION_EXECUTION_PLAN | completed |
| 000136 | CQ-A04-005 | A04-005 - SNRI_PROFILE_SHELLS | completed |
| 000137 | CQ-A04-006 | A04-006 - SNRI_SOURCE_ANCHOR_PLAN | completed |
| 000138 | CQ-A04-007 | A04-007 - SNRI_FIELD_TRACEABILITY_MATRIX | completed |
| 000139 | CQ-A04-008 | A04-008 - SNRI_EXTRACTION_GATES | completed_with_blocker |
| 000140 | CQ-A04-008A | A04-008A - SNRI_SOURCE_ANCHOR_FINALIZATION | completed |
| 000141 | CQ-A04-008B | A04-008B - SNRI_EXTRACTION_PROTOCOL_PACKAGE | completed_with_blocker |
| 000142 | CQ-A04-008C | A04-008C - SNRI_SOURCE_SECTION_SELECTION_OR_BLOCKER | completed_with_blocker |
| 000143 | CQ-A04-008D | A04-008D - SNRI_SOURCE_TEXT_ACQUISITION_PACKAGE | completed |
| 000144 | CQ-A04-008E | A04-008E - SNRI_SOURCE_SECTION_LOCATOR_PLAN | completed |
| 000145 | CQ-A04-008F | A04-008F - SNRI_SOURCE_SECTION_SELECTION_GATE | completed_with_blocker |

## Rules

- `SEQ` is global for the whole project.
- `QUEUE ID` is permanent.
- Queue numbers never restart inside a program.
- Queue numbers do not override State Driven Protocol.
- If a queued mission conflicts with `NEXT_MISSION.md`, the repository state prevails.

## Final Declaration

The Codex Execution Queue is an auxiliary locator. The official executable state remains `NEXT_MISSION.md`, `NEXT_BLOCK.md` and `PROJECT_EXECUTION_CONTEXT.md`.
