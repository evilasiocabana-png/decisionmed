# Program 10 Phase 3 Part 2 - Context Evolution and Runtime Context Services

## Program

Program 10 - Clinical Runtime.

## Phase

Phase 3 - Clinical Context Runtime.

## Scope

This document consolidates Missions 261 through 267.

It specifies how the Clinical Context Runtime detects structural changes, produces diffs, merges valid sources, binds context to runtime sessions, navigates temporal versions, manages cache and exposes an internal Runtime Context API.

No clinical reasoning, diagnosis, recommendation, prescription, AI or runtime scientific knowledge consumption is introduced.

## Mission 261 - Clinical Context Change Detection Engine

### Objective

Define the mechanism responsible for detecting structural changes between Clinical Context versions.

### Responsibilities

- compare consecutive context versions;
- identify additions;
- identify removals;
- identify modifications;
- classify changes structurally;
- generate structural events;
- expose results to Runtime components.

### Inputs

- previous Clinical Context Snapshot;
- current Clinical Context Snapshot.

### Output

Context Change Set.

### Change Types

- `Added`
- `Updated`
- `Removed`
- `Restored`
- `Archived`

### Events

- `ContextChanged`
- `ContextUnchanged`
- `ContextInvalidated`
- `ContextRestored`

### Conceptual Algorithm

```text
Receive previous snapshot
Receive current snapshot
Normalize structural fields
Compare identifiers
Compare section membership
Compare version metadata
Build structural change set
Emit structural context event
Return change set
```

### Prohibited Interpretation

The engine must not infer:

- clinical improvement;
- clinical worsening;
- severity;
- urgency;
- therapeutic priority.

## Mission 262 - Clinical Context Diff Engine

### Objective

Specify the structured representation of differences between two Clinical Context versions.

### Diff Fields

- `entity`
- `attribute`
- `previousValue`
- `newValue`
- `timestamp`
- `origin`
- `version`

### Supported Cases

- inclusion;
- exclusion;
- update;
- state change;
- dependency change.

### Granularity

Diffs should be granular enough to explain what changed structurally, but must avoid interpreting clinical meaning.

### Serialization

Diff output must be JSON-safe and stable across Runtime versions.

### Persistence Boundary

This specification defines logical persistence only.

No physical database, file persistence or storage technology is selected.

## Mission 263 - Clinical Context Merge Controller

### Objective

Define the controller that consolidates multiple valid context sources into one consistent Snapshot.

### Possible Sources

- Clinical Workspace;
- Clinical Widgets;
- Runtime Session;
- Patient Model;
- Domain Services.

### Merge Principles

- preserve Runtime-defined source priority;
- prevent silent conflicts;
- register every conflict;
- preserve traceability;
- produce a single structurally consistent Snapshot candidate.

### Conflict Types

- `Duplicate Entity`
- `Missing Dependency`
- `Version Conflict`
- `Invalid State`
- `Circular Reference`

### Conflict Handling

Conflicts are reported structurally.

The Merge Controller does not choose a clinical truth, does not decide care and does not resolve clinical ambiguity.

## Mission 264 - Runtime Session Context Binder

### Objective

Define the service responsible for binding a valid Clinical Context to an active Runtime Session.

### Operations

- bind;
- unbind;
- rebind;
- validate session;
- enforce single active context per session;
- synchronize lifecycle.

### Binding Rules

- only valid contexts may be bound;
- one Runtime Session may have only one active Clinical Context;
- rebind requires explicit invalidation or archival of previous binding;
- every bind/unbind/rebind event must be auditable.

### Prohibited Behavior

The binder must not:

- mutate clinical content;
- validate clinical correctness;
- authorize therapeutic decisions;
- publish context to unauthorized consumers.

## Mission 265 - Temporal Clinical Context Manager

### Objective

Define temporal navigation across Clinical Context versions.

### Capabilities

- Timeline;
- Point-in-Time Snapshot;
- Previous Snapshot;
- Current Snapshot;
- Version Navigation.

### Temporal Rules

- previous versions are immutable;
- no retroactive mutation is allowed;
- timeline order is determined by version metadata and timestamp;
- archived versions remain readable for audit;
- temporal navigation does not imply clinical interpretation.

### Navigation Contract

```text
getCurrent()
getPrevious(versionId)
getAt(timepoint)
listTimeline()
```

These are logical operations only, not endpoint definitions.

## Mission 266 - Runtime Context Cache

### Objective

Define the architectural cache for Clinical Context.

### Responsibilities

- reduce repeated context reconstruction;
- invalidate stale versions;
- control expiration;
- preserve coherence;
- prevent use of invalid versions.

### Cache States

- `Warm`
- `Cold`
- `Expired`
- `Invalid`
- `Refreshing`

### Cache Rules

- cache is never the source of truth;
- invalid contexts cannot be served;
- stale contexts require refresh before authorized use;
- cache invalidation must be traceable;
- cache must not hide validation failures.

### Technology Boundary

No cache technology, framework or storage backend is selected in this phase.

## Mission 267 - Runtime Context API

### Objective

Specify the internal API for authorized access to Clinical Context.

### Operations

- `getCurrentContext()`
- `getContextVersion()`
- `getContextHistory()`
- `getSnapshot()`
- `getDiff()`
- `subscribe()`
- `unsubscribe()`
- `invalidate()`
- `publish()`

### API Requirements

- consumers receive read-only context unless explicitly authorized otherwise;
- permissions are explicit;
- versions are explicit;
- contracts are stable;
- future Clinical Kernel integration must not bypass the API.

### Authorized Consumers

- Clinical Runtime components;
- Clinical Kernel;
- Clinical Workspace through Application Layer;
- Audit components.

### Prohibited Consumers

- direct UI components bypassing Application Layer;
- prescribing modules;
- autonomous decision modules;
- unvalidated AI components.

### API Boundary

This is an internal contract specification.

It does not define HTTP endpoints, database access, external services or infrastructure details.

## Architecture Diagram

```text
Snapshot Versions
    |
    v
Change Detection Engine
    |
    v
Diff Engine
    |
    v
Merge Controller
    |
    v
Session Context Binder
    |
    v
Temporal Context Manager
    |
    v
Runtime Context Cache
    |
    v
Runtime Context API
    |
    v
Authorized Read-only Consumers
```

## Acceptance Criteria

- Change detection is specified.
- Diff model is specified.
- Merge controller is specified.
- Runtime Session binding is specified.
- Temporal context navigation is specified.
- Runtime Context Cache is specified.
- Runtime Context API is specified.
- No clinical reasoning, recommendation, prescription or AI is introduced.

## Current Project State

This phase does not alter the current Track A blocker:

`A04-003 - SNRI_SOURCE_CORPUS_INTAKE`

## Final Declaration

Program 10 Phase 3 Part 2 defines context evolution and runtime context service contracts as structural, read-only infrastructure. It remains non-prescriptive and does not execute clinical reasoning.
