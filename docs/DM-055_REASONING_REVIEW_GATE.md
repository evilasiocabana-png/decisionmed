# DM-055 — Reasoning review gate

## Objective

Allow the Reasoning Gate to recognize an exact, current safety-review record
without enabling any reasoning or clinical execution.

## Contract

`ReasoningGate.assess` accepts an optional `SafetyReviewRecord`. For a safety
assessment that is ready for human review, the record must match its exact
fingerprint and trace and cannot predate the clinical snapshot.

A validation disposition reaches only `SAFETY_REVIEW_RECORDED`, with the review
fingerprint carried in the result for traceability. A reassessment disposition
reaches `SAFETY_REASSESSMENT_REQUIRED`. Both states remain fail-closed.

Without a record, the existing `AWAITING_HUMAN_SAFETY_VALIDATION` state remains
unchanged. Reviews do not override incomplete, blocked, or human-review-required
safety states.

## Safety limits

- a review record is metadata and does not independently prove authentication;
- no reasoning engine, question, hypothesis, diagnosis, objective, strategy, or
  recommendation is added;
- no clinical rule or knowledge is introduced;
- reasoning and clinical execution remain false in every state.

The authorized and audited Application path from DM-054 remains the governed
producer of review records. A future mission must preserve that orchestration
boundary before any executable reasoning state can exist.

## Rollback

Remove the new gate states, optional review input, tests, and this document. No
schema, endpoint, catalog, or persisted data changes.
