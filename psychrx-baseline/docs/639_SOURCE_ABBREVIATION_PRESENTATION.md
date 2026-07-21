# 639 - Source Abbreviation Presentation

## Objective

Present already-registered sources pragmatically in the clinical result: a
short source code in parentheses beside the content and one visible legend
below the result.

## Implementation

- official disease-use indication matches receive their regulatory source code,
  such as `(DM)` or `(EMA)`;
- a mapped guideline that still lacks row-level support is shown transparently
  as `(NICE/PENDENTE)`;
- an unsupported row remains `(PENDENTE)`;
- interaction lines are rendered with their existing source codes in
  parentheses instead of a long `Fonte:` suffix;
- ranking and evidence citations use compact source codes;
- dose-range source is rendered as `(TM)`, `(DM)`, `(HC)` or the applicable
  source code;
- one source legend is visible below the decision-support result.

## Source Legend

- `DM` - DailyMed/FDA;
- `NICE` - National Institute for Health and Care Excellence;
- `EMA` - European Medicines Agency;
- `HC` - Health Canada;
- `ANVISA` - Brazilian regulator;
- `TM` - PsychRx local tables;
- `ST-E`, `ST-PG`, `GG` and `BNF` - identified scientific references;
- `PENDENTE` - supporting source not yet confirmed for that claim.

## Boundary

This mission changes presentation and source traceability only. It does not
promote pending scientific content or change clinical ranking logic.

## Declaration Final

The app now exposes compact source references where the clinician reads the
content, with a single legend that explains every abbreviation.
