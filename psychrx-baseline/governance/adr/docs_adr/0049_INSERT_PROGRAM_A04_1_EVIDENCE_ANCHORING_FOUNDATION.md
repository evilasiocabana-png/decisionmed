# ADR 0049 - Insert Program A04.1 Evidence Anchoring Foundation

## Status

Proposed - Pending Final Governance Review.

## Context

Program A04 is active but blocked before A04-009 because the official gate reports:

- source sections selected: 0;
- selected sections reviewable: 0;
- A04-009 may start: false.

The proposed next work was named "Program A05 - Evidence Anchoring & Scientific Extraction Foundation". This conflicts with the existing roadmap, where Program A05 is already reserved for Scientific Content Population: NDRIs.

## Proposed Decision

Insert an intermediate program named:

```text
PROGRAM A04.1 - Evidence Anchoring & Scientific Extraction Foundation
```

Program A04.1 exists between:

```text
PROGRAM A04 - Scientific Content Population: SNRIs
```

and:

```text
A04-009 - SNRI_MECHANISM_POPULATION_DRAFT
```

Program A04.1 would not replace Program A05. Program A05 remains reserved for NDRIs and remains blocked.

This decision is intentionally marked as pending. It should be resolved at the final governance review for the current block, not during source inventory work.

## Rationale

The project needs a governed evidence anchoring foundation before any scientific extraction can occur.

This program creates the administrative and traceability infrastructure required to transform:

```text
Specific source
-> Specific section
-> Psychopharmacological field
-> Reviewable content
```

into future evidence objects.

## Impact

- A04-009 remains blocked.
- Program A04 remains active.
- Program A04.1 remains a proposed execution lane until final governance review.
- Program A05 remains NDRIs and stays blocked.
- No scientific content is extracted.
- No runtime eligibility is created.

## Risks

- If Program A04.1 is confused with Program A05, roadmap drift may occur.
- If section mapping is treated as extraction, the Evidence Traceability Policy may be violated.
- If sections are approved without reviewability, A04-009 may be incorrectly released.

## Documents Affected

- `docs/PROGRAM_A04_1_EVIDENCE_ANCHORING_FOUNDATION.md`
- `governance/execution/NEXT_MISSION.md`
- `governance/execution/NEXT_BLOCK.md`
- `governance/execution/PROJECT_EXECUTION_CONTEXT.md`
- `governance/execution/PROJECT_STATUS.md`
- `PROJECT_STATUS.md`
- `governance/execution/PROJECT_PROGRESS.md`
- `governance/execution/PROJECT_TREE.md`
- `governance/execution/PROJECT_INDEX.md`

## Review Criteria

This ADR must be resolved during the final governance review for the current block.

It should also be revisited if:

- Program A05 is renumbered by a formal roadmap ADR;
- A04-009 is released by an approved section-selection gate;
- the evidence anchoring pipeline is generalized for all drug classes.
