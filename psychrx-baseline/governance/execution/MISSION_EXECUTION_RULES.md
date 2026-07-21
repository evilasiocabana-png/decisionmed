# Mission Execution Rules - PsychRx

## Status

Official Program X01 rule document.

## Purpose

Define the rules for executing a single mission.

## Command

```text
EXECUTE MISSION <MISSION_ID>
```

## Mandatory Checks

Codex must confirm that the mission:

- is the current mission in `governance/execution/NEXT_MISSION.md`;
- is not completed;
- is not superseded;
- is not blocked;
- belongs to the active program and phase;
- has all dependencies satisfied;
- has acceptance criteria;
- has clear files permitted or implied by the mission;
- does not violate permanent clinical safety boundaries.

## Execution Steps

1. Read current state.
2. Resolve mission authorization.
3. Inspect existing files.
4. Create or update only authorized files.
5. Avoid duplicate concepts.
6. Validate acceptance criteria.
7. Run tests.
8. Update control documents.
9. Record report.
10. Set the next mission.

## Current Authorized Mission

```text
No mission is authorized before CTO gate review.
```

Program A03 Phase 3 Sprint 1 is complete through A03-030.

## Final Declaration

Mission execution is atomic: one mission, one scope, one report, one next state.

