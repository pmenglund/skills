---
name: spec-extractor
description: "Use when extracting a durable, language-neutral behavior specification and portable conformance assets from an existing codebase for cross-language reimplementation, parity, migration, compatibility review, or implementation planning."
---

# Spec Extractor

Extract an evidence-backed behavior contract from an existing project. Preserve the recognizable public API layout while removing source-binding mechanics so another language can implement the same contract idiomatically and reach materially similar results.

Use `assets/SPEC_TEMPLATE.md` as the starting structure. Delete sections that do not help the project; never leave placeholders in a completed spec.

Default to **deterministic behavioral parity**: independent implementations must agree on deterministic inputs, outputs, artifacts, ordering, state transitions, and failures. Use **structural parity** only when the request is limited to API shape. Use **generative-output parity** only when prompt and generated-output similarity are explicitly part of the goal.

## Required Workflow

1. Identify the source repository and destination. Default to `<source-root>/SPEC.md` only when the source root is unambiguous; otherwise obtain an explicit destination.
2. Read the nearest applicable `AGENTS.md` files. Inspect an existing destination immediately before editing it and preserve authoritative manual changes.
3. Gather read-only evidence from public documentation, exported interfaces, implementation, tests, fixtures, schemas, examples, error handling, state ownership, persistence, compatibility behavior, and recent changes when relevant. Treat tests and fixtures as evidence, not automatically as contract.
4. Classify evidence before drafting:
   - **Observed behavior:** what the system does now.
   - **Required continuity:** what users or integrations rely on.
   - **Desired change:** behavior the request intentionally adds, removes, or clarifies.
   - **Incidental implementation:** source-binding or internal choices that are not contract.
   - **Unknown:** behavior that cannot be proven and requires an explicit question or draft marker.
5. Select the compatibility target: structural, deterministic behavioral, or generative-output parity. Record it in the spec and bundle manifest.
6. Write purpose, goals, non-goals, users, and the hero workflow. Then express critical workflows as observable requirements covering inputs, outputs, ordering, state, side effects, defaults, failures, and completion evidence.
7. When the source contains behavior-bearing fixtures, schemas, or goldens, produce the portable conformance bundle described in `references/CONFORMANCE_BUNDLE.md`. If no useful portable assets exist, say so in verification rather than manufacturing weak fixtures.
8. Run the API-landmark pass, binding-neutralization pass, evidence audit, two-implementer convergence audit, and final contract review below.
9. Write the resulting `SPEC.md` and any bundle, then re-read them as an implementer in a different language.

Do not invent product scope, silently preserve accidental behavior, or turn every implementation detail found in source into a requirement.

## Preserve API Landmarks

Keep canonical public names that let users recognize the same SDK layout across languages:

- public components and data types, such as `Memory`, `Session`, and `MemoryItem`;
- public operations, such as `extract`, `extract_batch`, `dream`, and `render_read_instructions`;
- public fields, options, modes, enum values, file names, artifact names, and protocol literals.

Confirm that a name is public through exports, documentation, examples, compatibility tests, or real consumers. Do not preserve internal helper names or a binding-specific package/module namespace unless it is deliberately part of the cross-SDK contract.

Describe APIs with language-neutral tables. For each operation record its canonical name, inputs, outputs, defaults, ordering, side effects, completion behavior, and failure behavior. For each data type record its canonical name, fields, constraints, defaults, and identity rules.

## Neutralize Binding Details

Translate source evidence into portable semantics:

| Source construct | Write in the specification |
|---|---|
| Class, struct, module, or service | Canonical public component or data type |
| Method or function | Canonical operation and its behavior |
| Framework model | Validated structured record |
| Native list, slice, array, or tuple | Ordered collection when order matters |
| Native dictionary or map | Key-value collection when key semantics matter |
| Null sentinel | Omitted, not supplied, disabled, or no limit, according to behavior |
| Exception type | Stable error category and observable failure |
| Async syntax | Completion, cancellation, concurrency, and ordering semantics |
| Constructor syntax | Required and optional configuration with defaults |

Exclude source-language names, runtime/version requirements, framework or type-system mechanics, imports, decorators, native signature syntax, package managers, linters, test runners, source paths/extensions, and implementation-local build or test commands.

Never write a binding's null sentinel, such as `None`, `nil`, or `undefined`, as an API default or option value. State the semantic condition instead: not supplied, omitted, disabled, no limit, or no value. Preserve `null` only when it is an externally observable serialized wire value.

Preserve named technologies only when externally observable or required for interoperability: wire schemas, JSON fields, Markdown files, CLI flags, endpoints, event names, provider APIs, persisted formats, public model defaults, and exact public literals. A dependency used only because of the source implementation is not contract.

## Extract Portable Conformance Evidence

Read `references/CONFORMANCE_BUNDLE.md` whenever tests, fixtures, schemas, snapshots, golden files, prompts, or persisted examples may help independent implementations converge.

Extract only behavior-bearing evidence that can be represented independently of the source runtime. Typical candidates include deterministic input/output records, normalization, ordering, paths, serialization, parsing failures, truncation, persisted artifacts, wire schemas, and stable deterministic rendering. Convert native exceptions into portable error categories and identify the stage at which failure becomes observable.

Exclude test-framework objects, implementation-bound mocks, source-only setup, temporary paths, request identifiers, timing or scheduler accidents, and fixtures that merely expose an incidental implementation choice. Preserve an apparent bug only when evidence classifies it as required continuity; label it explicitly.

Make canonical representation rules explicit where they affect equality or interoperability: character encoding, newline handling, object-key treatment, number representation, omitted versus serialized null values, logical path model, sorting, duplicate identity, and comparison rules.

Deterministic public outputs may have byte-exact goldens in deterministic behavioral parity. Do not make live model prose byte-exact contract. For nondeterministic generation, use semantic invariants and fixed fake-provider responses. Copy internal generation prompts and their prompt-rendering goldens only for generative-output parity, and source-pin them in the manifest.

Keep binding-specific API signatures, package names, runtime requirements, and tooling out of the portable core. Put them in `bindings/<language>.md` only when the request explicitly asks for a binding profile.

## Evidence Audit

For every normative detail, ask:

1. Can a caller, persisted artifact, external system, or compatibility test observe it?
2. Is it an explicitly required constraint rather than merely how the source happens to work?
3. Could another language satisfy it without copying the source runtime, framework, object model, or repository layout?

If the first two answers are no, omit it. If the third answer is no, rewrite it as behavior or mark it as a deliberate platform constraint. Do not make internal artifact names, request identifiers, prompt text, temporary paths, helper concurrency, or provider lifecycle normative unless evidence proves consumers depend on them. Do not name an internal file or directory merely to say it is temporary, cleaned up, or excluded; state that temporary working artifacts must not appear in durable output.

When sources disagree, record the conflict. Do not silently choose aspirational documentation over implementation, or implementation over an explicit compatibility promise. In particular, distinguish generation guidance from post-generation validation: a prompt requesting a property does not prove the system enforces it.

## Two-Implementer Convergence Audit

Before finishing, compare two independent implementers who cannot inspect the source. When fresh agents are available, give each only the extracted spec and bundle, ask for a separate implementation-decision ledger, and compare their answers. Otherwise perform two isolated passes without carrying conclusions from the first into the second. For every relevant item below, ask whether both would make the same observable choice or explicitly mark the surface not applicable:

- defaults and versioned provider or model profiles;
- normalization, serialization, path semantics, ordering, duplicate identity, cross-scope conflicts, and most-specific-match rules;
- token or size accounting, truncation, and boundary conditions;
- state ownership, replacement versus upsert, atomicity, migration, partial failure, and input immutability;
- error categories, attribution, partial success, cancellation, retries, and timeouts;
- prompt versions, deterministic rendering, generated-output validation, and enforcement boundaries.

Resolve each likely divergence by adding a normative requirement, portable fixture, schema, golden, or explicit binding profile. A normative case must contain a concrete expected outcome; an instruction to "choose" or "define" a rule is not conformance evidence. If evidence cannot resolve the choice, classify the case as evidence-only and keep an open question that clearly blocks parity. Do not invent behavior for inapplicable surfaces. Do not hide an implementation decision behind words such as "deterministic", "approximately", "safe", or "canonical" without defining the relevant algorithm or comparison.

## Verification

Make acceptance criteria behavioral and falsifiable. Name conformance scenarios, fixtures, schemas, goldens, interoperability checks, or manual workflows; do not prescribe source-language commands or source test filenames in the portable spec.

Before finishing, confirm:

- purpose, goals, non-goals, users, and hero workflow agree;
- each important public API landmark is covered, intentionally excluded, or explicitly changed;
- normalization, duplicates, ordering, defaults, paths, state ownership and replacement, side effects, errors, migrations, cancellation, retries, and enforcement boundaries are explicit where relevant;
- the convergence audit leaves no silent choice that could materially change deterministic results;
- conformance assets are portable, pinned to an immutable source revision when available, classified as normative or evidence-only, and mapped back to source evidence;
- exact prompts appear only when generative-output parity requires them;
- another language can implement every normative sentence while retaining the recognizable API layout;
- no source language, framework, runtime, toolchain, native signature, binding null sentinel, source path, or unresolved template placeholder remains;
- externally observable formats and exact literals were not accidentally generalized away;
- open questions do not conceal a decision required for implementation.

The final document is a steady-state behavior contract, not a README rewrite, reverse-engineering transcript, source inventory, or implementation plan.
