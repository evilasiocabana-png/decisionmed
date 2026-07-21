# Program-Centric Execution Model

## Purpose

This document defines Program as the primary user-facing execution unit of the PsychRx Project Operating System.

It is governance-only. It does not define clinical content, runtime behavior, scientific claims, recommendations or prescriptions.

## User-Facing Rule

The founder should be able to request work at Program level:

```text
EXECUTE PROGRAM A04
EXECUTE PROGRAM 10
NEXT PROGRAM
CONTINUE PROGRAM
```

The user does not need to provide internal paths, individual mission files or repository implementation details.

## Responsibilities

### User

- Approves Programs.
- Sets priority between Programs when governance permits.
- Reviews blockers and gates when Codex cannot continue.

### CTO

- Decomposes Programs into Phases, Sprints and Missions.
- Defines dependencies, gates and acceptance criteria.
- Resolves conflicts between roadmap, governance and execution state.
- Approves scope changes when a Program requires restructuring.

### Codex

- Reads the official project state.
- Resolves the active Program.
- Executes authorized Missions and Tasks in sequence.
- Stops at gates, blockers, failed tests or scope conflicts.
- Updates state files and execution reports.

## Execution Resolution

When the user asks for a Program-level action, Codex must resolve:

```text
Program
-> Phase
-> Sprint
-> Mission
-> Task
```

from repository state, not chat memory.

Required state files:

1. `governance/PROJECT_STATE.md`
2. `governance/execution/EXECUTION_STATE.json`
3. `governance/execution/NEXT_MISSION.md`
4. `governance/execution/NEXT_BLOCK.md`
5. `governance/MASTER_ROADMAP.md`

## Backward Compatibility

Mission-level commands remain valid:

```text
EXECUTE MISSION A04-011
```

Phase-level commands remain valid:

```text
EXECUTE PHASE A04 MECHANISM_POPULATION
```

However, if a Program-level command and a Mission-level command conflict, the official repository state prevails.

## Stop Conditions

Codex must stop if:

- the next mission is outside the active Program;
- dependencies are missing;
- tests fail;
- JSON validation fails;
- a gate requires review;
- scientific interpretation exceeds the authorized scope;
- runtime, prescription, recommendation or clinical decision boundaries are touched.

## Current Active Program

```text
Program A04 - Scientific Content Population: SNRIs
```

Current scientific mission:

```text
A04-011 - SNRI_MECHANISM_POPULATION
```

Current governance mission completed by this document:

```text
R03-003 - PROGRAM_CENTRIC_EXECUTION_MODEL
```

## Declaration

Program is the primary user-facing execution unit. Mission remains the smallest governed executable unit.
