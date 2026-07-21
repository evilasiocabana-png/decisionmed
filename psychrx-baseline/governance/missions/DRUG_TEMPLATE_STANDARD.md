# Drug Template Standard

## Purpose

Define the minimum structure required for reusable SSRI templates in Program A03.

## Required Metadata

Every template must contain:

- `schema`;
- `program`;
- `mission`;
- `template_name`;
- `schema_version`;
- `document_version`;
- `status`;
- `creation_date`;
- `last_revision`;
- `author`;
- `editorial_status`;
- `scientific_status`;
- `publication_status`.

## Required Governance Flags

Every template must explicitly declare:

- `scientific_content_populated: false`;
- `clinical_content_interpreted: false`;
- `source_content_interpreted: false`;
- `drug_profile_created: false`;
- `runtime_consumption_allowed: false`.

## Payload Rule

`template_payload` must remain empty until a future mission explicitly authorizes field-level scientific modeling.

## Prohibited Use

Templates cannot be used as:

- validated scientific content;
- Drug Profiles;
- clinical recommendations;
- runtime objects;
- evidence classification records.

## Declaration Final

The template standard guarantees structural consistency. It does not authorize scientific population.
