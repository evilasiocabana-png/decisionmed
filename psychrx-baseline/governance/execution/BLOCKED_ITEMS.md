# Blocked Items

## Resolved Blocker

### A04_SOURCE_SECTION_SELECTION_REQUIRED

Status: resolved for mechanism field only by A04-008G.

This blocker is historical for the mechanism field and must not override `governance/PROJECT_STATE.md`, `EXECUTION_STATE.json`, `NEXT_MISSION.md`, or `NEXT_BLOCK.md`.

Program A04 is active and A04-009 has been completed as a non-runtime mechanism draft structure.

A04-010 is released only for `SNRI_MECHANISM_SOURCE_TEXT_EXTRACTION`.

The following traceability chain now exists for mechanism-field section selection:

```text
Specific source
-> Specific section
-> Psychopharmacological field
-> Reviewable content
-> Unresolved draft mechanism slot
```

The chain is recorded in:

- `KnowledgeBase/SNRIs/Traceability/SNRI_SOURCE_SECTION_SELECTION.json`
- `KnowledgeBase/SNRIs/Traceability/SNRI_SOURCE_SECTION_SELECTION_GATE.json`
- `KnowledgeBase/SNRIs/Traceability/SNRI_MECHANISM_DRAFT_TRACEABILITY.json`
- `KnowledgeBase/SNRIs/ScientificContent/SNRI_MECHANISM_OF_ACTION_DRAFT.md`
- `governance/missions/PROGRAM_A04_SNRI_SCIENTIFIC_CONTENT/PHASE_SOURCE_SECTION_SELECTION/A04-008G_SNRI_SOURCE_SECTION_SELECTION_EXECUTION.md`

## Active Restrictions

The following remain blocked:

- mechanism claim publication without formal source-text extraction and review;
- mechanism population before A04-010 exact source-text extraction is completed;
- editorial review before A04-011 mechanism population is completed;
- pharmacokinetic extraction;
- pharmacodynamic extraction;
- safety extraction;
- evidence grading;
- therapeutic recommendation;
- prescription;
- clinical runtime enablement.

## A05 Future Field Extraction

Status: active blocker.

Program A05 populated only the bupropion mechanism field as internal non-runtime scientific content.

The following remain blocked:

- pharmacokinetics extraction;
- pharmacodynamics extraction;
- safety extraction;
- evidence grading;
- therapeutic recommendation;
- prescription;
- clinical runtime consumption.

## A06 Program Start

Status: blocked.

Program A06 requires an explicit governance package before execution can begin.

Resolved: A06 was executed by inbox package `A06_EXECUTE_FULL_PROGRAM.md` and completed through A06-017.

## A06 Future Field Extraction

Status: active blocker.

Program A06 populated only the mirtazapine mechanism field as internal non-runtime scientific content.

The following remain blocked:

- pharmacokinetics extraction;
- pharmacodynamics extraction;
- safety extraction;
- evidence grading;
- therapeutic recommendation;
- prescription;
- clinical runtime consumption.

## A07 Program Start

Status: ready from inbox.

Program A07 has a complete package in `codex/inbox/A07_EXECUTE_FULL_PROGRAM.md`.

No separate pre-execution authorization is required if dependencies, gates, traceability policy, tests and clinical safety restrictions pass.

Resolved: A07 was executed by inbox package `A07_EXECUTE_FULL_PROGRAM.md` and completed through A07-017.

## A07 Future Field Extraction

Status: active blocker.

Program A07 populated only the amitriptyline mechanism field as internal non-runtime scientific content.

The following remain blocked:

- pharmacokinetics extraction;
- pharmacodynamics extraction;
- safety extraction;
- evidence grading;
- therapeutic recommendation;
- prescription;
- clinical runtime consumption.

## A08 Program Start

Status: ready from inbox.

Program A08 has a complete package in `codex/inbox/A08_EXECUTE_FULL_PROGRAM.md`.

No separate pre-execution authorization is required if dependencies, gates, traceability policy, tests and clinical safety restrictions pass.

Resolved: A08 was executed by inbox package `A08_EXECUTE_FULL_PROGRAM.md` and completed through A08-017.

## A08 Future Field Extraction

Status: active blocker.

Program A08 populated only the phenelzine mechanism field as internal non-runtime scientific content.

The following remain blocked:

- pharmacokinetics extraction;
- pharmacodynamics extraction;
- safety extraction;
- evidence grading;
- therapeutic recommendation;
- prescription;
- clinical runtime consumption.

## A09 Program Package

Status: resolved.

`codex/inbox/A09_EXECUTE_FULL_PROGRAM.md` exists.

A09 was executed and completed through A09-017 as an internal non-runtime mechanism package for trazodone.

## A09 Future Field Extraction

Status: active blocker.

Program A09 populated only the trazodone mechanism field as internal non-runtime scientific content.

The following remain blocked:

- pharmacokinetics extraction;
- pharmacodynamics extraction;
- safety extraction;
- evidence grading;
- therapeutic recommendation;
- prescription;
- clinical runtime consumption.

## A10 Program Package

Status: resolved.

`codex/inbox/A10_EXECUTE_FULL_PROGRAM.md` exists.

A10 was executed and completed through A10-017 as an internal non-runtime mechanism package for chlorpromazine.

## A10 Future Field Extraction

Status: active blocker.

Program A10 populated only the chlorpromazine mechanism field as internal non-runtime scientific content.

The following remain blocked:

- pharmacokinetics extraction;
- pharmacodynamics extraction;
- safety extraction;
- evidence grading;
- therapeutic recommendation;
- prescription;
- clinical runtime consumption.

## A11 Program Package

Status: resolved.

`codex/inbox/A11_EXECUTE_FULL_PROGRAM.md` exists.

A11 was executed and completed through A11-017 as an internal non-runtime mechanism package for risperidone.

## A11 Future Field Extraction

Status: active blocker.

Program A11 populated only the risperidone mechanism field as internal non-runtime scientific content.

The following remain blocked:

- pharmacokinetics extraction;
- pharmacodynamics extraction;
- safety extraction;
- evidence grading;
- therapeutic recommendation;
- prescription;
- clinical runtime consumption.

## A12 Program Package

Status: resolved.

`codex/inbox/A12_EXECUTE_FULL_PROGRAM.md` exists.

A12 was executed and completed through A12-017 as an internal non-runtime mechanism package for lithium.

## A12 Future Field Extraction

Status: active blocker.

Program A12 populated only the lithium mechanism field as internal non-runtime scientific content.

The following remain blocked:

- pharmacokinetics extraction;
- pharmacodynamics extraction;
- safety extraction;
- evidence grading;
- therapeutic recommendation;
- prescription;
- clinical runtime consumption.

## A13 Program Package

Status: resolved.

`codex/inbox/A13_EXECUTE_FULL_PROGRAM.md` exists.

A13 was executed and completed through A13-017 as an internal non-runtime mechanism package for diazepam.

## A13 Future Field Extraction

Status: active blocker.

Program A13 populated only the diazepam mechanism field as internal non-runtime scientific content.

The following remain blocked:

- pharmacokinetics extraction;
- pharmacodynamics extraction;
- safety extraction;
- evidence grading;
- therapeutic recommendation;
- prescription;
- clinical runtime consumption.

## Next Inbox Package

Status: active blocker.

No later governed package is currently present in `codex/inbox/`.

## Track B Runtime Implementation

Status: active blocker.

Track B B01 through B08 were executed as governance artifacts only.

The following remain blocked:

- clinical runtime activation;
- runtime consumption of draft scientific knowledge;
- prescription;
- therapeutic recommendation;
- dose suggestion;
- patient-specific medication selection;
- patient-facing clinical guidance.

Future implementation requires a separate governed inbox package and explicit gate approval.

## Track D Certification and Release

Status: active blocker.

Track D D01 through D08 were executed as validation and certification governance artifacts only.

The following remain blocked:

- certification claim;
- regulatory compliance claim;
- release authorization;
- external approval claim;
- clinical runtime activation;
- prescription;
- therapeutic recommendation;
- dose suggestion;
- patient-specific medication selection.

Future certification, compliance or release requires a separate governed package and explicit gate approval.

## Track E Production Deployment

Status: active blocker.

Track E E01 through E08 were executed as production readiness governance artifacts only.

The following remain blocked:

- production deployment;
- patient data processing;
- production identity integration;
- production monitoring activation;
- compliance certification claim;
- release authorization;
- clinical runtime activation;
- prescription;
- therapeutic recommendation;
- dose suggestion;
- patient-specific medication selection.

Future production deployment requires a separate governed package and explicit gate approval.

## Track C Clinical UX Implementation

Status: active blocker.

Track C C01 through C08 were executed as product and UX governance artifacts only.

The following remain blocked:

- functional clinical UI implementation without a future governed package;
- UI-driven clinical conduct;
- autonomous diagnosis;
- prescription;
- therapeutic recommendation;
- dose suggestion;
- patient-specific medication selection;
- patient-facing clinical guidance.

Future implementation requires a separate governed inbox package and explicit gate approval.

## Ambiguities Found

- The former root `NEXT_MISSION.md` was outdated and generic. It was preserved as `governance/execution/NEXT_MISSION.root.md`.
- Multiple status files existed before this reorganization:
  - former root `PROJECT_STATUS.md`
  - former `governance/execution/PROJECT_STATUS.md`
  - former `governance/execution/PROJECT_EXECUTION_CONTEXT.md`
  - former `governance/execution/NEXT_MISSION.md`
  - former `governance/execution/NEXT_BLOCK.md`
- `governance/execution/PROJECT_EXECUTION_CONTEXT.md` was the clearest state document and was used to initialize `EXECUTION_STATE.json`.

## Duplicate Documents Preserved

- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/PROJECT_STATUS.root.md`
- `governance/execution/NEXT_MISSION.md`
- `governance/execution/NEXT_MISSION.root.md`

The root variants were preserved rather than overwritten.

## Human Review Needed

- Review whether root pointer files should be recreated for GitHub discoverability.
- Review internal links that still mention old `docs/` governance paths.
- Decide whether historical program documents in `governance/programs/` should later be indexed by program family.
- Treat older documents that still mention `BLOCKED - A04_SOURCE_SECTION_SELECTION_REQUIRED` as historical until they are formally archived or annotated.
