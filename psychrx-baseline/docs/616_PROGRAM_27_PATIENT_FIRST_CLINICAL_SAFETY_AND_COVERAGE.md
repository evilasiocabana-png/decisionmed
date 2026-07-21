# 616 - Program 27 Patient-First Clinical Safety and Coverage

## Objective

Close the clinically relevant gaps identified by the WeMeds coverage audit while
preserving the PsychRx operating model:

```text
Patient -> current state -> safety -> current treatment -> response and
tolerability -> traceable strategy comparison -> physician decision
```

## Priority Gates

### P0 - Safety correctness

- explicit assessed state for essential safety domains;
- unselected never means denied;
- incomplete critical safety blocks or downgrades routine strategy;
- active evidence remains labelled by review status;
- P0 tests and audit.

### P1 - Population context

- calculate age from birth date;
- child, adolescent, adult and older-adult bands;
- pregnancy, lactation and postpartum remain distinct;
- population uncertainty modifies eligibility and confidence;
- P1 tests and audit.

### P2 - High-value clinical contexts

- structured adverse-syndrome and acute-risk context;
- delirium, withdrawal and substance contexts;
- perinatal, neurocognitive and developmental context boundaries;
- no unsupported treatment rules;
- P2 tests and audit.

### P3 - Pharmacological data governance

- interaction and alias coverage audit;
- missing condition-range audit;
- monitoring coverage;
- runtime eligibility based on review status;
- P3 tests and audit.

### P4 - Canonical coverage taxonomy

- canonical matrix for all 51 audited themes;
- covered, partial, relevant gap or contextual-only status;
- internal context normalization and UI alignment;
- no disease encyclopedia;
- P4 tests and audit.

### P5 - Certification

- full automated test suite;
- clinical safety regression audit;
- evidence and layer-dependency audit;
- coverage reconciliation;
- rollback verification;
- final certification report.

## Mission Sequence

- 617 - P0 explicit safety state contract;
- 618 - P0 safety UI and runtime integration;
- 619 - P0 validation and audit;
- 620 - P1 population context contract;
- 621 - P1 population integration;
- 622 - P1 validation and audit;
- 623 - P2 clinical context registry;
- 624 - P2 runtime integration;
- 625 - P2 validation and audit;
- 626 - P3 pharmacological governance audit services;
- 627 - P3 runtime eligibility and monitoring integration;
- 628 - P3 validation and audit;
- 629 - P4 canonical coverage matrix;
- 630 - P4 context normalization and UI alignment;
- 631 - P4 validation and audit;
- 632 - P5 integrated test and architecture audit;
- 633 - P5 final certification report.

## Permanent Restrictions

- no autonomous diagnosis;
- no autonomous prescription;
- no unsourced clinical rule;
- no interface-owned clinical logic;
- no automatic conversion of a diagnosis into symptoms or medication;
- no disease encyclopedia or `Apply to case` workflow.

## Rollback

Every priority must remain revertible independently. The complete pre-program
restore point is documented in ADR 0050.

## Declaration Final

Program 27 is ready for sequential implementation. A priority is complete only
after its tests pass and its audit records no blocking discrepancy.
