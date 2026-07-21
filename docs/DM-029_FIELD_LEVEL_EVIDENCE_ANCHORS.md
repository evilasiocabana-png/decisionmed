# DM-029 — Field-level evidence anchors

## Outcome

Catalog schema `4.0.0` requires every knowledge object to identify the exact
source section that supports it. A broad bibliography entry is no longer
sufficient.

Each immutable `EvidenceAnchor` contains:

- `source_id`: governed `EvidenceSource` identifier;
- `section`: human-readable section, table, figure, or recommendation label;
- `locator`: direct public location for verification.

`KnowledgeObject.evidence_source_ids` is derived from its anchors, preventing
the source list and source locations from diverging. Multiple distinct anchors
may point to the same source. Empty or duplicate anchors fail closed.

## Interface

The read-only form API returns an `anchors` array inside each evidence source.
The workflow page displays every specific section as an external link before
the source metadata. Anchors remain reference-only and never authorize clinical
execution.

## Migration and rollback

Catalog v3 records must replace `evidence_source_ids` with `evidence_anchors`.
The loader rejects v3 after this change. Rollback requires restoring the v3
platform loader and its matching catalog release together; mixed versions fail
closed.

## Verification

- Contract and loader tests cover immutability, exact anchor fields, duplicate
  rejection, source derivation, and unknown-source rejection.
- API tests verify section, locator, and non-runtime status.
- The complete DecisionMEd and inherited PsychRx test suites must remain green.
