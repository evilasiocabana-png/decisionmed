# 643 - Age-Population Validation Audit

## Scope

Validate the official age-population evidence catalog, its safe Application
integration and the physician-facing web presentation added by ADR 0052.

## Catalog Audit

- medications: `83/83`;
- age bands: `4/4` for every medication;
- total rows: `332/332`;
- missing population summaries: `0`;
- duplicate medication/age-band keys: `0`;
- display-eligible rows: `332`;
- therapeutic-runtime-eligible rows: `0`;
- structured official population sections: `273`;
- curated alternate official product-information rows: `44`;
- bounded clinical population-text rows: `15`.

An intermediate audit identified broad-label extraction noise in legacy SPLs.
The extractor was corrected before acceptance: fallback content is now limited
to clinical sections, bounded sentences, population terms and clinical markers.
The regenerated catalog contains no packaging or ingredient fallback text.

## Source Audit

- DailyMed/FDA: `292` rows;
- European Medicines Agency: `4` rows;
- Health Canada product monographs: `8` rows;
- UK Summary of Product Characteristics: `28` rows.

Every row contains a source title, official locator, population anchor,
abbreviation and content checksum. The accepted hosts are limited by automated
test to `dailymed.nlm.nih.gov`, `ema.europa.eu`, `pdf.hres.ca` and
`medicines.org.uk`.

## Runtime and UI Audit

- the backend-derived band selects only the matching evidence row;
- current medicines and visible candidates are deduplicated;
- at most five evidence lines are presented;
- child/adolescent/older-adult review gates remain active;
- population evidence does not change ranking, dose or eligibility;
- the UI shows the compact source abbreviation and its legend;
- adult and child scenarios rendered the expected DailyMed evidence;
- browser console errors: `0`.

## Automated Validation

- focused tests: `45` passed;
- complete test suite: `246` passed;
- Python compilation: passed;
- JavaScript syntax check: passed;
- Git whitespace validation: passed.

## Final Finding

Official-source acquisition and display coverage are complete for all catalogued
medications and canonical age bands. Therapeutic validation is intentionally not
claimed: every row remains display-only until population-, condition- and
formulation-specific clinical review authorizes a future runtime rule.
