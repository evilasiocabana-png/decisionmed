# Project Maturity Report - PsychRx

## Date

2026-07-01

## Overall Maturity

PsychRx is architecturally mature for its current phase, but scientifically and product-functionally immature.

The project has strong scaffolding. It does not yet have clinically validated, runtime-consumable scientific knowledge.

## Maturity by Area

| Area | Maturity | Assessment |
| --- | ---: | --- |
| Governance | High | ADRs, status files, mission controls and dependency rules exist. |
| Architecture | High | Core architecture is well defined and layered. |
| Documentation | High volume, medium usability | Very complete but heavy. Navigation requires strict controls. |
| Scientific Corpus | Medium | Corpus is structured and published, but content extraction is not complete. |
| KnowledgeBase | Medium | Strong structures and shells; limited populated scientific content. |
| Runtime | Structural | Runtime layers exist as architectural/read-only baselines. |
| Frontend | Prototype | Localhost app exists and is read-only. |
| Backend | Structural | Service architecture exists; clinical runtime is not clinically operational. |
| QA | Good for current scope | 146 tests pass; JSON valid. |

## Program Maturity

| Program Range | Maturity |
| --- | --- |
| Program 00-06 | Foundational maturity achieved. |
| Program 07-17 | Structural baseline maturity achieved. |
| Program 18-26 | Strategic architecture baseline achieved. |
| Track A A01-A02.5 | Corpus and knowledge infrastructure mature enough for controlled modeling. |
| Track A A03 | Active and partially mature. |
| Track A A04-A15 | Intentionally blocked. |

## Key Maturity Gap

The main gap is transition from structural shells to validated scientific content.

Program A03 must not rush into clinical claims, indications, safety, interactions or recommendations without field-level extraction, source traceability and editorial review.

## Readiness for Next Step

Ready for:

```text
A03-026 - INDICATION_MODELING
```

Not ready for:

- therapeutic recommendations;
- clinical decision runtime;
- automated prescribing;
- full drug profile publication;
- opening A04 in parallel.

## Maturity Recommendation

Create a formal execution protocol before continuing many more missions manually.

