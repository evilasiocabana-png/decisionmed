# JSON Template Standard

## Purpose

Define JSON consistency rules for Program A03 templates.

## Format

All templates must be valid JSON and must preserve:

- stable schema naming;
- explicit version fields;
- explicit status fields;
- explicit governance flags;
- empty payloads before authorized scientific modeling.

## Versioning

Initial template versions use:

```text
0.1.0
```

Future changes must update both:

- `schema_version`;
- `document_version`.

## Status Values

Current status:

```text
empty_template_metadata_only
```

This means the template is structurally available but contains no scientific field values.

## Validation Expectations

Template validation must confirm:

- JSON parseability;
- required metadata fields;
- absence of populated scientific payload;
- absence of runtime authorization.

## Declaration Final

JSON templates are structural contracts for future work. They are not scientific content.
