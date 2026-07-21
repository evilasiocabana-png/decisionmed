# Execute Until Block Rules - PsychRx

## Command

```text
EXECUTE UNTIL BLOCK
```

## Purpose

Continue executing the current authorized mission sequence until Codex encounters a formal stop condition.

## Execution Boundary

This command may cross missions but must not silently cross:

- program gates;
- phase baselines;
- ADR requirements;
- publication gates;
- safety gates.

## Stop Conditions

Stop at:

- blocker;
- gate;
- dependency missing;
- test failure;
- JSON validation failure;
- source traceability gap;
- next mission ambiguity;
- clinical recommendation;
- prescription;
- runtime attempt.

## Reporting

When stopping, Codex must report:

- last mission completed;
- blocking condition;
- files created;
- files updated;
- validation result;
- next authorized mission or gate.

## Declaration Final

`EXECUTE UNTIL BLOCK` is the longest safe autonomous mode. It ends at the first real governance boundary.
