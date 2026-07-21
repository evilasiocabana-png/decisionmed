# 644 - Guided Demonstration Case Sequence

## Objective

Expose one visible simulated case for every major P1-P5 implementation group,
immediately after the existing acute-toxicity and intoxication examples, while
preserving the complete medication, interaction, dose-band and association test
suite.

## Canonical Order

| Position | Group | Demonstration |
|---:|---|---|
| 1-5 | Existing clinical prescription flow | one to five clinical axes |
| 6 | P0 acute safety | suspected medication toxicity |
| 7 | P0 acute safety | suspected intoxication or excessive exposure |
| 8-11 | P1 age | child, adolescent, adult and older adult |
| 12-16 | P1 special population | pregnancy, lactation, postpartum, altered renal function and altered hepatic function |
| 17-20 | P2 clinical context | adverse syndrome, substance, diagnostic boundary and population boundary |
| 21-22 | P3 pharmacological governance | known interaction and pending interaction profile |
| 23-24 | P3 official monitoring | lithium and antipsychotic monitoring rules |
| 25-26 | P4 canonical coverage | mapped topic and explicit context outside the 51-topic matrix |
| 27 | P5 integration | complete multi-axis scenario |
| 28 onward | Existing exhaustive suite | remaining prescriptions, interactions, medications/dose bands and associations |

## Presentation

The clinical-advice card now identifies the next case number, group and label.
After a case is generated, the status line records the group and demonstration
that was loaded. Clinical-context examples also select their corresponding
registry entry by canonical identifier.

## Safety Boundary

These are simulated presentation fixtures. They exercise existing contracts but
do not introduce a diagnosis, treatment rule, medication choice, dose rule or
scientific claim. Population and safety gates remain unchanged; blocked examples
must continue to render as blocked.

## Coverage Result

- existing scenarios preserved: `342`;
- new guided demonstrations: `20`;
- total sequence: `362`;
- first age example: position `8`, immediately after intoxication;
- exhaustive coverage resumes: position `28`.

## Validation Audit

- interface tests: `14` passed;
- complete automated suite: `246` passed;
- JavaScript syntax and Python compilation: passed;
- visual sequence audit: cases `1-27` executed in order;
- age results: `9` child, `15` adolescent, `46` adult and `76` older adult;
- official population evidence: DailyMed, EMA and Health Canada abbreviations
  rendered in the expected age cases;
- clinical registry selections: `AKATHISIA`, `ALCOHOL_CONTEXT`,
  `NEUROCOGNITIVE_CONTEXT` and `PERINATAL_CONTEXT` rendered in positions
  `17-20`;
- monitoring activation: `TPC-012` for lithium and `TPC-014`/`TPC-015` for
  antipsychotic monitoring;
- P4 output: one mapped `covered` theme and one explicit context outside the
  matrix;
- next case after P5: position `28`, resuming the pre-existing exhaustive suite;
- browser console errors: `0`.

## Rollback

- tag `restore/pre-guided-case-sequence-20260720-f6ee7fc`;
- branch `codex/restore-pre-guided-case-sequence-20260720`;
- bundle `C:\Users\evcab\PsychRx_pre_guided_case_sequence_20260720_f6ee7fc.bundle`.

## Declaration Final

The guided sequence explains what each implemented group does without changing
the patient-first consultation flow or the physician decision boundary.
