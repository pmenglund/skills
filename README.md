# skills
Local AI assistant skills packaged as an [`sx`](https://github.com/sleuth-io/sx) vault.

`sx` is a package manager for AI coding assistants. This repository uses `sx.toml` as the manifest and stores versioned skill assets under `assets/<skill>/<version>/`.

## Available skills

- `agents-council`: run important decisions, tradeoffs, plans, proposals, or uncertain judgment calls through a Codex subagent council.
- `agents-md`: bootstrap a repository with the instruction template from `github.com/pmenglund/agents` by creating `AGENTS.md`, `APP.md`, `PLANS.md`, `LANGUAGE.md`, `WORKFLOW.md`, and `plans/`.
- `gc`: perform a static architecture and code quality review of a Go repository and write findings to `GC.md`.
- `goth-web-ui`: build a Go net/http web UI using gomponents + htmx + Tailwind (daisyUI), with embedded assets and unit/integration/e2e tests.
- `spec-extractor`: extract a durable behavior specification and portable conformance assets from an existing codebase.

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
