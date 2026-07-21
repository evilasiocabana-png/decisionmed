# Execution Command Reference

## Purpose

Define official high-level commands for state-driven PsychRx execution.

## Commands

### EXECUTE PROGRAM

```text
EXECUTE PROGRAM A03
```

Executes the active program from the current `NEXT_MISSION.md` until the next gate.

### EXECUTE PHASE

```text
EXECUTE PHASE A03-3
```

Executes a phase from the first incomplete mission, respecting gates.

### EXECUTE SPRINT

```text
EXECUTE SPRINT A03-3-1
```

Executes a sprint from the first incomplete mission.

### EXECUTE UNTIL GATE

```text
EXECUTE UNTIL GATE
```

Continues from the current next mission and stops at a baseline, blocker or decision gate.

### CONTINUE ROADMAP

```text
CONTINUE ROADMAP
```

Uses the repository state to select the next allowed action.

### AUDIT PROJECT

```text
AUDIT PROJECT
```

Runs a read-only project audit and does not advance missions.

### AUDIT -> EXECUTE -> REVIEW

```text
AUDIT -> EXECUTE -> REVIEW
```

Audits state, executes the next mission or sequence, validates, updates controls and reports.

## Current Recommended Command

```text
EXECUTE PROGRAM A03
```

## Declaration Final

These commands replace manual prompt-by-prompt navigation as the preferred operating mode.
