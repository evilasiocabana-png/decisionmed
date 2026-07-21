# A04-008G - SNRI Source Section Selection Execution

## Objective

Resolve the A04 pre-extraction blocker by selecting specific, reviewable source sections for the SNRI mechanism field.

This mission does not extract, interpret, normalize or populate scientific content.

## Scope

Allowed:

- select source sections;
- link each section to a drug and psychopharmacological field;
- record reviewable remote location metadata;
- re-evaluate the A04 source-section gate.

Forbidden:

- mechanism content extraction;
- pharmacokinetic extraction;
- pharmacodynamic extraction;
- safety extraction;
- evidence grading;
- therapeutic recommendation;
- prescription;
- clinical runtime enablement.

## Sources

The selected sections use existing A04.0 source records:

| Source ID | Source | Type | Access |
| --- | --- | --- | --- |
| A04.0-SD-R002 | DailyMed | official label database | public remote source locator |
| A04.0-SD-R001 | Drugs@FDA | regulatory database | public remote source locator |

## Selected Sections

| Selection ID | Drug | Source | Section | Field | Review Status |
| --- | --- | --- | --- | --- | --- |
| A04-008G-SEC-001 | Venlafaxine | DailyMed | CLINICAL PHARMACOLOGY; mechanism-related subsection when present | mechanism | selected_reviewable_pending_extraction |
| A04-008G-SEC-002 | Venlafaxine | Drugs@FDA | Approved labeling; Clinical Pharmacology | mechanism | selected_reviewable_pending_extraction |
| A04-008G-SEC-003 | Desvenlafaxine | DailyMed | CLINICAL PHARMACOLOGY; mechanism-related subsection when present | mechanism | selected_reviewable_pending_extraction |
| A04-008G-SEC-004 | Desvenlafaxine | Drugs@FDA | Approved labeling; Clinical Pharmacology | mechanism | selected_reviewable_pending_extraction |
| A04-008G-SEC-005 | Duloxetine | DailyMed | CLINICAL PHARMACOLOGY; mechanism-related subsection when present | mechanism | selected_reviewable_pending_extraction |
| A04-008G-SEC-006 | Duloxetine | Drugs@FDA | Approved labeling; Clinical Pharmacology | mechanism | selected_reviewable_pending_extraction |
| A04-008G-SEC-007 | Levomilnacipran | DailyMed | CLINICAL PHARMACOLOGY; mechanism-related subsection when present | mechanism | selected_reviewable_pending_extraction |
| A04-008G-SEC-008 | Levomilnacipran | Drugs@FDA | Approved labeling; Clinical Pharmacology | mechanism | selected_reviewable_pending_extraction |
| A04-008G-SEC-009 | Milnacipran | DailyMed | CLINICAL PHARMACOLOGY; mechanism-related subsection when present | mechanism | selected_reviewable_pending_extraction |
| A04-008G-SEC-010 | Milnacipran | Drugs@FDA | Approved labeling; Clinical Pharmacology | mechanism | selected_reviewable_pending_extraction |

## Linked Fields

Only the `mechanism` field is linked by this mission.

The following fields remain blocked:

- pharmacokinetics;
- pharmacodynamics;
- safety;
- contraindications;
- interactions;
- indications;
- posology;
- evidence.

## Review Criteria

A selected section is reviewable when it has:

- specific source ID;
- specific source database or document family;
- specific drug name;
- specific section label;
- target psychopharmacological field;
- remote review location.

## Blocked Items

This mission does not authorize:

- runtime use;
- therapeutic recommendations;
- clinical decision support output;
- prescribing;
- PK/PD/safety extraction.

## Criterion To Release A04-009

A04-009 may start only because the mechanism field now has selected and reviewable source sections for each SNRI in the official A04 portfolio.

A04-009 remains limited to mechanism population draft work, and all output must remain non-runtime-eligible.
