# Execution Protocol - PsychRx

## Status

Official operational governance document.

## Purpose

Define how Codex executes PsychRx programs, phases and missions through high-level commands while preserving clinical safety, scientific governance and project state.

This protocol reduces manual prompt dependency. Codex must resolve the current state from project control documents before acting.

## Supported Commands

```text
EXECUTE PROGRAM <PROGRAM_ID>
EXECUTE PHASE <PROGRAM_ID> <PHASE_ID>
EXECUTE MISSION <MISSION_ID>
EXECUTE UNTIL GATE
EXECUTE PHASE <PROGRAM_ID>-<PHASE_ID> AUTO
EXECUTE PROGRAM <PROGRAM_ID> AUTO
EXECUTE UNTIL BLOCK
CONTINUE ROADMAP
AUDIT PROJECT
VERIFY CURRENT STATE
AUDIT THEN EXECUTE
REPORT STATUS
BLOCK IF DEPENDENCY MISSING
```

## Mandatory Reading Order

Before execution Codex must read:

1. `governance/execution/PROJECT_CURRENT_STATE.md`
2. `governance/execution/NEXT_MISSION.md`
3. Relevant ADRs, only when the requested action changes architecture, gates or governance
4. Program, phase and mission documents directly related to the requested command

Historical control files remain valid, but they must not turn simple execution into repetitive paperwork.

## Execution Rule

Codex may execute the next mission resolved from the current project state or the next complete program package present in `codex/inbox/`.

High-level commands do not grant permission to skip sequence, bypass gates or execute blocked programs.

Automatic commands may continue across all missions of a complete inbox program package when dependencies, gates, tests, traceability and safety restrictions pass.

## Lean Blocking Rule

When a dependency is already known and registered, Codex must not create another blocker report that repeats the same finding.

For repeated commands that hit the same blocker, Codex must:

1. point to `governance/execution/PROJECT_CURRENT_STATE.md`;
2. preserve the same `governance/execution/NEXT_MISSION.md`;
3. avoid new governance artifacts;
4. explain the missing input in plain language.

New blocker reports are allowed only when the blocking condition is new, changes the roadmap, creates a safety risk or requires an ADR.

## Permanent Prohibitions

- Do not skip missions.
- Do not start blocked programs.
- Do not create new architecture outside an authorized mission.
- Do not create scientific content without an authorized mission.
- Do not execute clinical runtime.
- Do not generate prescriptions.
- Do not generate clinical recommendations.
- Do not consume scientific knowledge in runtime before publication and validation gates.

## Relationship With Existing X01 Documents

This document is the canonical entry point for Program X01. It is supported by:

- `docs/CTO_EXECUTION_PROTOCOL.md`
- `docs/EXECUTE_PROGRAM_PROTOCOL.md`
- `docs/PROGRAM_EXECUTION_GATE.md`
- `docs/MISSION_SUPERSEDENCE_POLICY.md`
- `docs/EXECUTION_COMMAND_REFERENCE.md`
- `docs/AUTO_EXECUTION_PROTOCOL.md`
- `docs/EXECUTE_PHASE_AUTO_RULES.md`
- `docs/EXECUTE_UNTIL_BLOCK_RULES.md`

## Current Authorized Next Use

```text
EXECUTE PROGRAM A05 AUTO
```

Complete program packages in `codex/inbox/` are sufficient operational authorization for full program execution. No separate pre-execution confirmation is required.

## Final Declaration

The Execution Protocol turns PsychRx execution into a state-driven process governed by status, dependencies, gates, inbox package order, tests, traceability and safety restrictions.


