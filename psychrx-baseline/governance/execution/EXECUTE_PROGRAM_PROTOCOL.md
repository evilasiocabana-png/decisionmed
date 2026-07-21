# Execute Program Protocol

## Command

```text
EXECUTE PROGRAM <PROGRAM_ID>
```

## Purpose

Execute a program from the current repository state until the next required gate.

## Inputs

Required:

- program ID;
- current `NEXT_MISSION.md`;
- program status file;
- dependency file;
- ADRs.

Optional:

- phase ID;
- sprint ID;
- stop condition.

## Execution Flow

```text
Read State
-> Verify Program
-> Verify Next Mission
-> Verify Dependencies
-> Execute Mission
-> Validate
-> Update Controls
-> Advance Next Mission
-> Repeat Until Gate
```

## Program Resolution Rules

If the requested program differs from `NEXT_MISSION.md`, the agent must not jump automatically.

It must determine whether:

- the requested program is blocked;
- the requested program is already complete;
- the current active program must finish first;
- an ADR authorizes a sequence change.

## Current Program Resolution

For current PsychRx state:

```text
EXECUTE PROGRAM A03
```

resolves to:

```text
A03-026 - INDICATION_MODELING
```

## Validation Requirements

Every cycle must validate:

- JSON parseability when JSON is created;
- tests when code or tested structures are touched;
- control document consistency;
- next mission correctness.

## Output

At the end of execution, report:

- missions executed;
- files created;
- files updated;
- validations;
- blockers;
- next mission;
- whether a gate was reached.

## Declaration Final

`EXECUTE PROGRAM` is the preferred command for continuing PsychRx work after Program X01.
