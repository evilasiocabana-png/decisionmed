# UX01 Click-First Clinical Workflow Specification

## Metadata

Project: PsychRx

Track: C - Clinical Experience Productization

Program: UX01 - Click-First Workflow

Mission: UX01-001 - CLICK_FIRST_WORKFLOW_DESIGN

Status: design_only

Runtime impact: none

Scientific content impact: none

## Objective

Define a click-first clinician workflow for PsychRx.

The experience must help the physician organize a consultation through structured selections, minimal free text, review checkpoints and non-prescriptive clinical organization.

PsychRx must remain a clinical reasoning support environment. It must not diagnose, prescribe, recommend treatment autonomously, select medications, or replace physician judgment.

## Design Principles

1. The physician remains the final reviewer and decision maker.
2. Structured selection is preferred when it improves speed, consistency and auditability.
3. Free text is preserved when clinical nuance matters.
4. The interface should organize the patient state, not force a diagnosis-first workflow.
5. Safety context must remain visible but non-autonomous.
6. Draft knowledge and unvalidated scientific content must never appear as clinical runtime guidance.

## Consultation Journey

```text
Patient context
-> Reason for visit
-> Current symptoms
-> Absent symptoms
-> Observed signs
-> Clinical stability
-> Current treatment
-> Treatment response
-> Safety review
-> Therapeutic objectives
-> Planned clinical direction
-> Monitoring plan
-> Final physician review
```

## Step 1 - Patient Context

Purpose:

Orient the consultation without making the software the source of clinical truth.

Structured selection:

- appointment type;
- follow-up or first visit;
- patient-reported change since last visit;
- current functional impact level.

Free text:

- brief contextual note;
- patient narrative opening.

## Step 2 - Reason For Visit

Purpose:

Capture why the patient is being seen today.

Structured selection:

- worsening symptoms;
- medication review;
- adverse effect concern;
- adherence issue;
- sleep complaint;
- anxiety complaint;
- mood complaint;
- functional decline;
- monitoring visit;
- other.

Free text:

- patient's own words.

## Step 3 - Current Symptoms

Purpose:

Capture present symptoms quickly and consistently.

Structured selection:

- depressed mood;
- anxiety;
- insomnia;
- anhedonia;
- irritability;
- psychomotor slowing;
- agitation;
- suicidal ideation to investigate;
- substance use to investigate;
- manic symptoms to investigate.

Structured intensity:

- absent;
- mild;
- moderate;
- severe;
- requires clarification.

Free text:

- symptom nuance;
- temporal pattern;
- patient-specific phrasing.

## Step 4 - Absent Symptoms

Purpose:

Prevent clinical reasoning from only accumulating positive findings.

Structured selection:

- denies suicidal ideation;
- denies manic symptoms;
- denies psychotic symptoms;
- denies substance use;
- denies medication adverse effects;
- denies adherence difficulty.

Free text:

- important negative findings requiring nuance.

## Step 5 - Observed Signs

Purpose:

Capture mental-state observations without turning them into automatic diagnosis.

Structured selection:

- psychomotor slowing;
- psychomotor agitation;
- pressured speech;
- reduced speech;
- tearfulness;
- restricted affect;
- anxious appearance;
- tangential thought;
- disorganized thought;
- sedation observed.

Free text:

- clinician observation note.

## Step 6 - Clinical Stability

Purpose:

Center the workflow around the current clinical state instead of diagnosis-first navigation.

Structured selection:

- stable;
- partially stable;
- unstable;
- relapse concern;
- remission;
- partial response;
- no response;
- clinical deterioration;
- requires urgent evaluation.

Free text:

- why this stability state was selected.

## Step 7 - Current Treatment

Purpose:

Organize current treatment without generating prescribing instructions.

Structured selection:

- no current psychopharmacological treatment;
- current medication present;
- dose known;
- dose unknown;
- adherence adequate;
- adherence uncertain;
- adherence poor;
- adverse effect present;
- response present;
- response partial;
- response absent.

Free text:

- medication details entered by physician;
- patient-reported response;
- adverse effect narrative.

## Step 8 - Safety Review

Purpose:

Ensure safety topics are visible before final review.

Structured selection:

- suicide risk to assess;
- aggression risk to assess;
- delirium/intoxication/withdrawal concern;
- pregnancy/lactation context;
- renal/hepatic impairment context;
- cardiovascular/QT context;
- epilepsy/seizure context;
- interaction concern;
- allergy or severe prior reaction.

Free text:

- safety note;
- reason for escalation;
- reason for urgent referral consideration.

## Step 9 - Therapeutic Objectives

Purpose:

Capture what the physician is trying to improve, without recommending how to treat.

Structured selection:

- improve sleep;
- reduce anxiety;
- improve mood;
- improve energy;
- reduce adverse effects;
- improve adherence;
- improve function;
- monitor before changing;
- clarify diagnosis/context.

Free text:

- individualized objective.

## Step 10 - Planned Clinical Direction

Purpose:

Record the physician's intended direction without generating prescriptions.

Structured selection:

- maintain current plan;
- monitor before changing;
- investigate further;
- review medication;
- consider adjustment;
- consider substitution;
- consider association;
- consider gradual discontinuation;
- refer or escalate care.

Free text:

- physician rationale;
- shared decision-making note.

## Step 11 - Monitoring Plan

Purpose:

Organize follow-up targets.

Structured selection:

- mood;
- anxiety;
- sleep;
- appetite/weight;
- libido/sexual function;
- sedation;
- adherence;
- functioning;
- adverse effects;
- safety symptoms;
- return interval: 2 weeks;
- return interval: 4 weeks;
- return interval: 6 weeks;
- return interval: 3 months.

Free text:

- monitoring details;
- patient instructions written by physician.

## Step 12 - Final Physician Review

Purpose:

Make explicit that PsychRx organizes information but does not decide conduct.

Checklist:

- patient state reviewed;
- symptoms reviewed;
- absent symptoms reviewed;
- safety reviewed;
- treatment context reviewed;
- objectives reviewed;
- monitoring reviewed;
- final plan reviewed by physician.

Required final action:

```text
Physician confirms final review.
```

## Reusable Interface Components

### Clinical Stepper

Shows the consultation journey and progress.

### Clinical Selection Group

Reusable component for structured options.

### Severity Selector

Captures symptom intensity.

### Safety Review Panel

Always-visible safety checklist.

### Patient State Summary

Summarizes the current clinical state using selected fields and physician notes.

### Physician Review Panel

Final confirmation that the physician reviewed and owns the plan.

### Free Text Note

Minimal free-text component for nuance.

### Missing Information Prompt

Displays incomplete fields without forcing diagnosis or treatment.

## Low-Fidelity Flow

```text
[Patient Context]
       |
       v
[Reason For Visit]
       |
       v
[Symptoms] ----> [Absent Symptoms]
       |               |
       v               v
[Observed Signs] -> [Clinical Stability]
       |
       v
[Current Treatment]
       |
       v
[Safety Review]
       |
       v
[Objectives]
       |
       v
[Planned Clinical Direction]
       |
       v
[Monitoring]
       |
       v
[Final Physician Review]
```

## Explicit Non-Goals

UX01 does not create:

- diagnosis automation;
- prescribing automation;
- medication selection;
- dosing suggestions;
- therapeutic recommendation;
- clinical runtime execution;
- scientific knowledge population;
- patient-specific medical advice.

## Acceptance Criteria Mapping

| Criterion | Status |
| --- | --- |
| UX01 registered as design-only program | satisfied |
| Click-first workflow specification exists | satisfied |
| Physician remains final reviewer and decision maker | satisfied |
| Runtime files unmodified | satisfied |
| Scientific files unmodified | satisfied |

## Declaration

UX01 defines a click-first consultation workflow for PsychRx as a design-only Clinical Experience program. It organizes clinical information for physician review and does not automate diagnosis, prescribing, treatment selection or clinical decisions.
