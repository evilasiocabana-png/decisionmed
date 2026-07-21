# Knowledge Layer Baseline

## Baseline

Sprint 8, Mission 070 freezes the first infrastructure baseline of the Knowledge Layer.

## Included

- Knowledge package structure.
- Base `KnowledgeObject`.
- Knowledge lifecycle status values.
- Version primitives and version history.
- Repository abstraction contract.
- Loader abstraction contract.
- Structural validator.
- Guideline schema model without content.
- Evidence schema model without content.
- Knowledge test helpers.
- Structural and contract tests.

## Explicitly Excluded

- real guidelines;
- real psychopharmacological agents;
- real evidence entries;
- clinical recommendations;
- therapeutic rules;
- AI loading;
- PDF importing;
- parsing;
- database persistence;
- ORM integration;
- clinical engines;
- clinical decisions.

## Architecture Review

The baseline preserves the required separation between:

- scientific content;
- structured knowledge objects;
- execution logic;
- future clinical reasoning.

The Knowledge Layer remains technology-independent and contains no concrete persistence implementation.

## Sprint 9 Gate

ADR-0002 is accepted. The official decision is to separate platform and scientific knowledge.

Sprint 9 must populate scientific content only in `psychrx-knowledge` or in a formally isolated equivalent area prepared for extraction into that repository.
