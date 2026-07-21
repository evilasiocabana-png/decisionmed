# DM-051 — Reasoning safety gate

## Objective

Create the first Reasoning Layer contract and make Safety a mandatory,
trace-bound prerequisite before any future reasoning engine.

## Contract

`ReasoningGate` consumes an immutable `ClinicalSnapshot` and `SafetyAssessment`
from the same trace. It distinguishes incomplete snapshots, incomplete safety,
blocked safety, and safety findings requiring human review.

Even `READY_FOR_HUMAN_REVIEW` safety reaches only
`AWAITING_HUMAN_SAFETY_VALIDATION`; no reasoning execution state exists yet.

## Safety limits

- no question, hypothesis, diagnosis, objective, strategy, comparison, or
  recommendation is generated;
- no clinical knowledge or algorithm is introduced;
- no interface or application binding is added;
- reasoning and clinical execution remain false in every state.

## Architecture

The new Reasoning package depends only on allowed Domain and Safety contracts.
It does not access Application, Interface, persistence, or patient identifiers.

## Rollback

Remove the Reasoning package, tests, and this document. No schema, catalog, or
persisted data changes.
