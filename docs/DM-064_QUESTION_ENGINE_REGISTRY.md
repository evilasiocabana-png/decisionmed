# DM-064 — Question Engine registry

## Outcome

DecisionMEd now has an identity-only registry for future Question Engine ports.
An engine can be registered only when its id, provider and contract version
exactly match an approved immutable binding.

## Safety boundary

Registration never invokes `generate` and approves no clinical content. The
binding and registry explicitly keep engine, reasoning and clinical execution
disabled. A complete registry means identity coverage only; it is not runtime
readiness.

## Rollback

Revert the DM-064 commit. The change is isolated to one registry module, its
exports, tests and this document.
