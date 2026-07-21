# ADR 0050 - Patient-First Safety and Coverage Program

## Status

Accepted for implementation on 2026-07-20.

## Context

The current PsychRx web workflow contains a useful patient-first pharmacological
review, but the coverage audit found four structural risks:

- an unselected safety item can be transported as if it had been denied;
- `birth_date` is collected but does not influence the local motor;
- internal knowledge coverage is broader than the contexts exposed by the UI;
- large parts of the medication-context and dose-range data remain pending formal
  scientific review.

The founder authorized a governed P0-P5 program to close relevant gaps without
turning PsychRx into a disease encyclopedia.

## Decision

Create Program 27 - Patient-First Clinical Safety and Coverage, organized in six
sequential priorities:

1. P0 - explicit safety state and evidence eligibility;
2. P1 - age and special-population context;
3. P2 - adverse syndromes and missing high-value clinical contexts;
4. P3 - medication data, interactions, aliases, ranges and monitoring governance;
5. P4 - topic taxonomy and UI/runtime alignment;
6. P5 - integrated validation and certification.

Each priority must end with automated tests and a written audit gate before the
next priority starts.

## Architectural Boundaries

- Patient state remains the entry point.
- The UI collects and presents; it does not create clinical meaning.
- Missing safety data remains uncertainty and never becomes a negative finding.
- Draft or awaiting-validation knowledge cannot silently support a strong output.
- Clinical rules require traceable sources or a governance contract that only
  enforces structural safety.
- The physician remains the final decision-maker.
- No automatic diagnosis, prescription or dose calculation is authorized.
- No WeMeds-like disease library or `Apply to case` workflow is authorized.

## Consequences

- Existing request and response contracts may gain backward-compatible fields.
- Safety-incomplete requests may be blocked or downgraded.
- Population context may alter eligibility and confidence only through explicit,
  testable rules.
- Context coverage will be measured by a canonical audit matrix.
- Scientific gaps remain visible until their evidence passes the official gates.

## Rollback

The pre-program state is preserved by:

- tag `restore/pre-p0-p5-20260720-b155a6c`;
- branch `codex/restore-pre-p0-p5-20260720`;
- bundle `C:\Users\evcab\PsychRx_pre_p0_p5_20260720_b155a6c.bundle`.

## Declaration

Program 27 may improve safety, population awareness, coverage and auditability,
but it may not change PsychRx from patient-first decision support into autonomous
clinical decision-making or a disease encyclopedia.
