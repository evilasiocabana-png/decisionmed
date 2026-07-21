# Program A03 Dependencies

## Upstream Dependencies

- Program A01 - Official Scientific Knowledge Base;
- Program A02 - Psychopharmacology Library Population;
- Program A02.5 - SSRI Source Corpus Intake;
- SSRI Scientific Source Corpus `0.1.0-controlled-corpus`;
- ADR 0031 - A03 Scientific Content Population Gate;
- ADR 0044 - Insert Program A02.5 SSRI Source Corpus Intake.

## Released Dependency Scope

A03 may consume A02.5 only as an administrative source corpus package.

Current released scope:

- Phase 1 structural foundation completed;
- A03-011 completed as portfolio definition metadata-only;
- A03-012 completed as portfolio editorial registry metadata-only;
- A03-013 completed as administrative source binding metadata-only;
- A03-014 completed as directory generation metadata-only.

## Blocked Dependency Scope

A03 may not consume A02.5 as validated clinical content, because no scientific field extraction has occurred.

## Downstream Dependencies

- Program A04 remains blocked until the A03 workflow is validated.
- Evidence Runtime remains blocked from consuming A03 content until future publication gates.

## Current Next Dependency Step

```text
A03-015 - DRUG_TEMPLATE_GENERATION
```

This step may create empty drug templates only. It must not populate Drug Profiles, field-level scientific content or runtime objects.

## Declaration Final

A03 depends on A02.5 for corpus traceability, not for prevalidated clinical assertions.
