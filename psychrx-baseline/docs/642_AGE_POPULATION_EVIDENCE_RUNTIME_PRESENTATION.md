# 642 - Age-Population Evidence Runtime Presentation

## Objective

Show official age-population information beside the clinical result without
turning a source excerpt into an automated treatment rule.

## Implementation

- added a read-only Application-layer population evidence table;
- crosses current medication and available candidates with the backend-derived
  canonical age band;
- returns source-transparent lines in `population_evidence_summary`;
- displays those lines under `Faixa etaria e fonte oficial`;
- adds `UK-SMPC` to the visible source legend;
- preserves the existing review block for children, adolescents and older
  adults;
- keeps all therapeutic runtime flags false.

## Declaration Final

The clinician can now see the official population statement relevant to the
patient's age band. The app still does not prescribe, calculate a dose or remove
the special-population review boundary.
