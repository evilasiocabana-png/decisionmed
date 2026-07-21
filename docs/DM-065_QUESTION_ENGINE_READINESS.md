# DM-065 — Question Engine readiness

## Outcome

DecisionMEd can now report whether the structural prerequisites for one
registered Question Engine are present. The report binds the selected engine to
the exact governed input fingerprint and trace.

## Fail-closed checks

- approved engine binding exists;
- matching implementation identity is registered;
- clinical snapshot remains structurally complete;
- exact human safety review remains recorded;
- Knowledge, Evidence and specialty schemas remain current.

## Safety boundary

`STRUCTURAL_PREREQUISITES_PRESENT` is not permission to invoke an engine. The
report always keeps engine, reasoning and clinical execution disabled and names
audited invocation orchestration as the next missing control. No engine method
is called.

## Rollback

Revert the DM-065 commit. The change adds one isolated readiness module, its
exports, tests and this document.
