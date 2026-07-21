# DM-062 — Reasoning schema binding

## Objective

Extend the governed Reasoning Knowledge binding with validated
`SpecialtyFormSchema` values so every future Question Engine `field_key` can be
traced to governed field meaning.

## Contract

`ReasoningKnowledgeBinding` now requires at least one validated, current schema
for the exact specialty. Schema IDs and workflow-step bindings are unique. Every
field must reference a Knowledge object already present in the binding.

Repeated `field_key` values across workflow steps are accepted only when their
complete definitions are identical. Conflicting labels, types, sections,
required flags, allowed values, or Knowledge references fail closed.

The schema and every field definition are included in the deterministic binding
fingerprint. `form_schema_ids` and normalized `field_keys` support future output
validation. Dynamic review currency now covers Knowledge, Evidence, and schemas.

## Safety limits

- a schema defines governed capture structure, not clinical logic;
- no interface rule, question-generation algorithm, or engine invocation is
  added;
- the real external catalog remains draft and ineligible;
- reasoning and clinical execution remain false.

The next mission can validate Question Engine fields, Knowledge IDs, and Evidence
IDs against this complete binding before any output is accepted.

## Rollback

Revert the required schema field, validation, fingerprint content, tests, and
this document together. No external catalog, endpoint, or persisted data changes.
