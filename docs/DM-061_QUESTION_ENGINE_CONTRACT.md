# DM-061 — Question Engine contract

## Objective

Define the structural input, output, state, identity, traceability, and failure
contracts required before any concrete Question Engine implementation.

## Contract

`QuestionEngine` is a runtime-checkable port that receives only a
`GovernedReasoningInput`. It has no implementation in this mission.

`QuestionEngineItem` represents a Reasoning output record rather than a new
Domain entity. Every item requires a canonical target field, required or
conditional classification, contiguous priority rank, rationale, governed
Knowledge IDs, Evidence IDs, trace, and exact input fingerprint.

`QuestionEngineResult` supports the official states `COLLECTION_PENDING`,
`COLLECTION_SUFFICIENT`, and `UNCERTAINTY_PERSISTS`. It enforces unique ordered
questions, explicit open gaps, input identity, engine identity, and an overall
explanation.

## Safety limits

- no concrete engine, registry, adapter, or application invocation is added;
- no clinical prioritization algorithm or hardcoded question is introduced;
- tests use synthetic structural prompts only;
- the real external catalog remains draft;
- Question outputs do not diagnose, prescribe, recommend, or authorize clinical
  action;
- reasoning and clinical execution remain false.

Before a concrete engine can run, future missions still require engine
registration, exact Knowledge subset validation, output validation against the
input binding, audited orchestration, and clinical/scientific validation.

## Rollback

Remove the Question Engine contract module, export, tests, and this document. No
catalog, ontology, endpoint, schema, or persisted data changes.
