# 624 - P2 Clinical Context Runtime Integration

## Objective

Integrate priority contexts into explicit safety assessment and the existing
patient-first flow.

## Implementation

- aggression, delirium, intoxication, withdrawal, allergy and severe prior
  reaction became explicit essential safety domains;
- the UI no longer relies on the generic restrictions card for these domains;
- added a non-prescriptive clinical-context selector for adverse syndromes,
  substances, neurocognitive/developmental boundaries and perinatal context;
- added `/api/clinical-contexts` backed by the Application Layer registry;
- transported selected canonical identifiers in the decision-support request;
- applied registry blocking contexts before routine ranking;
- exposed selected contexts and their evidence/runtime status in the response;
- retained the separate source-anchored toxidrome screening flow.

## Preserved Boundaries

- no diagnosis is generated from a selected context;
- no treatment, antidote, emergency dose or drug ranking is encoded in the
  registry;
- `source_pending` contexts only add traceable structure and display context;
- clinical logic remains outside the Interface Layer.

## Declaration Final

P2 contexts participate in safety routing without changing the core PsychRx
workflow or its physician decision boundary.
