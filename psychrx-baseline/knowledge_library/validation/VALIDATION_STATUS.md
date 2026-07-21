# Knowledge Validation Status

## Status Values

- `draft`
- `awaiting_review`
- `validated`
- `conflicting_evidence`
- `deprecated`
- `archived`

## Transition Rules

- `draft` may move to `awaiting_review` only after metadata completion.
- `awaiting_review` may move to `validated` only after human scientific validation.
- `conflicting_evidence` cannot feed engines.
- `deprecated` and `archived` cannot feed engines.
- No draft content can become a recommendation automatically.
