# DM-067 — Authorized Question Engine execution

## Outcome

DecisionMEd can now orchestrate one registered Question Engine port only after
an external authority returns a matching authorization for the exact governed
input, trace, engine identity and contract version. The output is then validated
against the same input and recorded with metadata-only audit events.

## Fail-closed sequence

1. assess structural readiness for the selected registered engine;
2. verify an exact external authorization decision;
3. append an authorization audit event **before** calling the engine;
4. call the port once;
5. validate every field, Knowledge and Evidence reference in its result;
6. append either a result receipt summary or a safe rejection event.

An unavailable audit ledger prevents the engine call. A blocked readiness
report, mismatching or denied authorization, thrown engine error, or invalid
output never returns a result.

## Safety boundary

The orchestration introduces no engine implementation and no clinical rule.
Its tests use synthetic structural questions only. Audit records exclude prompt,
rationale and clinical observation values. A generated question is not a
diagnosis, recommendation, prescription or clinical authorization: all exposed
execution permission flags remain false. The real knowledge catalog is still
`draft` and cannot form a valid runtime input.

## Rollback

Revert the DM-067 commit. The change is isolated to authorization and
application orchestration contracts, their exports, tests and this document.
