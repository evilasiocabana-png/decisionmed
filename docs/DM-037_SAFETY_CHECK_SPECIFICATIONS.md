# DM-037 — Governed safety-check specifications

## Objective

Create a governed metadata contract for future safety checks before any
patient-specific evaluator or clinical rule is introduced.

## Contract

`SafetyCheckSpecification` declares a canonical identifier, specialty, purpose,
limits, evidence-source identifiers, semantic version, lifecycle status, human
review metadata, and next-review date. A validated specification requires a
future review date.

`SafetyCheckRegistry` fails closed when evidence is missing, does not declare the
same specialty, or is not validated for a validated specification. Registration
is deterministic and independent from interfaces and application orchestration.

## Safety limits

- A specification is metadata, not an evaluator.
- It accepts no patient data and produces no `SafetyFinding`.
- It contains no contraindication, interaction, threshold, or clinical rule.
- It is never runtime eligible and never authorizes clinical execution.
- Future executable checks still require sourced knowledge, implementation,
  clinical tests, human scientific review, and regulatory validation.

## Architecture

The Safety Layer depends only on the Evidence Layer in this increment, as
allowed by the PsychRx layer rules and ADR 0014. No new clinical entity or ADR is
required.

## Rollback

Remove the two specification/registry modules, their exports, tests, and this
document. No catalog schema or persisted data is changed.
