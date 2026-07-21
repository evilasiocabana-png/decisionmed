# A04-008C - SNRI Source Section Selection Or Blocker

## Program

PROGRAM A04 - Scientific Content Population: SNRIs.

## Mission

A04-008C - SNRI_SOURCE_SECTION_SELECTION_OR_BLOCKER.

## Objective

Select source sections if SNRI source texts are available, or formally block extraction if source texts are unavailable.

## Result

```text
BLOCKED
```

No selectable SNRI source text files were found.

## Availability Check

Checked paths:

- `ScientificCorpus/SNRIs/`
- `ScientificCorpus/SourceTextIntake/SNRIs/`

Selectable source text extensions checked:

- `.txt`
- `.pdf`
- `.html`
- `.htm`
- `.xml`
- `.docx`

Result:

```text
source_text_files_found: 0
```

## Created Artifact

- `KnowledgeBase/SNRIs/Traceability/SNRI_SOURCE_SECTION_SELECTION_OR_BLOCKER.json`

## Blocked Mission

```text
A04-009 - SNRI_MECHANISM_POPULATION_DRAFT
```

## Blocking Reason

The SNRI corpus contains metadata, manifests, indexes and validation artifacts, but no selectable source text files.

Without source text files, source sections cannot be selected.

Without selected source sections, scientific extraction cannot begin.

## Required Next Action

```text
A04-008D - SNRI_SOURCE_TEXT_ACQUISITION_PACKAGE
```

## Explicit Non-Actions

No source section was selected.

No source text was interpreted.

No scientific claim was extracted.

No SNRI profile field was populated.

No evidence was graded.

No therapeutic recommendation was created.

No prescription, dose guidance or clinical decision was created.

## Runtime Eligibility

```text
not_eligible
```

## Final Declaration

Program A04 is formally blocked before A04-009 until selectable SNRI source texts are acquired or registered.

