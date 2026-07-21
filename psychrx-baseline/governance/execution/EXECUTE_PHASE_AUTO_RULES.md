# Execute Phase Auto Rules - PsychRx

## Command

```text
EXECUTE PHASE <PROGRAM_ID>-<PHASE_ID> AUTO
```

## Purpose

Execute all authorized missions in a phase sequentially until the phase baseline, gate, blocker or validation failure.

## Required Preconditions

- phase exists in project roadmap;
- previous phase baseline is complete;
- phase gate is approved;
- next mission is listed in `governance/execution/NEXT_MISSION.md`;
- mission sequence is known;
- dependencies are satisfied;
- expected validation is defined.

## Behavior

Codex must:

1. execute the next mission;
2. validate results;
3. update all controls;
4. resolve the next mission;
5. continue only if it belongs to the same phase;
6. stop at phase baseline or blocker.

## Current Example

```text
EXECUTE PHASE A03-04 AUTO
```

This should begin with:

```text
A03-036 - MECHANISM_CONTENT_EXTRACTION
```

## Stop Rule

If a mission would require unapproved clinical interpretation, recommendation, prescription or runtime behavior, the phase must stop and a blocker report must be created.

## Declaration Final

`EXECUTE PHASE AUTO` is allowed only inside a single phase and stops at its baseline.
