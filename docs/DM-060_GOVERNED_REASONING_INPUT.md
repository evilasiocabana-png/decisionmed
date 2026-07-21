# DM-060 — Governed Reasoning input

## Objective

Compose the exact clinical envelope from DM-058 with the governed Knowledge and
Evidence binding from DM-059 while preserving a non-executable boundary.

## Contract

`GovernedReasoningInput` requires matching specialties, valid temporal ordering,
and Knowledge/Evidence reviews that remain current at assembly time. It combines
the snapshot, Safety assessment, safety review, gate, catalog, Knowledge, and
Evidence fingerprints into one deterministic SHA-256 identity.

Scientific content and clinical values remain outside the representation. The
composition exposes only identifiers and fingerprints needed for traceability.

`ReasoningKnowledgeBinding.review_current` is evaluated dynamically. A binding
that was valid when created becomes incomplete after any Knowledge or Evidence
review expires.

## Safety limits

- the real external catalog remains draft and cannot produce this input;
- no engine contract or implementation exists in this mission;
- `engine_contract_present`, engine invocation, reasoning execution, and
  clinical execution remain false;
- no clinical rule, question, hypothesis, diagnosis, objective, strategy, or
  recommendation is generated.

The next mission may define the structural Question Engine port and output
contract. A concrete implementation remains prohibited until governed content,
engine identity, output validation, and audit orchestration are all present.

## Rollback

Remove the governed input module, export, tests, and this document, and restore
the previous static binding-completeness property. No catalog, endpoint, schema,
or persisted data changes.
