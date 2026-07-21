# Program X01 - Project Execution Protocol

## Status

Completed as project operating system baseline.

## Purpose

Program X01 defines how PsychRx should be executed after the architecture phase.

The goal is to transform the project from prompt-driven execution into state-driven execution.

## Problem

The PsychRx architecture is mature. The bottleneck is now operational orchestration:

- many programs;
- many phases;
- hundreds of missions;
- large documentation volume;
- strict safety boundaries;
- dependency chains;
- scientific traceability requirements.

Manual `next prompt` execution is no longer the safest default.

## Official Commands

Program X01 recognizes these high-level commands:

```text
EXECUTE PROGRAM <ID>
EXECUTE PHASE <ID>
EXECUTE SPRINT <ID>
EXECUTE UNTIL GATE
CONTINUE ROADMAP
AUDIT PROJECT
AUDIT -> EXECUTE -> REVIEW
```

## Execution Principle

The agent must always execute from repository state, not from memory.

Before any execution, it must read:

- `docs/PROJECT_AUDIT_REPORT.md`
- `governance/execution/PROJECT_STATUS.md`
- `PROJECT_STATUS.md`
- `governance/execution/PROJECT_TREE.md`
- `docs/PROJECT_DEPENDENCIES.md`
- `governance/execution/PROJECT_INDEX.md`
- `governance/execution/NEXT_MISSION.md`
- relevant ADRs
- relevant program status and progress files

## Current State After X01

The next state-driven command is:

```text
EXECUTE PROGRAM A03
```

The first mission inside that command is:

```text
A03-026 - INDICATION_MODELING
```

## Permanent Limits

Program X01 cannot override:

- Manifest;
- Clinical Constitution;
- Architectural Principles;
- Ontology;
- Safety Contract;
- Evidence Traceability Policy;
- ADRs.

## Declaration Final

Program X01 is the operating layer that tells agents how to continue PsychRx without losing sequence, context or governance.
