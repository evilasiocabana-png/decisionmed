# 618 - P0 Safety UI and Runtime Integration

## Objective

Connect explicit safety assessment to the consultation workflow and the local
rule table without moving clinical logic into the interface.

## Implementation

- added the `Seguranca essencial` consultation card;
- added explicit states: not assessed, denied after assessment, present, unknown
  and not applicable;
- added structured suicide-detail fields for plan, intent, means access and recent
  attempt;
- removed automatic inference of suicide, mania and substances as denied;
- added essential-safety completeness to navigation and request readiness;
- connected the local rule table to `ClinicalSafetyAssessmentService`;
- updated simulated cases so their safety state is explicit.

## Boundaries

- suicide-detail fields record context but do not calculate a risk score;
- the UI does not decide whether a risk is absent;
- the motor blocks or requests investigation; it does not prescribe a response;
- acute toxidrome triage remains separate and source-anchored.

## Declaration Final

The UI now collects safety meaning explicitly and the Application Layer owns the
structural blocking decision.
