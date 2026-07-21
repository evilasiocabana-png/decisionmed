# DM-034 — Governed object review lifecycle

## Objective

Extend explicit review freshness from evidence sources to knowledge objects and
specialty form schemas. This is governance metadata only: no clinical rule,
recommendation, threshold, or executable behavior is introduced.

## Contract

- Catalog schema version is `6.0.0`.
- Every knowledge object and form schema declares `review_due_on` as an ISO date
  or `null`.
- A due date requires `reviewed_on` and must follow it.
- A `validated` object or schema requires a human validator, a review date, and
  a future due date.
- Draft records may remain unscheduled, but the knowledge readiness gate stays
  blocked.
- Derived states are `unscheduled`, `overdue`, `due_today`, and `current`.

No default interval is inferred. Review timing remains a human governance
decision.

## Surfaces and readiness

The form API exposes lifecycle metadata for the schema and each linked knowledge
object. The reference workflow displays it. Readiness counts overdue and
unscheduled objects and schemas, and fails closed with a specific reason.
Clinical execution remains disabled independently of metadata status.

## Migration and rollback

The platform and private catalog must move together to schema `6.0.0`. Rollback
must restore both repositories to the preceding compatible schema generation.
