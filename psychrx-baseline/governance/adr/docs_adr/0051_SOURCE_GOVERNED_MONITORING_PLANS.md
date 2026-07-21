# ADR 0051 - Source-Governed Monitoring Plans

## Status

Accepted for implementation on 2026-07-20 by founder request.

## Context

Program 27 identified four monitoring concerns with authoritative guideline
anchors but with `runtime_eligible=false`: antidepressant withdrawal, lithium,
antipsychotic movement disorders and antipsychotic metabolic risk.

The permanent safety boundary prohibits autonomous clinical alerts and
prescribing. At the same time, hiding a source-validated monitoring checklist
would leave relevant information unavailable during physician review.

## Decision

Authorize the four concerns below as source-governed, non-prescriptive
`MonitoringPlan` prompts:

- `TPC-005` - antidepressant withdrawal monitoring;
- `TPC-012` - lithium monitoring;
- `TPC-014` - antipsychotic movement-disorder monitoring;
- `TPC-015` - antipsychotic metabolic monitoring.

Runtime eligibility requires all of the following:

1. an authoritative `EvidenceSource` with a section-level anchor;
2. scientific review recorded as `verified_against_official_guideline`;
3. editorial review recorded as `approved_for_non_prescriptive_runtime`;
4. publication state `published_monitoring_knowledge_object`;
5. `runtime_eligible=true` in both the theory-to-practice matrix and the
   monitoring publication table;
6. a matching patient-state trigger.

## Runtime Scope

The authorized output may:

- list information or measurements to review;
- reproduce guideline monitoring intervals in an informational checklist;
- show the source identifier, section and URL;
- make missing monitoring data visible for physician review.

It may not:

- diagnose an adverse reaction;
- prescribe, stop or change a medicine;
- calculate a taper or dose;
- choose a medicine;
- issue an autonomous emergency instruction;
- claim that completion of a checklist makes treatment safe.

## Trigger Boundary

- `TPC-005` requires a clinician-selected `taper_or_withdraw` action and a
  current antidepressant.
- `TPC-012` requires lithium in the current medication list.
- `TPC-014` and `TPC-015` require a current antipsychotic.

Drug-class detection is metadata lookup only. It does not infer diagnosis or
indication.

## Scientific Sources

- NICE NG222, recommendations 1.4.12-1.4.21;
- NICE CG185, recommendations 1.10.14-1.10.24;
- NICE CG178, recommendations 1.3.5.1-1.3.6.5.

## Consequences

The four rules become visible only when relevant, with citations and explicit
non-prescriptive limits. All other theory-to-practice rules remain inactive.
Pharmacological rows pending formal review remain ineligible; this ADR does not
mass-promote interaction, disease-use, dose-range or Motor 2 content.

## Rollback

- tag `restore/pre-scientific-promotion-20260720-27a4750`;
- branch `codex/restore-pre-scientific-promotion-20260720`;
- bundle `C:\Users\evcab\PsychRx_pre_scientific_promotion_20260720_27a4750.bundle`.

## Declaration Final

PsychRx may present source-governed monitoring knowledge to support physician
review. The physician remains the final decision-maker, and no autonomous
clinical alert, diagnosis, prescription or dose operation is authorized.
