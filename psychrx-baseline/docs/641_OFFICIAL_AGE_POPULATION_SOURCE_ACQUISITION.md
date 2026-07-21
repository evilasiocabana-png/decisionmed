# 641 - Official Age-Population Source Acquisition

## Objective

Locate official population information for every medication in the PsychRx
decision-support catalog and normalize it into the four canonical age bands.

## Result

- medications researched: `83`;
- canonical age bands per medication: `4`;
- generated evidence rows: `332`;
- rows without a population summary: `0`;
- DailyMed/FDA rows: `292`;
- EMA rows: `4`;
- Health Canada rows: `8`;
- UK SmPC rows: `28`.

## Source Resolution

DailyMed SPL sections `8.4 Pediatric Use`, `8.5 Geriatric Use` and `2 Dosage
and Administration` are extracted when present. If a structured population
section is absent, extraction is restricted to bounded clinical section text
and requires both an age-population term and a clinical marker. Packaging,
ingredient and full-document text are never accepted as population evidence.

Agomelatine, amisulpride, bromazepam, dosulepin, levomepromazine, maprotiline,
mianserin, oral naltrexone, sulpiride and zopiclone use an appropriate alternate
official product-information source. Clomipramine uses the official Anafranil
label instead of the unsuitable prior locator.

## Boundary

Source acquisition is complete for display traceability. All rows remain
blocked from therapeutic runtime pending condition-, formulation- and
population-specific clinical review.
