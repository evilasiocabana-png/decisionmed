# DM-058 — Reasoning input envelope

## Objective

Define the first complete input contract owned by the Reasoning Layer, binding
the exact Clinical Snapshot, Safety assessment, human review, and deterministic
Reasoning Gate result without invoking a clinical engine.

## Contract

`ReasoningInputEnvelope.prepare` recomputes the gate from its inputs and accepts
only `SAFETY_REVIEW_RECORDED`. The immutable envelope validates canonical
identity, semantic contract version, producer metadata, and temporal ordering.
Snapshot content, safety explanations, review rationale, and other clinical data
are excluded from its representation.

The envelope exposes exact snapshot and assessment fingerprints for future
traceability. It explicitly reports knowledge binding incomplete and engine
invocation, reasoning execution, and clinical execution as false.

## Safety limits

- producer metadata is descriptive and does not authenticate an adapter;
- no Knowledge or Evidence object is attached yet;
- no Question Engine or other clinical engine implementation is added;
- no question, hypothesis, objective, strategy, diagnosis, explanation, or
  recommendation is generated;
- the governed DM-054 Application flow remains the intended review producer.

The next mission must define a governed Knowledge/Evidence input binding before
any engine port can be considered invocable.

## Architecture

The envelope lives in Reasoning and depends only on allowed Domain and Safety
contracts. It has no Application, Interface, Audit, persistence, or framework
dependency.

## Rollback

Remove the envelope module, export, tests, and this document. No schema,
endpoint, catalog, or persisted data changes.
