# SNRI Mechanism of Action Draft

## Metadata

Project: PsychRx

Program: A04 - Scientific Content Population: SNRIs

Mission: A04-009 - SNRI_MECHANISM_POPULATION_DRAFT

Status: draft_non_runtime

Runtime eligibility: not_eligible

Date: 2026-07-04

## Purpose

This artifact creates the first traceable draft structure for SNRI mechanism-of-action knowledge.

It does not populate clinical runtime knowledge. It does not create therapeutic recommendations, prescribing guidance, diagnostic guidance, comparative conclusions, or safety alerts.

## Scope

Allowed scope:

- mechanism field only;
- SNRI class and individual SNRI profile slots;
- traceability to source sections selected by A04-008G;
- unresolved draft slots when source text has not yet been extracted.

Forbidden scope:

- pharmacokinetics;
- pharmacodynamics outside the mechanism field;
- safety;
- adverse effects;
- interactions;
- indications;
- dosing;
- evidence grading;
- therapeutic recommendation;
- prescription;
- clinical runtime use.

## Source Section Basis

The following selected source sections are the only authorized basis for this draft.

| Selection ID | Drug | Source | Selected Section | Status |
| --- | --- | --- | --- | --- |
| A04-008G-SEC-001 | Venlafaxine | DailyMed | Official label record; CLINICAL PHARMACOLOGY section; mechanism-related subsection when present | selected_reviewable_pending_extraction |
| A04-008G-SEC-002 | Venlafaxine | Drugs@FDA | FDA approved labeling; Clinical Pharmacology section | selected_reviewable_pending_extraction |
| A04-008G-SEC-003 | Desvenlafaxine | DailyMed | Official label record; CLINICAL PHARMACOLOGY section; mechanism-related subsection when present | selected_reviewable_pending_extraction |
| A04-008G-SEC-004 | Desvenlafaxine | Drugs@FDA | FDA approved labeling; Clinical Pharmacology section | selected_reviewable_pending_extraction |
| A04-008G-SEC-005 | Duloxetine | DailyMed | Official label record; CLINICAL PHARMACOLOGY section; mechanism-related subsection when present | selected_reviewable_pending_extraction |
| A04-008G-SEC-006 | Duloxetine | Drugs@FDA | FDA approved labeling; Clinical Pharmacology section | selected_reviewable_pending_extraction |
| A04-008G-SEC-007 | Levomilnacipran | DailyMed | Official label record; CLINICAL PHARMACOLOGY section; mechanism-related subsection when present | selected_reviewable_pending_extraction |
| A04-008G-SEC-008 | Levomilnacipran | Drugs@FDA | FDA approved labeling; Clinical Pharmacology section | selected_reviewable_pending_extraction |
| A04-008G-SEC-009 | Milnacipran | DailyMed | Official label record; CLINICAL PHARMACOLOGY section; mechanism-related subsection when present | selected_reviewable_pending_extraction |
| A04-008G-SEC-010 | Milnacipran | Drugs@FDA | FDA approved labeling; Clinical Pharmacology section | selected_reviewable_pending_extraction |

## Draft Claim Policy

No scientific mechanism claim is populated in this artifact because the selected source sections currently exist as reviewable remote locators, not as extracted source text.

Every drug slot below is therefore marked as:

```text
unresolved_pending_source_text_extraction
```

This preserves traceability and prevents unreviewed or memory-derived scientific content from entering the PsychRx Knowledge Base.

## Class-Level Mechanism Slot

Status: unresolved_pending_source_text_extraction

Draft content:

```text
Not populated in A04-009. Requires formal extraction from the selected source sections before any mechanism statement can be written.
```

Traceability:

- A04-008G-SEC-001
- A04-008G-SEC-002
- A04-008G-SEC-003
- A04-008G-SEC-004
- A04-008G-SEC-005
- A04-008G-SEC-006
- A04-008G-SEC-007
- A04-008G-SEC-008
- A04-008G-SEC-009
- A04-008G-SEC-010

## Drug Mechanism Slots

### Venlafaxine

Drug ID: SNRI-VENLAFAXINE

Anchor ID: A04-SNRI-VENLAFAXINE-MECHANISM-ANCHOR-001

Selected sections:

- A04-008G-SEC-001
- A04-008G-SEC-002

Mechanism claim status: unresolved_pending_source_text_extraction

Draft content:

```text
Not populated in A04-009. Requires formal extraction from selected Venlafaxine source sections.
```

### Desvenlafaxine

Drug ID: SNRI-DESVENLAFAXINE

Anchor ID: A04-SNRI-DESVENLAFAXINE-MECHANISM-ANCHOR-001

Selected sections:

- A04-008G-SEC-003
- A04-008G-SEC-004

Mechanism claim status: unresolved_pending_source_text_extraction

Draft content:

```text
Not populated in A04-009. Requires formal extraction from selected Desvenlafaxine source sections.
```

### Duloxetine

Drug ID: SNRI-DULOXETINE

Anchor ID: A04-SNRI-DULOXETINE-MECHANISM-ANCHOR-001

Selected sections:

- A04-008G-SEC-005
- A04-008G-SEC-006

Mechanism claim status: unresolved_pending_source_text_extraction

Draft content:

```text
Not populated in A04-009. Requires formal extraction from selected Duloxetine source sections.
```

### Levomilnacipran

Drug ID: SNRI-LEVOMILNACIPRAN

Anchor ID: A04-SNRI-LEVOMILNACIPRAN-MECHANISM-ANCHOR-001

Selected sections:

- A04-008G-SEC-007
- A04-008G-SEC-008

Mechanism claim status: unresolved_pending_source_text_extraction

Draft content:

```text
Not populated in A04-009. Requires formal extraction from selected Levomilnacipran source sections.
```

### Milnacipran

Drug ID: SNRI-MILNACIPRAN

Anchor ID: A04-SNRI-MILNACIPRAN-MECHANISM-ANCHOR-001

Selected sections:

- A04-008G-SEC-009
- A04-008G-SEC-010

Mechanism claim status: unresolved_pending_source_text_extraction

Draft content:

```text
Not populated in A04-009. Requires formal extraction from selected Milnacipran source sections.
```

## Review Requirements

Before any mechanism content can be promoted beyond this draft:

1. Extract exact source text from each selected source section.
2. Link each extracted sentence or passage to its source-section ID.
3. Mark each extracted item as reviewable.
4. Submit the mechanism draft to scientific/editorial review.
5. Preserve non-runtime status until a future runtime eligibility gate explicitly changes it.

## Remaining Restrictions

This artifact does not release:

- PK extraction;
- PD extraction;
- safety extraction;
- evidence grading;
- recommendation;
- prescription;
- runtime clinical consumption.

## Declaration

A04-009 created a traceable, non-runtime SNRI mechanism draft structure. It did not populate mechanism claims because the required source text has not yet been formally extracted from the selected sections.
