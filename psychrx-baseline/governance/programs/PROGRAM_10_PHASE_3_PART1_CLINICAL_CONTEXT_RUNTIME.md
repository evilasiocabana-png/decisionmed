# Program 10 Phase 3 Part 1 - Clinical Context Runtime

## Program

Program 10 - Clinical Runtime.

## Phase

Phase 3 - Clinical Context Runtime.

## Scope

This document consolidates Missions 254 through 260.

The Clinical Context Runtime defines how the runtime will construct, version, validate and publish a structural Clinical Context for authorized downstream components.

This phase does not create clinical reasoning, AI, therapeutic recommendations, prescriptions, medication ranking or runtime consumption of scientific knowledge.

## Mission 254 - Clinical Context Snapshot Engine

### Objective

Define the engine responsible for creating immutable Clinical Context Snapshots.

### Responsibility

The Snapshot Engine creates a consistent representation of the current clinical context at a specific moment.

It consolidates structural context only. It does not infer, diagnose, recommend, prescribe or interpret clinical meaning.

### Logical Inputs

- Clinical Workspace state
- Clinical Widgets state
- Patient Context
- Runtime Session
- Existing Runtime metadata

### Logical Output

Clinical Context Snapshot.

### Minimum Logical Structure

- `snapshotId`
- `patientId`
- `encounterId`
- `runtimeVersion`
- `timestamp`
- `status`
- `completeness`
- `clinicalProblems`
- `symptoms`
- `hypotheses`
- `goals`
- `constraints`
- `medications`
- `monitoring`
- `pendingQuestions`

### Lifecycle

```text
Workspace State
-> Context Assembly
-> Snapshot Construction
-> Integrity Validation
-> Version Assignment
-> Read-only Availability
```

### Construction Rules

- snapshots must be immutable after creation;
- every snapshot must have a unique identifier;
- every snapshot must include runtime version and timestamp;
- missing fields must be represented explicitly rather than silently ignored;
- no field can be converted into a recommendation.

### Integrity Criteria

- required identifiers exist;
- snapshot has a known runtime version;
- referenced context sections are structurally present;
- status is explicit;
- publication is blocked if structural integrity fails.

## Mission 255 - Clinical Context Version Manager

### Objective

Define the versioning model for Clinical Context.

### Responsibility

The Version Manager creates immutable versions whenever the structural context changes.

It preserves history without modifying previous versions.

### Version Fields

- `versionId`
- `parentVersion`
- `creationTime`
- `reason`
- `author`
- `runtimeOrigin`
- `immutableHash`

### Versioning Rules

- versions are append-only;
- rollback is logical and never mutates previous versions;
- each version must reference its parent when applicable;
- each version must include a reason;
- each version must be traceable to runtime origin.

### Rollback Model

Rollback means selecting a previous valid version as active reference.

Rollback does not delete, rewrite or reinterpret any version.

## Mission 256 - Context Assembly Pipeline

### Objective

Define the official pipeline for assembling the Clinical Context.

### Pipeline

```text
Clinical Widgets
-> Workspace State
-> Clinical Context Builder
-> Snapshot
-> Validation
-> Runtime Availability
```

### Dependencies

- Clinical Workspace provides user-facing state.
- Clinical Widgets provide structured UI sections.
- Runtime Session provides execution identity.
- Snapshot Engine creates immutable representation.
- Validators check structural integrity.

### Failure Points

- missing patient identifier;
- missing encounter identifier;
- inconsistent widget state;
- duplicated section identifiers;
- unsupported context status;
- failed integrity validation.

### Contracts

- upstream components provide structural data;
- Runtime does not infer missing clinical meaning;
- invalid context cannot be published;
- downstream consumers receive only validated structural context.

## Mission 257 - Context Lifecycle Controller

### Objective

Define the lifecycle of the Clinical Context.

### States

```text
Draft
Building
Validating
Ready
Active
Archived
Invalid
```

### Transition Model

```text
Draft -> Building
Building -> Validating
Validating -> Ready
Ready -> Active
Active -> Archived
Draft -> Invalid
Building -> Invalid
Validating -> Invalid
```

### Blocking Rules

- only `Ready` contexts can be published;
- only validated contexts can become `Ready`;
- invalid contexts cannot be consumed by Clinical Kernel;
- archived contexts are read-only historical references;
- active context remains structural and non-prescriptive.

## Mission 258 - Context Integrity Validator

### Objective

Define structural validation for Clinical Context before availability to the Clinical Kernel.

### Validation Categories

- required fields;
- structural consistency;
- valid references;
- duplicate detection;
- snapshot integrity;
- lifecycle state validity.

### Error Categories

- `missing_required_field`
- `invalid_reference`
- `duplicate_identifier`
- `invalid_lifecycle_state`
- `snapshot_integrity_failure`
- `publication_blocked`

### Failure Handling

- validation failures must be explicit;
- invalid contexts remain unavailable;
- errors are auditable;
- no automatic correction may create clinical meaning.

## Mission 259 - Context Consistency Checker

### Objective

Define the mechanism that checks internal consistency before activation.

### Consistency Checks

- all widget references map to known context sections;
- snapshot sections do not contradict lifecycle state;
- version parent exists when required;
- context status matches validation status;
- publication request references a valid snapshot.

### Conflict Classification

- structural conflict;
- reference conflict;
- lifecycle conflict;
- version conflict;
- publication conflict.

### Integration With Validator

The Consistency Checker supplements the Integrity Validator.

The Integrity Validator checks whether required structure exists.

The Consistency Checker checks whether the existing structure is coherent.

Neither component performs clinical inference.

## Mission 260 - Context Publication Gateway

### Objective

Define the gateway responsible for publishing only structurally valid Clinical Context versions to authorized consumers.

### Publication Criteria

- context state is `Ready`;
- integrity validation passed;
- consistency check passed;
- version metadata exists;
- traceability metadata exists;
- publication target is authorized.

### Access Control

Authorized consumers may include:

- Clinical Kernel;
- Clinical Workspace;
- Audit components;
- future runtime components explicitly approved by architecture.

Unauthorized consumers include:

- prescribing modules;
- autonomous decision modules;
- unvalidated AI components;
- direct interface access bypassing application/runtime contracts.

### Publication Events

- `ContextPublicationRequested`
- `ContextPublished`
- `ContextPublicationBlocked`

These are structural events only and do not represent clinical action.

### Blocking Rules

- invalid context is blocked;
- non-ready context is blocked;
- untraceable context is blocked;
- runtime clinical recommendation remains blocked;
- prescription remains blocked.

## Architecture Boundary

Clinical Context Runtime is a runtime infrastructure concern.

It does not own:

- diagnosis;
- therapeutic objectives;
- evidence interpretation;
- safety evaluation;
- medication recommendation;
- prescription;
- clinical judgment.

## Textual Diagram

```text
Clinical Workspace
    |
    v
Clinical Widgets
    |
    v
Context Assembly Pipeline
    |
    v
Clinical Context Snapshot
    |
    v
Version Manager
    |
    v
Integrity Validator
    |
    v
Consistency Checker
    |
    v
Publication Gateway
    |
    v
Authorized Read-only Consumers
```

## Acceptance Criteria

- Clinical Context is specified as a unique versionable architecture artifact.
- Snapshot construction is documented.
- Versioning is documented.
- Assembly pipeline is documented.
- Lifecycle states are documented.
- Structural validation and consistency checks are documented.
- Publication Gateway is documented.
- No clinical logic, AI, recommendation or prescription is introduced.

## Current Project State

This phase does not alter the current Track A blocker:

`A04-003 - SNRI_SOURCE_CORPUS_INTAKE`

## Final Declaration

Program 10 Phase 3 Part 1 defines the Clinical Context Runtime as structural, versioned, validated and publishable infrastructure. It remains read-only and non-prescriptive.
