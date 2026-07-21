# Safety Engine

The Safety Engine is the structural safety layer for PsychRx.

It is read-only and does not prescribe, select medication, rank strategies, or make autonomous clinical decisions. Its current implementation provides contracts, coordination, traceability, audit, alert, blocking, and runtime integration primitives for future validated safety knowledge.

## Current Status

- Structural package only.
- No hardcoded clinical rules.
- No therapeutic recommendation.
- No medication selection.
- No prescription.
- No patient-specific clinical decision.

## Main Flow

```text
Runtime Context
-> Safety Coordinator
-> Evaluators
-> Alert Engine
-> Blocking Engine
-> Safety Result
-> Runtime / Workspace read-only status
```

## Declaration

The Safety Engine protects the architecture before it protects clinical execution. Clinical content must enter through validated knowledge and evidence contracts, never through hardcoded algorithmic shortcuts.
