# DM-056 — Clinical Snapshot fingerprint

## Objective

Create a deterministic SHA-256 fingerprint for the complete pseudonymous
`ClinicalSnapshot`, so later Safety and Reasoning contracts can prove that they
refer to the exact same clinical input rather than only sharing a trace ID.

## Contract

`clinical_snapshot_fingerprint` covers snapshot, lineage, subject and session
references, specialty, timestamps, every observation and its provenance,
previous snapshot lineage, trace, and contract version.

Observation order is normalized by immutable observation ID because ordering is
not clinical meaning. Primitive value types are encoded explicitly, so boolean
and integer values cannot collide. Timestamps are normalized to UTC with
microsecond precision.

`ClinicalSnapshot.content_fingerprint` exposes only the 64-character digest; it
does not expose clinical values or direct identifiers.

## Safety limits

- this mission does not alter Safety or Reasoning behavior yet;
- a fingerprint proves content identity, not clinical correctness or validation;
- no clinical rule, inference, question, diagnosis, or recommendation is added;
- clinical execution remains false.

The next mission must bind safety results and assessments to this fingerprint
before a reasoning input contract is introduced.

## Rollback

Remove the fingerprint function, property, export, tests, and this document. No
schema, endpoint, catalog, or persisted data changes.
