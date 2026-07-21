# DM-033 — Evidence review lifecycle

## Objective

Make evidence review freshness explicit and fail closed when its schedule is
missing or overdue. This mission changes governance metadata only; it adds no
clinical rule, recommendation, threshold, or runtime execution.

## Contract

- Catalog schema version is `5.0.0`.
- Every evidence source declares `review_due_on` as an ISO date or `null`.
- A due date must be later than `reviewed_on`.
- Evidence with status `validated` requires a future due date.
- Draft evidence may remain unscheduled, but readiness reports
  `review_schedule_missing` and stays blocked.
- Derived review states are `unscheduled`, `overdue`, `due_today`, and
  `current`.

No default review interval is inferred. Choosing that interval is a human
governance decision and must not be invented by the platform.

## Surfaces

The form-schema API exposes `review_due_on` and `review_state`. The generic
workflow displays the next review, and the readiness report counts overdue and
unscheduled sources. Clinical execution remains disabled independently of all
catalog statuses.

## Migration and rollback

The platform and private knowledge catalog must move together to schema
`5.0.0`. Rollback must restore both repositories to their preceding compatible
schema versions; mixing schema generations is rejected by the loader.
