---
name: agents-md
description: Bootstrap a repository with the instruction template from github.com/pmenglund/agents by creating AGENTS.md, APP.md, PLANS.md, LANGUAGE.md, WORKFLOW.md, and plans/. Use when asked to set up or adopt this template in a new or existing repo. Infer AGENTS.md template placeholder values from existing files, ask the user to validate replacements and provide missing values, then install with all AGENTS.md placeholders resolved.
---

## Goal
Bootstrap a target repository with the files and structure documented in `github.com/pmenglund/agents` README.

## Workflow
1. Confirm target repository path.
2. Confirm template choices:
- language: `go` or `python`
- workflow: `linear`, `beads`, `github`, `markdown`, or `template`
3. Infer AGENTS placeholder values from existing repo files:
```bash
./scripts/setup_repo.py --target /path/to/repo --language go --workflow linear --infer-only
```
4. Show inferred values to the user and ask for validation:
- ask the user to confirm each inferred value
- ask the user for each missing placeholder value
5. Confirm overwrite behavior:
- default: do not overwrite existing files
- use `--force` only when explicitly requested
6. Run `scripts/setup_repo.py` with validated + missing values supplied via `--set`.
7. Verify AGENTS has no unresolved `{{...}}` placeholders.
8. Report created files. APP placeholders may remain and are expected.

## Commands
Run from this skill folder:

```bash
./scripts/setup_repo.py \
  --target /path/to/repo \
  --language go \
  --workflow linear \
  --set APP_NAME=my-service \
  --set LANGUAGE_NAME=Go \
  --set TRACKER_NAME=Linear \
  --set TEST_COMMAND='go test ./...'
```

Inference pass (no writes):

```bash
./scripts/setup_repo.py --target /path/to/repo --language python --workflow github --infer-only
```

Dry run after values are complete:

```bash
./scripts/setup_repo.py \
  --target /path/to/repo \
  --language python \
  --workflow github \
  --set APP_NAME=my-service \
  --set LANGUAGE_NAME=Python \
  --set TRACKER_NAME='GitHub Issues' \
  --set TEST_COMMAND='pytest' \
  --set TRACKER_ID=PROJ-101 \
  --set EPIC_ID=PROJ-100 \
  --dry-run
```

## Rules
1. Prefer script execution over manual copying.
2. Keep source configurable via `--owner`, `--repo`, `--ref` when users request forks or pinned refs.
3. Always run `--infer-only` first and ask the user to validate proposed AGENTS replacements before writing files.
4. Keep operations idempotent by default:
- abort if destination files already exist
- require `--force` for overwrite
5. Always ensure `plans/` exists.
6. Never finish with unresolved placeholders in `AGENTS.md`.
7. Do not require `APP.md` placeholders to be resolved; user will complete `APP.md`.

## Resources
- `scripts/setup_repo.py`: deterministic installer for template files.
- `references/agents-template-usage.md`: source mapping, options, and checklist derived from the upstream README.
