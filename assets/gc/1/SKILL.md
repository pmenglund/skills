---
name: gc
description: Use when the user invokes $gc or asks for a static architecture and code quality review of a Go repository that writes concrete findings to GC.md. This skill inspects only and reports; it does not make code changes, open PRs, or commit files.
---

# GC Repository Review

Perform a senior Go engineer static architecture and code quality review of the current repository. Inspect the code and write concrete, high-signal findings to `GC.md`.

Do not make code changes. Do not open a PR. Do not commit `GC.md`. Only inspect and report.

## Mission

Find structural issues that make the code brittle, misleading, over-coupled, redundant, unsafe at boundaries, or likely to fail under change.

Prioritize by expected engineering payoff:

1. Correctness risk
2. Architectural damage
3. Maintainability drag
4. Performance problems on hot paths

Bias toward repository-specific evidence. Do not report style preferences, speculative concerns, or generic best practices.

## Required Workflow

1. Read `AGENTS.md` first and treat it as the repository authority.
2. Check whether `GC.md` already exists. If it does, inspect it before replacing it so user edits or prior findings are not lost blindly.
3. Read `go.mod` and, if useful, `go.sum` to understand module boundaries and major dependencies.
4. Inspect repository layout and package boundaries.
5. Review production code first. Use tests only to clarify contracts, assumptions, or boundary misuse.
6. Search for evidence using repository inspection commands where helpful.
7. Deduplicate overlapping issues before writing the report.
8. Write the final report to `GC.md` only.

## Review Targets

Look for:

- Layering violations against `AGENTS.md`.
- Cross-package reach-through or concrete dependency leaks.
- Domain logic depending on transport, storage, CLI, HTTP, or persistence details.
- Public APIs that expose internal implementation details.
- Redundant validation, normalization, sanitization, parsing, or auth checks.
- Hidden contracts expressed only by call order, comments, naming, or tribal knowledge.
- Weak boundaries using `any`, `interface{}`, `map[string]any`, raw JSON, unchecked assertions, reflection, stringly typed IDs/enums/state, context values, or `panic`-based assumptions.
- Dead code, stale abstractions, unused helpers, or unreachable branches.
- Hot-path waste such as repeated parsing, allocation, regex compilation, DB lookups, JSON marshal/unmarshal, conversion, logging, or metrics.
- Over-broad interfaces, wrong-layer interfaces, or one-implementation interfaces with no real boundary value.
- Exported identifiers that should be private.
- Invalid zero values, public structs that should be constructed, or ambiguous nullable fields.
- Context misuse, including missing propagation through I/O, ignored cancellation, child contexts created too deep, or business inputs stored in context.
- Error handling problems, including lost wrapping context, ignored errors, string matching, inconsistent sentinels, or discarded cleanup errors.
- Concurrency risks, including goroutine leaks, unclear channel ownership, missing cancellation, shared mutable state, or mutex misuse.
- Persistence boundary issues, including transaction leaks, DB models leaking into domain code, or repositories encoding domain rules improperly.
- HTTP/API boundary issues, including duplicated parsing, transport DTO leakage, or inconsistent domain-error status mapping.
- Testability problems caused by hidden globals, hardcoded time/randomness/filesystem/network/process access.
- Reinvented infrastructure that should use the Go standard library or a mature public module.

Prefer Go standard library solutions before recommending external dependencies.

## Finding Bar

Include a finding only if all are true:

- It is specific to this repository.
- It has concrete code evidence.
- It has a plausible failure mode or change-cost scenario.
- An engineer can act on it without further investigation.
- The recommendation simplifies boundaries, strengthens types, removes duplication, or reduces real risk.

Do not include plausible but weakly supported issues.

## Severity Rubric

- Critical: likely correctness, data loss, security, or production stability risk.
- High: strong architectural or correctness risk under realistic change.
- Medium: meaningful maintainability, boundary, or testability drag.
- Low: localized cleanup with clear value but limited blast radius.

## Output Requirements

For each finding, include:

- Title
- Severity: Critical / High / Medium / Low
- Category
- File / Symbol, with line references where possible
- Why it matters
- Evidence from the code
- Recommended fix
- Confidence: High / Medium / Low

Rank findings by real engineering payoff, not by file order.

If no meaningful issues are found, write a short `GC.md` saying so and summarize what was inspected.

## GC.md Format

Write exactly this structure:

```md
# Repository Review Findings

## Summary
- Total findings by severity
- 3-10 highest-value issues first

## Findings

### [Severity] Short title
- Category:
- File / Symbol:
- Why it matters:
- Evidence:
- Recommended fix:
- Confidence:
```

Omit empty categories.

## Final Check Before Saving

Before writing `GC.md`, verify that:

- Each finding has concrete code evidence.
- Each finding includes file/symbol references, with line numbers where practical.
- Overlapping findings are merged.
- Severity matches the rubric.
- Recommendations are simpler than the current design.
- Standard library options are preferred before dependencies.
- The report is concise, specific, and actionable.
