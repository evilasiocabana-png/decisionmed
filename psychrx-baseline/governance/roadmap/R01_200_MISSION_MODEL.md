# R01 200 Mission Model

## Mission

R01-001 - ROADMAP_REFACTORING_TO_200_MISSION_MODEL.

## Target

The new roadmap target contains 176 total mission slots.

This is below the maximum of 200 missions.

## Target Programs

| Program | Name | Mission Range | Count |
| --- | --- | ---: | ---: |
| 00 | Governance Foundation | 001-012 | 12 |
| 01 | Clinical Architecture | 013-028 | 16 |
| 02 | Software Platform | 029-044 | 16 |
| 03 | Clinical Workspace | 045-060 | 16 |
| 04 | Clinical Runtime Shell | 061-076 | 16 |
| 05 | Knowledge Framework | 077-092 | 16 |
| 06 | Scientific Corpus Pipeline | 093-108 | 16 |
| 07 | Scientific Extraction Pipeline | 109-124 | 16 |
| 08 | Drug Class Population Pipeline | 125-144 | 20 |
| 09 | Evidence Integration Pipeline | 145-156 | 12 |
| 10 | Safety and Constraint Pipeline | 157-168 | 12 |
| 11 | QA and Publication | 169-176 | 8 |
| 12 | Runtime Eligibility | 177-184 | 8 |
| 13 | Clinical Release Governance | 185-200 | 16 |

## Compression Rule

Mission ranges are framework missions.

They do not multiply by drug class.

Drug classes are parameters:

```text
DrugClass = SSRIs | SNRIs | NDRIs | NaSSAs | TCAs | MAOIs | SGAs | FGAs | MoodStabilizers | Anxiolytics | ADHD
```

## Historical Mapping

Existing mission documents remain historical evidence of design and execution.

Future execution should use the compressed model unless a CTO-approved exception is recorded.

## Final Declaration

The proposed model fits inside 200 missions and replaces repetitive class-specific program creation with reusable pipelines.
