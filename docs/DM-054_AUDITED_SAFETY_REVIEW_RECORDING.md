# DM-054 — Audited safety-review recording

## Objective

Create the minimum Application flow that records a human safety review only
after an external authority decision matches the exact review request and the
result can be appended to the audit ledger.

## Contract

`SafetyReviewApplicationService` fingerprints the assessment, asks the
`SafetyReviewerAuthority` port for a decision, and rejects invalid, mismatched,
or denied responses. An authorized response must match the reviewer, authority
reference, trace, fingerprint, provider, and safety-review action.

The service then creates the immutable `SafetyReviewRecord` and appends bounded
technical metadata before returning it. Audit failure prevents an unaudited
record from escaping. Authority failures, denials, mismatches, and invalid review
inputs are also audit attempts and remain fail-closed.

## Safety limits

- no concrete identity or authorization adapter is added;
- rationale, findings, explanations, evidence, and clinical values are excluded
  from audit payloads;
- the in-memory ledger is not claimed as persistent or medico-legal storage;
- authorization permits only review recording, not clinical validation;
- reasoning and clinical execution remain false.

## Architecture

The orchestration stays in Application, the only layer in this flow that depends
on both Safety and Audit. Safety remains independent of identity and audit.

## Rollback

Remove the application service, export, tests, and this document. No schema,
catalog, endpoint, or persisted data changes.
