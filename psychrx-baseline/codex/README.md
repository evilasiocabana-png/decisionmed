# Codex Mission Inbox Pipeline

This directory is the official inbox pipeline for Codex-executed PsychRx missions.

The goal is to let the CTO place mission packages in `codex/inbox/` without requiring the user to provide internal repository paths in chat.

## Flow

```text
ChatGPT (CTO)
        |
Generates mission package files
        |
User uploads package to GitHub
        |
codex/inbox/
        |
Codex reads the package
        |
Codex executes the mission
        |
Codex updates the project
        |
Codex writes execution report
        |
Codex moves the package
```

## Directories

- `inbox/`: new mission packages waiting for execution.
- `processing/`: the single mission package currently being executed.
- `completed/`: successfully executed mission packages.
- `failed/`: mission packages that failed execution.
- `templates/`: reusable mission package templates.

## Package Format

Each mission can be submitted either as a single Markdown file or as a folder.

Preferred simple format:

```text
codex/inbox/
    MISSION_001.md
```

Folder format remains supported for larger mission packages.

Example:

```text
codex/inbox/
    MISSION_001/
        README.md
        MISSION.md
        CODEX.md
        ACCEPTANCE.md
```

Not every file is mandatory. Codex must use the files that exist.

When the mission is a single Markdown file, Codex must read the complete file
as the mission package.

## Reading Order

For folder packages, Codex must always read package files in this order:

1. `README.md`
2. `MISSION.md`
3. `CODEX.md`
4. `ACCEPTANCE.md`

For single-file packages, Codex reads the Markdown file directly.

## Execution Rules

1. Never execute two missions at the same time.
2. Never skip a mission package.
3. Never create a new mission package as a substitute for a missing one.
4. Move the selected package from `inbox/` to `processing/` before execution.
5. No package may remain in `processing/` after execution ends.
6. On success, create `EXECUTION_REPORT.md` inside the package and move it to `completed/`.
7. On failure, create `ERROR_REPORT.md` inside the package and move it to `failed/`.

## Mandatory Project Updates

When applicable, every executed mission must update:

- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/EXECUTION_LOG.md`
- `governance/execution/EXECUTION_STATE.json`
- `governance/execution/NEXT_BLOCK.md`
- `governance/execution/NEXT_MISSION.md`

Any update to those files must be documented in the mission `EXECUTION_REPORT.md`.

## Safety Rules

Codex must never:

- alter the roadmap unless the mission explicitly authorizes it;
- alter the Clinical Constitution;
- alter the Manifesto;
- modify scientific content without authorization;
- create prescription logic;
- create autonomous clinical decision logic;
- execute a mission outside governance order.

## Current Implementation Scope

This pipeline is operational infrastructure. It does not implement a background daemon, scheduler, clinical runtime, scientific extraction, or autonomous mission execution.

Codex still executes missions when instructed, but mission packages can now be deposited in `codex/inbox/` as the official handoff mechanism.
