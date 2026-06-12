# Portable Conformance Bundle

Use this reference when source tests, fixtures, schemas, snapshots, prompts, or persisted examples can reduce ambiguity for a reimplementation.

## Destination And Ownership

Given a requested `<destination>/SPEC.md`, prefer `<destination>/specs/` for the bundle.

Before writing:

1. Inspect the destination and any existing `specs/` directory.
2. Reuse `specs/` only when it is absent or clearly belongs to this specification.
3. If `specs/` contains unrelated or authoritative content, use `<destination>/<spec-stem>.conformance/` instead.
4. Preserve existing files unless the user explicitly authorizes replacement. Re-read files immediately before editing.

Use only the directories needed by the evidence:

```text
specs/
  README.md
  manifest.json
  conformance.md
  evidence.md
  parity-profile.json
  fixtures/
  schemas/
  goldens/
  prompts/
  bindings/
```

`README.md`, `manifest.json`, `conformance.md`, and `evidence.md` are required when a bundle is produced. `parity-profile.json` is conditional, as are the remaining directories.

## Artifact Selection

Include an artifact when all of these are true:

- it proves externally observable behavior or a deliberate compatibility constraint;
- another implementation can consume it without the source runtime or test framework;
- its expected result and comparison rule are explicit;
- it materially reduces a plausible implementation divergence.

Good candidates:

- deterministic input/output tables;
- path normalization and validation cases;
- ordering, tie-breaking, and duplicate cases;
- serialization and parsing cases, including invalid inputs;
- truncation boundaries and size accounting;
- persisted snapshot, replacement, and migration cases;
- stable wire or artifact schemas;
- deterministic renderer output;
- fixed provider responses used to test generative workflows.

Exclude or rewrite:

- native objects serialized only for test convenience;
- framework fixtures, mocks, monkeypatches, or dependency injection setup;
- source test names and test-runner configuration;
- temporary directories, random identifiers, timestamps, and scheduling details;
- implementation call traces or private helper behavior;
- live model output presented as a byte-exact golden;
- accidental behavior not classified as required continuity.

## Portable Forms

Prefer JSON for structured cases, UTF-8 text or Markdown for textual artifacts, YAML only when it is itself a public format, and binary files only when the protocol requires byte-level compatibility.

Each fixture collection should state:

- case identifier and purpose;
- input and pre-existing state;
- operation or workflow stage;
- expected output, state, or error category;
- ordering and equality rules;
- whether the case is normative or evidence-only;
- source evidence pointers.

A normative fixture must provide concrete inputs, preconditions, expected outputs or state, and an executable comparison rule. A meta-case that merely says an implementation must select or define an algorithm is not normative. When the evidence does not establish the choice, mark the artifact evidence-only and record the decision as an open parity blocker.

Normalize source-bound concepts:

| Source evidence | Portable representation |
|---|---|
| Native exception | Stable error category plus failure stage |
| Runtime path object | Logical path string under the specified path model |
| Mock provider | Request record plus fixed response or error |
| In-memory model | Schema-valid structured record |
| Snapshot assertion | Deterministic golden plus comparison rules |
| Timing assertion | Observable cancellation, timeout, retry, or ordering requirement |

Do not assume common library defaults. Specify UTF-8 validity, line endings, trailing newline treatment, Unicode normalization when relevant, object-key comparison, numeric constraints, omitted versus null fields, path separators, case sensitivity, and whether comparisons are byte-exact or semantic.

## Manifest Contract

`manifest.json` must be deterministic except for explicitly labeled informational fields. It should contain:

```json
{
  "format_version": 1,
  "compatibility_target": "deterministic-behavioral",
  "source": {
    "repository": "logical repository identifier",
    "revision": "immutable source revision when available"
  },
  "artifacts": [
    {
      "path": "fixtures/example.json",
      "kind": "fixture",
      "role": "normative",
      "sha256": "lowercase hexadecimal digest",
      "evidence": ["source-relative pointer"]
    }
  ]
}
```

Allowed compatibility targets are `structural`, `deterministic-behavioral`, and `generative-output`. Artifact roles are `normative` and `evidence-only`. Artifact kinds should come from `document`, `fixture`, `schema`, `golden`, `prompt`, `binding`, `profile`, and `evidence` unless the spec defines another interoperable kind. Use `document` for `README.md` and `conformance.md`. Source-derived artifacts require evidence pointers; authored bundle documents may omit them when their provenance is the extracted contract itself.

List every emitted bundle file except `manifest.json` itself. Sort artifacts by portable path and hash the exact emitted bytes. Serialize the manifest as UTF-8 JSON with LF line endings, two-space indentation, and one trailing newline. Omit unavailable optional source fields instead of inserting placeholders. Avoid volatile generation timestamps unless the user needs provenance beyond the immutable source revision.

## Bundle Documents

`README.md` states the compatibility target, the relationship between `SPEC.md` and the bundle, how a reimplementation should consume the artifacts, and which comparisons are exact versus semantic.

`conformance.md` maps normative requirements to cases. It must cover happy paths, important boundaries, failures, state transitions, and compatibility behavior. It may reference fixture case identifiers rather than duplicate their contents.

`evidence.md` maps requirements and artifacts to documentation, interfaces, implementation, tests, fixtures, schemas, and examples. Classify each source as observed behavior, required continuity, desired change, incidental implementation, or unknown. Include conflicts and explain the chosen contract or unresolved question.

Also include an asset ledger for discovered tests, fixtures, schemas, snapshots, goldens, and prompts. For each source asset, record whether it was included, rewritten, or excluded and why. Group repetitive exclusions when they share one reason, but do not silently omit a behavior-bearing asset.

`parity-profile.json` is optional. Create it only when the selected target makes volatile provider, model, reasoning, prompt-version, or schema-version choices contractual. Pin it to the same immutable source revision as the manifest. Keep those snapshot settings out of the timeless portable core unless they are independently public defaults.

## Prompts And Generated Output

Include `prompts/` only for generative-output parity and only when the assets may be redistributed to the destination. Record exact prompt bytes and hashes, the source revision, rendering inputs, provider-facing schemas, and deterministic prompt-rendering goldens. This restriction does not exclude byte-exact goldens for deterministic public operations whose returned text is itself observable contract.

Separate three layers:

1. Prompt guidance: properties requested from a generator.
2. Recovery and validation: properties the implementation actually checks or normalizes.
3. Durable contract: properties callers may rely on after the operation succeeds.

For model prose, specify semantic invariants and use fixed fake-provider responses for deterministic workflow tests. Do not claim that two live model calls must return identical text.

## Binding Profiles

Create `bindings/<language>.md` only when the user explicitly requests an idiomatic binding contract. A binding profile may define native signatures, package names, runtime support, error mappings, and language-specific verification, but it must reference rather than redefine the portable behavior and conformance cases.

## Completion Check

The bundle is complete when:

- every normative artifact is referenced by a conformance case;
- every normative case contains a concrete expected outcome rather than a choice left to the implementer;
- every conformance case maps to source evidence or an explicit desired change;
- discovered conformance assets have an included, rewritten, or excluded disposition;
- exact and semantic comparisons are distinguishable;
- portable core artifacts contain no source-language syntax or test harness dependency;
- an independent implementer can explain defaults, ordering, duplicate identity and scope precedence, paths, serialization, truncation, atomic state replacement, errors, cancellation, retries, and prompt enforcement without inspecting source.
