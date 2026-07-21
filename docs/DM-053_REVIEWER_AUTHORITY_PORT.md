# DM-053 — Reviewer authority port

## Objective

Define the minimum Application contract required to ask an external identity
and authorization adapter whether a reviewer may record a safety attestation.

## Contract

`SafetyReviewerAuthority` is a runtime-checkable port with no concrete
implementation. Its decision is immutable and bound to the reviewer, authority
reference, safety-review action, assessment trace, and exact assessment
fingerprint.

An authorized decision permits only the future recording of the matching
review. A denied or mismatched decision remains fail-closed. Neither state
permits reasoning or clinical execution.

## Safety limits

- no user, credential, role, or identity provider is invented;
- no concrete authentication or authorization adapter is supplied;
- the decision contains bounded technical metadata only;
- authorization does not validate clinical content;
- no endpoint, persistence, reasoning, or clinical execution is added.

The next mission may orchestrate this port with the review record and append-only
audit, rejecting denials and mismatched decisions before returning a record.

## Architecture

The port belongs to Application. Future infrastructure may implement it without
adding identity dependencies to Safety.

## Rollback

Remove the port module, export, tests, and this document. No schema, catalog, or
persisted data changes.
