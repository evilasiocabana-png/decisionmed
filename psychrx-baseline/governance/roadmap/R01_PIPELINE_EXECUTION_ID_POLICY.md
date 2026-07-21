# R01 Pipeline Execution ID Policy

## Mission

R01-004 - ROADMAP_PIPELINE_IMPLEMENTATION.

## Purpose

Define how parameterized pipeline executions are identified without losing historical mission traceability.

## ID Format

Pipeline executions use:

```text
PIPE-<PROGRAM>-<SCOPE>-<PIPELINE>-<SEQUENCE>
```

Examples:

```text
PIPE-A04-0-SNRI-VALIDATION-001
PIPE-A04-SNRI-CONTENT-001
PIPE-A05-NDRI-CORPUS-001
```

## Required Fields

Every pipeline execution must record:

- pipeline execution ID;
- historical mission alias, when applicable;
- queue ID;
- pipeline family;
- parameters;
- source corpus path;
- allowed files;
- prohibited files;
- gates;
- validation command;
- final status.

## Historical Alias Rule

Historical IDs are never discarded.

When a historical mission is migrated into a pipeline, the pipeline execution must include:

```text
Historical alias: <MISSION_ID>
```

## Current Active Mapping

| Pipeline Execution ID | Pipeline | Historical Alias | Status |
| --- | --- | --- | --- |
| PIPE-A04-0-SNRI-VALIDATION-001 | ValidationPipeline[DrugClass=SNRIs] | A04.0-005 - SNRI_SOURCE_VALIDATION | Completed |

## Queue Rule

The global queue continues to use sequential `SEQ` values.

Pipeline execution IDs do not replace queue IDs. They describe the execution model.

## Final Declaration

Pipeline IDs make repeated scientific work executable without duplicating entire roadmap branches, while historical mission aliases preserve continuity and auditability.
