# Program Execution Plan Protocol - PsychRx

## Purpose

This document defines the mandatory execution bridge between a Program and Codex.

PsychRx must not rely on conversational memory to decide how a Program is executed.

## Simple Execution Chain

```text
Track
-> Program
-> Program Execution Plan
-> Codex
```

## Relationship To Full Hierarchy

The full governance hierarchy remains:

```text
Vision
-> Track
-> Program
-> Phase
-> Sprint
-> Mission
-> Task
```

The Program Execution Plan is the operational contract that translates a Program into executable Phases, Sprints, Missions and Tasks.

## Mandatory Rule

Every executable Program must have a Program Execution Plan before Codex changes project files.

If a Program Execution Plan is missing, Codex must stop and create or request the plan before executing the Program.

## Program Execution Plan Contents

Every Program Execution Plan must define:

- Track ID.
- Program ID.
- Program objective.
- Scope.
- Out-of-scope items.
- Dependencies.
- Gates.
- Phases.
- Sprints.
- Missions.
- Tasks.
- Acceptance criteria.
- Validation commands.
- Files or artifact families allowed.
- Files or artifact families prohibited.
- Status-update requirements.
- Completion report requirements.

## Codex Consumption Rule

Codex must read the Program Execution Plan before executing any Program.

The plan is the executable contract for:

- what to create;
- what to update;
- what to validate;
- what to prohibit;
- when to stop;
- when to mark the Program complete.

## Missing Plan Behavior

If the user requests:

```text
EXECUTE PROGRAM <ID>
```

and the Program Execution Plan does not exist, Codex must not improvise execution.

Codex may create the Program Execution Plan only when the requested Program scope is sufficiently clear and does not conflict with existing governance.

## Permanent Prohibitions

No Program Execution Plan can authorize:

- autonomous diagnosis;
- prescription;
- therapeutic recommendation;
- dose suggestion;
- patient-specific medication selection;
- clinical runtime activation;
- patient data processing;
- production deployment;
- regulatory compliance claim;
- certification claim;
- release authorization.

Those capabilities require separate future governance, safety, evidence and certification gates.

## Declaration

The Program Execution Plan is the official bridge between Program and Codex. Codex should not need to ask how to execute when a valid Program Execution Plan exists.

