# skills
Local AI assistant skills packaged as an [`sx`](https://github.com/sleuth-io/sx) vault.

`sx` is a package manager for AI coding assistants. This repository uses `sx.toml` as the manifest and stores versioned skill assets under `assets/<skill>/<version>/`.

## Available skills

- `agents-council`: run important decisions, tradeoffs, plans, proposals, or uncertain judgment calls through a Codex subagent council.
- `agents-md`: bootstrap a repository with the instruction template from `github.com/pmenglund/agents` by creating `AGENTS.md`, `APP.md`, `PLANS.md`, `LANGUAGE.md`, `WORKFLOW.md`, and `plans/`.
- `gc`: perform a static architecture and code quality review of a Go repository and write findings to `GC.md`.
- `goth-web-ui`: build a Go net/http web UI using gomponents + htmx + Tailwind (daisyUI), with embedded assets and unit/integration/e2e tests.
- `spec-extractor`: extract a durable behavior specification and portable conformance assets from an existing codebase.

## Available rules

- `codex-global-agents`: global Codex `AGENTS.md` guidance captured as an `sx` rule asset.

## Available agents

- `review-qa`: review test coverage, missing edge cases, regression risk, test reliability, fixtures, CI coverage, and acceptance criteria.
- `review-security`: review changes for security risks, including auth, authorization, input handling, secret handling, command execution, dependency risk, and unsafe defaults.
- `review-architecture`: review architecture, maintainability, API boundaries, data flow, naming, duplication, coupling, error handling, concurrency, and long-term operability.
- `review-ux-specialist`: review CLI and UI changes for user experience quality, including clarity, discoverability, accessibility, error states, and workflow efficiency.
- `review-sre`: review deployment safety, operability, observability, reliability, incident response, scaling, and production readiness.
- `explorer`: quickly gather focused, read-only repository evidence for bounded questions.
- `planner`: prepare concrete Plans.md recommendations for substantial work before implementation starts.
- `council-contrarian`, `council-first-principles`, `council-operator`, `council-user-advocate`, `council-systems-thinker`, `council-peer-reviewer`, and `council-chairman`: Codex agent definitions used by the `agents-council` skill.

## Use this repo with `sx`

Install `sx`:

```sh
brew tap sleuth-io/tap
brew install sx
```

Initialize a profile or project that uses this repo as a Git vault:

```sh
sx init --type git --repo git@github.com:pmenglund/skills.git
```

Install all assets available to the current scope:

```sh
sx install
```

Install a specific skill:

```sh
sx install agents-council
sx install agents-md
sx install goth-web-ui
sx install gc
sx install spec-extractor
```

If you are using a fork, replace `git@github.com:pmenglund/skills.git` with your fork's Git URL.

## Use `agents-md`
Use this skill when you want to adopt the `pmenglund/agents` instruction template in a new or existing repository. The skill:

- infers `AGENTS.md` placeholder values from the target repo first
- asks you to validate inferred values and provide missing ones
- installs files without overwriting existing files unless explicitly forced

Invoke it in Codex, for example:

```text
Use agents-md to bootstrap /path/to/target/repo with language go and workflow linear
```
