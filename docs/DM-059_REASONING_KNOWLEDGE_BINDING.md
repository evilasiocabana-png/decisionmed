# DM-059 — Reasoning Knowledge binding

## Objective

Define an exact, specialty-scoped Knowledge and Evidence input binding for
future reasoning engines without making catalog metadata executable.

## Contract

`ReasoningKnowledgeBinding` requires a validated release identity, validated and
current `KnowledgeObject` values, and validated and current `EvidenceSource`
values. Every supplied source must apply to the specialty and the supplied set
must exactly match all knowledge evidence anchors.

The binding normalizes object order and calculates a deterministic SHA-256 over
complete Knowledge and Evidence metadata. Clinical and scientific text remains
outside its representation. The exact object and source identifiers remain
available for traceability.

## Current catalog state

The external `DecisionMEd-Knowledge` release inspected during this mission is
`0.10.0` with status `draft`. It correctly remains ineligible for this binding.
No status, source, or scientific content was changed.

## Safety limits

- release metadata does not authenticate the publisher or validator;
- a valid binding proves governed structure and current review metadata, not
  clinical correctness for an individual patient;
- no knowledge is translated into an executable rule;
- engine invocation, reasoning execution, and clinical execution remain false;
- no question, hypothesis, diagnosis, objective, strategy, or recommendation is
  generated.

The next mission may combine this binding with the DM-058 input envelope, but a
separate engine contract and validation gate remain required.

## Rollback

Remove the binding module, export, tests, and this document. No external catalog,
schema, endpoint, or persisted data changes.
