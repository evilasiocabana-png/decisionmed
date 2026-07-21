# PsychRx Governance

This directory is the official governance area for PsychRx.

The repository state must be resolved from files in this directory, not from chat memory.

## Directory Roles

- `constitution/`: foundational clinical and architectural constraints. These documents define what the project must never violate.
- `manifesto/`: project manifesto and manifesto backups.
- `adr/`: Architecture Decision Records and ADR templates.
- `roadmap/`: roadmap, migration, refactoring and program mapping documents.
- `programs/`: program plans, program baselines, program reports and program-specific execution documents.
- `missions/`: mission rules, naming standards, repository rules and cross-cutting governance contracts.
- `execution/`: current operational state, execution logs, gates, blockers and state-driven command protocols.

## Operational Source Of Truth

The primary operational source of truth is:

`governance/execution/EXECUTION_STATE.json`

Before executing any mission, the CTO GPT and Codex must read:

1. `governance/execution/EXECUTION_STATE.json`
2. `governance/execution/PROJECT_EXECUTION_CONTEXT.md`
3. `governance/execution/PROJECT_STATUS.md`
4. `governance/execution/NEXT_MISSION.md`
5. `governance/execution/NEXT_BLOCK.md`
6. `governance/execution/GATES.md`
7. relevant ADRs in `governance/adr/`

## Mandatory Rule

No mission may be executed without consulting `governance/execution/EXECUTION_STATE.json`.

If `EXECUTION_STATE.json` conflicts with older status files, execution must stop and the conflict must be registered in `governance/execution/BLOCKED_ITEMS.md`.

## Scope

This governance reorganization is structural and documentary only. It does not alter clinical logic, runtime behavior, scientific knowledge, tests, algorithms or safety rules.
