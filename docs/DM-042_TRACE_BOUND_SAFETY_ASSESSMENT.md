# DM-042 — Trace-bound safety assessment

## Objective

Prevent structural safety results from different runs from being combined into
one assessment.

## Contract

Every `SafetyCheckResult.trace_id` must exactly match the assessment trace.
Mixed traces are rejected before aggregation with `safety.trace_mismatch`.

## Safety limits

This is an integrity check only. It adds no patient data, evaluator, clinical
rule, recommendation, runtime capability, or clinical execution permission.

## Rollback

Remove the trace equality check and its test. No schema or persisted data changes.
