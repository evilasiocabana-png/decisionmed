# ADR 0043 - Block Program A15 Until Program A14 Validation

## ID

0043

## Date

2026-06-30

## Status

Accepted.

## Context

Program A15 proposes the scientific population of cognitive enhancers and dementia-related psychopharmacology.

The requested scope includes donepezil, rivastigmine, galantamine and memantine, with medication-specific metadata such as cognitive domains, behavioral symptoms, dementia stage mapping, bradycardia risk, syncope risk, weight loss risk, renal and hepatic considerations and caregiver considerations.

This scope depends on Program A14 and on the scientific governance established by Program 21, Program 22, the Safety Engine, the Evidence Runtime and the Clinical Operating Mind.

However, Program A14 is blocked by Program A13, and the whole scientific population chain remains blocked back to Program A03. Program A03 has not yet completed source corpus intake, reviewer assignment, field-level traceability validation or editorial publication gates.

The Program A15 request references ADR 0042, but ADR 0042 already exists for Program A14. This ADR therefore uses ID 0043.

## Decision

Program A15 must not be executed until Program A14 is validated or until a formal CTO exception ADR explicitly authorizes a different order.

The current authorized next mission remains:

```text
MISSION A03-002 - SSRI Source Corpus Intake
```

## Alternatives Considered

1. Execute Program A15 immediately.

Rejected. This would create dementia-related psychopharmacology content before the scientific content pipeline is validated.

2. Create metadata-only placeholders for cognitive enhancers.

Rejected for now. Even metadata-only geriatric, cognitive-domain, dementia-stage and safety structures would bypass the validated sequence unless explicitly authorized.

3. Block Program A15 and preserve the existing dependency chain.

Accepted. This keeps the project aligned with scientific governance and traceability.

## Justification

Cognitive enhancer and dementia-related psychopharmacology content has specific risks:

- older adult vulnerability;
- bradycardia and syncope risks;
- weight loss and gastrointestinal effects;
- renal and hepatic considerations;
- disease-stage specificity;
- caregiver-context metadata;
- neuropsychiatric symptom interpretation;
- possible confusion between cognitive support and therapeutic recommendation.

These fields must not be populated before the source corpus, validation workflow and publication gates are proven in earlier medication-class programs.

## Impact

Program A15 is recorded as blocked.

No cognitive enhancer content is added.

No dementia-related medication content is added.

No Safety Engine integration is added.

No Evidence Runtime integration is added.

No prescribing or recommendation behavior is introduced.

Project navigation documents must continue to point to A03-002 as the next authorized mission.

## Risks

The main risk is roadmap delay for dementia-related psychopharmacology content.

This is acceptable because premature content population would create larger clinical, scientific and architectural risk.

## Documents Affected

- `docs/PROGRAM_A15_BLOCKED_REPORT.md`
- `governance/execution/PROJECT_STATUS.md`
- `PROJECT_STATUS.md`
- `governance/execution/PROJECT_PROGRESS.md`
- `governance/execution/PROJECT_TREE.md`
- `docs/PROJECT_DEPENDENCIES.md`
- `governance/execution/PROJECT_INDEX.md`
- `governance/execution/NEXT_MISSION.md` remains unchanged.

## Review Criteria

This ADR may be reviewed when:

- Program A03 source corpus intake is complete;
- Fluoxetine pilot validation is complete;
- Programs A04 through A14 have completed or have formal CTO exception ADRs;
- older adult, dementia-stage and cognitive-domain governance is approved;
- NEXT_MISSION authorizes Program A15.

## Declaration Final

Program A15 remains blocked until the upstream scientific population pipeline is validated. This decision protects the scientific integrity, traceability and safety-first architecture of PsychRx.
