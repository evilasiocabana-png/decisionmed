# CTO Execution Protocol

## Objective

Define the mandatory reasoning order for executing PsychRx work after the CTO audit.

## Mandatory Execution Order

Before any mission, the agent must:

1. Identify the requested command.
2. Read `NEXT_MISSION.md`.
3. Read `PROJECT_STATUS.md`.
4. Read `PROJECT_TREE.md`.
5. Read `PROJECT_DEPENDENCIES.md`.
6. Read relevant ADRs.
7. Confirm the next mission is not already complete.
8. Confirm dependencies are satisfied.
9. Confirm no gate blocks execution.
10. Execute only the allowed scope.
11. Validate artifacts.
12. Update control documents.
13. Set the next correct mission.

## Command Interpretation

If the user says:

```text
EXECUTE PROGRAM A03
```

The agent must continue Program A03 from `NEXT_MISSION.md`, not from the beginning.

If the user says:

```text
CONTINUE ROADMAP
```

The agent must use the current state to select the next authorized mission.

If the user says:

```text
EXECUTE UNTIL GATE
```

The agent must continue missions in order until a baseline, gate, blocked dependency, failed validation or human decision point is reached.

## Stop Conditions

Stop immediately when:

- a dependency is missing;
- a gate is reached;
- a conflict appears;
- a mission would create prohibited clinical behavior;
- tests fail;
- JSON validation fails;
- `NEXT_MISSION.md` is ambiguous;
- the requested mission is out of order.

## Clinical Safety

The protocol never authorizes:

- prescription;
- autonomous clinical decision;
- recommendation without source and explanation;
- runtime consumption before publication gate;
- interface-level clinical logic.

## Declaration Final

The CTO Execution Protocol makes the project state-driven and prevents prompt drift.
