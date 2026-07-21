# ADR 0042 - Block Program A14 Until Program A13 Validation

## ID

0042

## Date

2026-06-30

## Status

Accepted.

## Context

Program A14 proposes the scientific population of ADHD medications, including stimulants and non-stimulants.

The requested scope includes methylphenidate, lisdexamfetamine, dexamphetamine, atomoxetine, guanfacine and clonidine, with ADHD-specific scientific metadata such as controlled substance metadata, abuse potential, diversion risk, cardiovascular risk, pediatric monitoring, growth, appetite and sleep effects.

This scope depends on Program A13 and on the scientific governance established by Program 21, Program 22, the Safety Engine and the Evidence Runtime.

However, Program A13 is blocked by Program A12, and the whole scientific population chain remains blocked back to Program A03. Program A03 has not yet completed source corpus intake, reviewer assignment, field-level traceability validation or editorial publication gates.

## Decision

Program A14 must not be executed until Program A13 is validated or until a formal CTO exception ADR explicitly authorizes a different order.

The current authorized next mission remains:

```text
MISSION A03-002 - SSRI Source Corpus Intake
```

## Alternatives Considered

1. Execute Program A14 immediately.

Rejected. This would create high-risk ADHD medication content before the scientific content pipeline is validated.

2. Create metadata-only placeholders for ADHD medications.

Rejected for now. Even metadata-only controlled substance, cardiovascular and pediatric monitoring structures would risk bypassing the validated sequence unless explicitly authorized.

3. Block Program A14 and preserve the existing dependency chain.

Accepted. This keeps the project aligned with scientific governance and traceability.

## Justification

ADHD medication content has specific risks:

- stimulant misuse and diversion;
- controlled substance metadata;
- cardiovascular monitoring;
- pediatric growth and appetite monitoring;
- sleep effects;
- psychosis and mania risk;
- age-group specificity;
- regulatory availability differences.

These fields must not be populated before the source corpus, validation workflow and publication gates are proven in earlier medication-class programs.

## Impact

Program A14 is recorded as blocked.

No ADHD medication content is added.

No Safety Engine integration is added.

No Evidence Runtime integration is added.

No prescribing or recommendation behavior is introduced.

Project navigation documents must continue to point to A03-002 as the next authorized mission.

## Risks

The main risk is roadmap delay for ADHD medication content.

This is acceptable because premature content population would create larger clinical, scientific and architectural risk.

## Documents Affected

- `docs/PROGRAM_A14_BLOCKED_REPORT.md`
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
- Programs A04 through A13 have completed or have formal CTO exception ADRs;
- ADHD-specific governance for controlled substances, cardiovascular risk and pediatric monitoring is approved;
- NEXT_MISSION authorizes Program A14.

## Declaration Final

Program A14 remains blocked until the upstream scientific population pipeline is validated. This decision protects the scientific integrity, traceability and safety-first architecture of PsychRx.
