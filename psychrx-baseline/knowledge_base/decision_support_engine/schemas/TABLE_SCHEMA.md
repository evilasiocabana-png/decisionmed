# Decision Support Engine Table Schema

## `medication_strategy_table.csv`

Required columns:

- `drug_id`
- `drug_name`
- `drug_class`
- `targets`
- `usual_adult_range`
- `source_id`
- `source_title`
- `source_section`
- `source_url`
- `cautions`
- `substitution_fit`
- `association_fit`
- `status`

## `decision_rules.csv`

Required columns:

- `rule_id`
- `priority`
- `safety_state`
- `stability`
- `has_current_medication`
- `response_state`
- `tolerability`
- `impairment_required`
- `output_action`
- `output_summary`
- `required_fields`
- `blocked_if_missing`

## `question_derivation_matrix.csv`

Required columns:

- `field_id`
- `field_label`
- `question_text`
- `input_type`
- `allowed_values`
- `priority`
- `required_for_actions`
- `unlocks`
- `blocking_if_missing`

## `safety_gate_questions.csv`

Required columns:

- `safety_field`
- `question_text`
- `safe_values`
- `blocking_values`
- `engine_behavior_if_blocked`
- `priority`

## Validation Expectations

- Every rule field in `required_fields` must exist in `question_derivation_matrix.csv`.
- Every medication source must include a source URL.
- Every candidate used for substitution or association must have a source ID.
- Every safety field must be asked before strategy output.

## Evidence Preparation Tables

### `theory_to_practice_matrix.csv`

Required lineage columns:

- `didactic_source`
- `didactic_pages`
- `theoretical_concern`
- `required_app_inputs`
- `motor_check`
- `official_source_id`
- `official_source_section`
- `official_source_url`
- `validation_status`
- `runtime_eligible`

### `medication_official_claims.csv`

Each medication row may contain short review anchors for indication, dosage, mechanism, warnings and interactions. The source URL, locator, extraction status, editorial status and content checksum are mandatory. Extracted text is a candidate for normalization, not a published knowledge object.

### `medication_disease_use_evidence_review.csv`

Each original disease-use relationship is preserved and receives an official indication match, evidence review status, next review action and `runtime_eligible=false`.

### `motor2_gap_resolution_matrix.csv`

Each Motor 2 relationship is classified as one of:

- existing local value preserved;
- official source anchor extracted, normalization pending;
- guideline or off-label review required;
- no supported relationship registered, do not invent a value.

Missing clinical ranges must never be populated solely from a generic product dosage section. Condition, indication, formulation and population must be normalized and reviewed first.

### `medication_population_evidence.csv`

Each of the 83 medications must have exactly one row for each canonical age
band: `CHILD`, `ADOLESCENT`, `ADULT` and `OLDER_ADULT`.

Required traceability columns:

- `source_system`, `source_abbreviation`, `source_title`, `source_version`;
- `source_date`, `source_url`, `source_locator`, `population_anchor`;
- `population_summary`, `dosage_anchor`, `dosage_summary`;
- `evidence_status`, `scientific_review_status`, `editorial_status`;
- `display_eligible`, `therapeutic_runtime_eligible`, `content_sha256`.

Official source excerpts may be displayed for physician review when
`display_eligible=true`. They must not alter ranking, choose a medicine or
authorize a population-specific dose while `therapeutic_runtime_eligible=false`.
