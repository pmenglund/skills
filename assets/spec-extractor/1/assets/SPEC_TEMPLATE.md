---
title: "[Project Name] Specification"
status: Draft
owners:
  - "[Owner or team]"
last_updated: YYYY-MM-DD
compatibility_target: deterministic-behavioral
---

# [Project Name] Specification

Status: Draft

Purpose: [State what this project is for in one or two sentences. Name the user problem or system need, not just the artifact being built.]

## 1. Goals

- [Outcome this project must achieve.]
- [Behavior or capability this spec must make unambiguous.]
- [Quality, compatibility, operational, or delivery result that matters.]

## 2. Non-Goals

- [Related work this project will not do.]
- [Behavior a reader might reasonably assume is included but is explicitly out of scope.]
- [Deferred or intentionally unsupported path.]

## 3. Context

[Give the minimum background needed to understand the spec. For an existing project, describe the current system, relevant behavior to preserve, and the change or clarification this spec introduces. For a new project, describe the problem, target user, and why this project should exist.]

### Compatibility Target

- Target: [Structural, deterministic behavioral, or generative-output parity.]
- Source baseline: [Reference the immutable source revision recorded in the bundle manifest.]
- Observable parity boundary: [State what independent implementations must produce equivalently.]
- Versioned parity profile: [Reference provider defaults, prompt assets, or other source-pinned behavior when applicable.]

## 4. Users and Use Cases

### Primary Users

- [User, operator, service, or system that depends on this project.]

### Hero Use Case

[Describe the most important end-to-end use case in concrete terms.]

### Additional Use Cases

- [Important supported use case.]
- [Important supported use case.]

## 5. Product and Behavior Contract

[Describe the durable behavior this project must provide. Write requirements as observable contracts. Prefer "must", "must not", and "should" when the distinction matters.]

### [Workflow or Capability A]

- [Required behavior.]
- [Inputs, outputs, state transitions, or user-visible result.]
- [Boundary or invariant that must hold.]

### [Workflow or Capability B]

- [Required behavior.]
- [Inputs, outputs, state transitions, or user-visible result.]
- [Boundary or invariant that must hold.]

## 6. Interfaces

[Describe the surfaces through which people or systems use the project. Keep only the subsections that apply.]

### User Interface

- [Views, controls, flows, or interaction expectations.]

### CLI

- `[command or command shape]`: [Required behavior, output, exit status, or safety rule.]

### API or Service Contract

- `[canonical operation, endpoint, event, or protocol]`: [Inputs, outputs, defaults, side effects, ordering, completion, and failure behavior.]

### Files, Data Formats, or Generated Artifacts

- `[path format or artifact]`: [Schema, ownership, lifecycle, or compatibility rule.]

### Binding Profiles

- [Reference any optional language-specific API profile. Keep its syntax, runtime, and tooling requirements outside this portable core.]

## 7. Data, State, and Lifecycle

- [State the project reads.]
- [State the project writes.]
- [Persistence, migration, retention, caching, or cleanup requirement.]
- [Ownership rule for source data versus derived data.]

## 8. Configuration, Dependencies, and Permissions

- [Configuration the project accepts or requires.]
- [External dependency, platform assumption, or integration boundary.]
- [Permission, credential, trust, or safety constraint.]

## 9. Error Handling and Edge Cases

- [Expected failure category and required observable response.]
- [Invalid input, missing dependency, conflict, timeout, retry, or partial-success behavior.]
- [What must be reported to users, callers, operators, or logs.]

## 10. Quality Attributes and Constraints

- [Performance, reliability, accessibility, security, privacy, maintainability, or portability requirement.]
- [Compatibility constraint with existing behavior or consumers.]
- [Known technical, organizational, legal, or operational constraint.]

## 11. Verification and Acceptance Criteria

### Acceptance Criteria

- [Concrete behavior that proves the spec is satisfied.]
- [Concrete behavior that proves an important boundary or failure mode is handled.]

### Verification

- [Conformance scenario, fixture, schema, golden, manual flow, metric, or operational check.]
- [Regression or compatibility check for existing behavior.]

### Conformance Assets

- Bundle: [Portable bundle location, or state that no behavior-bearing portable assets were found.]
- Normative assets: [Fixtures, schemas, and deterministic goldens implementations must satisfy.]
- Evidence-only assets: [Artifacts retained for traceability but not made contract.]
- Comparison model: [Byte-exact, structurally equal, ordered semantic equality, or other explicit rule.]
- Deterministic text: [Reference byte-exact goldens for public deterministic outputs where applicable.]
- Generative behavior: [Semantic invariants and fixed-provider cases; internal prompts and prompt-rendering goldens only when generative-output parity applies.]

## 12. Rollout, Migration, and Operations

[Keep this section when the project changes deployed behavior, persistent state, user workflows, or operational ownership.]

- [Release, migration, backfill, feature flag, compatibility, or rollback requirement.]
- [Monitoring, alerting, support, or ownership expectation.]

## 13. Decisions and Open Questions

### Decisions

- [Decision already made and why it matters.]

### Evidence Conflicts

| Contract topic | Observed implementation | Documentation, tests, or guidance | Extracted decision |
|---|---|---|---|
| [Topic] | [Observed behavior.] | [Supporting or conflicting claim.] | [Required continuity, desired change, incidental behavior, or unresolved.] |

### Open Questions

- [Question that must be answered before implementation or release.]

### Unresolved Divergences

| Decision surface | Plausible implementation choices | Required resolution or conformance asset |
|---|---|---|
| [Defaults, ordering, duplicates, serialization, paths, truncation, state, errors, cancellation, retries, prompts, or enforcement.] | [Choices that would change observable results.] | [Normative rule, fixture, profile, or explicit open question.] |
