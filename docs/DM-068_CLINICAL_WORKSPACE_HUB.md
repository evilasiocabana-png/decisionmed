# DM-068 — Clinical workspace hub

## Outcome

The local DecisionMEd home page now presents an independent clinical workspace
shell: platform readiness, catalog state, specialty count, governed schema
count, technical gates and specialty entry points are visible at a glance.

## Safety boundary

The hub consumes only the existing read-only app-state endpoint. It never
accepts, stores, displays or infers patient values. Every specialty remains
explicitly constrained by its governed scope and the page keeps clinical
execution blocked.

## Rollback

Revert the DM-068 commit. This change is limited to the local hub presentation,
its regression assertion and this document.
