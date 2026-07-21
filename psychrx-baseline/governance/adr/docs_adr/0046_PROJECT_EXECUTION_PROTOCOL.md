# ADR 0046 - Project Execution Protocol

## Status

Accepted.

## Date

2026-07-01

## Context

The PsychRx audit concluded that the main bottleneck is no longer architecture, but execution orchestration.

The project has mature governance, stable tests and a large roadmap. Manual prompt-by-prompt execution is becoming a risk because the project now contains hundreds of missions, more than one thousand Markdown files and hundreds of JSON artifacts.

## Decision

Create an official Program X01:

```text
PROGRAM X01 - Project Execution Protocol
```

Program X01 defines the Project Operating System for executing future work through state-driven commands such as:

- `EXECUTE PROGRAM A03`
- `EXECUTE PHASE A03-3`
- `EXECUTE UNTIL GATE`
- `CONTINUE ROADMAP`
- `AUDIT -> EXECUTE -> REVIEW`

## Scope

Program X01 does not alter clinical architecture, scientific content, runtime behavior, product UI or medical logic.

It governs how agents decide what to execute next.

## Consequences

- `NEXT_MISSION.md` may point to a state-driven execution command.
- Agents must read audit, status, dependencies and gates before executing.
- Execution must stop at gates, conflicts, missing dependencies or safety boundaries.
- Manual prompts remain allowed, but program-level execution becomes the preferred mode.

## Non-Authorization

This ADR does not authorize:

- prescription;
- recommendation;
- runtime consumption of scientific content;
- parallel scientific population;
- bypassing `NEXT_MISSION.md`;
- skipping gates;
- modifying clinical architecture.

## Declaration Final

PsychRx now has an official execution protocol layer. The project should proceed by state rather than by isolated manual prompts whenever possible.
