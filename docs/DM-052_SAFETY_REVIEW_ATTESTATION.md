# DM-052 — Safety review attestation

## Objective

Define an immutable human-review attestation bound to the exact safety
assessment reviewed, without treating metadata alone as authenticated authority.

## Contract

`safety_assessment_fingerprint` creates a deterministic SHA-256 digest over the
complete assessment, including outcomes, explanations, evidence references,
findings, missing checks, reasons, and trace.

`SafetyReviewRecord` stores only the digest and bounded review metadata. It can
record validation for reasoning review only when the assessment was
`READY_FOR_HUMAN_REVIEW`; blocked or incomplete assessments can only be returned
for reassessment. Any assessment content change invalidates the match.

## Safety limits

- the record does not authenticate the reviewer or authority workflow;
- it does not copy clinical explanations, findings, or evidence into review
  metadata;
- it does not unlock reasoning or clinical execution by itself;
- no clinical rule, recommendation, endpoint, or persistence is added.

Authentication, authorization, append-only audit, and Reasoning Gate integration
remain separate required missions.

## Rollback

Remove the review module, export, tests, and this document. No schema, catalog,
or persisted data changes.
