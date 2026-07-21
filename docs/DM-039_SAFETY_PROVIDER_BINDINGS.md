# DM-039 — Safety provider bindings

## Objective

Separate governed safety knowledge from technical provider coverage so that a
validated specification cannot be mistaken for an implemented check.

## Contract

`SafetyCheckProviderBinding` identifies a provider and the exact specification
version it claims to implement. `SafetyCheckProviderRegistry` accepts bindings
only for known, validated specifications and rejects duplicates.

`SafetyImplementationCoverage` partitions every specification into exactly one
state: compatible binding, missing binding, or incompatible binding. Coverage is
complete only when the specification set is non-empty and every version matches.

## Safety limits

- A binding is a descriptor, not executable code.
- This mission defines no evaluator and accepts no patient data.
- Complete structural coverage never authorizes clinical execution.
- A future evaluator must still implement the formal input/output port, preserve
  evidence traceability, pass clinical safety tests, and receive human review.

## Architecture

The change remains inside the Safety Layer and consumes its governed
specification registry. It adds no dependency on Application or Interface and
requires no new clinical entity or ADR.

## Rollback

Remove the provider module, exports, tests, and this document. Catalog schemas
and persisted data are unaffected.
