# AGENTS.md Setup Usage Reference

Source repo: `https://github.com/pmenglund/agents` (default branch: `master`)

## Files to install in a consuming repo root
- `AGENTS.md` from `_AGENTS.md`
- `APP.md` from `APP.md`
- `PLANS.md` from `PLANS.md`
- `LANGUAGE.md` from one file in `languages/`
- `WORKFLOW.md` from one file in `workflows/`
- `plans/` directory (empty by default)

## Available variants
Language options:
- `go` -> `languages/GO.md`
- `python` -> `languages/PYTHON.md`

Workflow options:
- `linear` -> `workflows/LINEAR.md`
- `beads` -> `workflows/BEADS.md`
- `github` -> `workflows/GITHUB.md`
- `markdown` -> `workflows/MARKDOWN.md`
- `template` -> `workflows/TEMPLATE.md`

## Core checklist from upstream README
1. Copy the core files into repo root.
2. Create `LANGUAGE.md` from one language template.
3. Create `WORKFLOW.md` from one workflow template.
4. Create `plans/`.
5. Fill placeholders such as `{{TRACKER_NAME}}`, `{{APP_NAME}}`, and `{{TEST_COMMAND}}`.
6. Update `APP.md` with real architecture and constraints.
7. Keep `AGENTS.md` and `PLANS.md` stable unless strong reason.

## Notes
- README documents an optional `.ai/` layout, but only if tooling is configured to load it.
- Default recommendation is to keep these files in repo root for discoverability.
- `AGENTS.md` placeholders must be fully resolved before finishing setup.
- `APP.md` placeholders may remain after setup and are expected to be edited by the user.
