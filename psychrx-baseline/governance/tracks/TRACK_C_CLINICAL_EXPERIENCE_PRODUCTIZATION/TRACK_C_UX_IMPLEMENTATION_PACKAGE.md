# Track C UX Implementation Package

## Status

Created as governed technical implementation package.

## Objective

Convert Track C from product and UX governance artifacts into a controlled read-only UX implementation package for the PsychRx Clinical Workspace.

The package authorizes presentation-layer implementation only. It does not authorize clinical runtime activation, prescribing, therapeutic recommendation, dose suggestion, autonomous diagnosis or patient-specific medication selection.

## Scope

Authorized implementation scope:

- consultation-first screen organization;
- current patient state intake surface;
- symptom capture UI;
- clinical stability UI;
- safety gap visibility;
- current treatment context UI;
- objective and follow-up organization;
- technical governance reference kept secondary;
- responsive read-only presentation;
- tests that verify presentation contracts.

## Dependencies Read

- `governance/execution/EXECUTION_STATE.json`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/NEXT_BLOCK.md`
- `governance/execution/NEXT_MISSION.md`
- `governance/tracks/TRACK_C_CLINICAL_EXPERIENCE_PRODUCTIZATION/TRACK_C_EXECUTION_PLAN.md`
- `governance/tracks/TRACK_C_CLINICAL_EXPERIENCE_PRODUCTIZATION/TRACK_C_COMPLETION_REPORT.md`
- `governance/tracks/TRACK_C_CLINICAL_EXPERIENCE_PRODUCTIZATION/TRACK_C_PROGRAM_INDEX.json`

## Implementation Rule

The user-facing interface must answer first:

```text
Como esta este paciente hoje?
```

The first screen must prioritize:

1. patient speech;
2. current symptoms;
3. observed changes;
4. clinical stability;
5. current treatment context;
6. safety gaps;
7. objectives;
8. follow-up.

Conceptual documentation, roadmap, widget library and governance material must not dominate the consultation surface.

## Explicitly Forbidden

- prescription;
- therapeutic recommendation;
- dose suggestion;
- autonomous diagnosis;
- patient-specific medication selection;
- clinical runtime decisioning;
- UI rules that decide conduct;
- source-free clinical claims;
- runtime consumption of scientific knowledge.

## Authorized Files

- `interfaces/web/static/index.html`
- `interfaces/web/static/styles.css`
- `interfaces/web/static/app.js` only if needed for presentation behavior
- `tests/interfaces/test_web_app.py`
- Track C governance package files under `governance/tracks/TRACK_C_CLINICAL_EXPERIENCE_PRODUCTIZATION/`
- execution status files under `governance/execution/`

## Acceptance Criteria

- The Clinical Workspace opens as a practical consultation surface.
- The first user task is the current patient state, not diagnosis.
- Technical and governance content is secondary and collapsible.
- The UI remains read-only and non-prescriptive.
- No clinical runtime behavior is enabled.
- No recommendation, prescription, dose or medication selection is introduced.
- Tests pass.

## Completion Status

Package created. Initial read-only consultation surface refactor executed in the web interface.

