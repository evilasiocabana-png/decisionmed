# Codex Commands - PsychRx

## Status

Official command reference.

## Purpose

Define the high-level commands Codex may interpret for PsychRx execution.

## Commands

### EXECUTE PROGRAM `<PROGRAM_ID>`

Execute the next authorized mission inside the requested program after resolving dependencies, blockers and gates.

### EXECUTE PHASE `<PROGRAM_ID>` `<PHASE_ID>`

Execute the next authorized mission inside a specific phase. Stop at the phase gate.

### EXECUTE MISSION `<MISSION_ID>`

Execute one explicit mission only if it is the next authorized mission.

### EXECUTE UNTIL GATE

Continue executing authorized missions in order until the next mandatory gate is reached.

### EXECUTE PHASE `<PROGRAM_ID>-<PHASE_ID>` AUTO

Execute all authorized missions in a phase until phase baseline, gate, blocker or validation failure.

### EXECUTE PROGRAM `<PROGRAM_ID>` AUTO

Execute authorized missions in a program until program gate, blocker, phase boundary requiring review or validation failure.

### EXECUTE UNTIL BLOCK

Continue executing the currently authorized sequence until the first formal stop condition.

### CONTINUE ROADMAP

Resolve the next authorized program, phase or mission from project state documents.

### AUDIT PROJECT

Inspect project state, inconsistencies, blockers, dependencies and next authorized action without advancing execution.

### VERIFY CURRENT STATE

Read control documents and report the current program, phase, mission, blockers and next action.

### AUDIT THEN EXECUTE

Audit first. Execute only if no blocker, contradiction or gate violation is found.

### BLOCK IF DEPENDENCY MISSING

Stop execution and create/update a blocker report when dependencies are missing.

### REPORT STATUS

Report current state without creating clinical content or executing a mission.

## Invalid Command Outcomes

A command must be rejected when it would:

- skip the next mission;
- start a blocked program;
- bypass a gate;
- alter frozen documents without ADR;
- create clinical content without authorization;
- create prescribing or recommendation behavior.
- continue after a failed validation.
- continue after a gate is reached.

## Current Command Mapping

```text
VERIFY CURRENT STATE
-> CTO_GATE_REVIEW - A03_PHASE_3_SPRINT_1_BASELINE_REVIEW
```

Current auto candidate:

```text
EXECUTE PHASE A03-04 AUTO
-> starts with A03-036 - MECHANISM_CONTENT_EXTRACTION
```

## Final Declaration

Codex commands are operational shortcuts, not permission to ignore governance.

