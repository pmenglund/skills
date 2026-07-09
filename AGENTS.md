# Repository Instructions

This repository is an `sx` asset vault. Keep `README.md` focused on human setup and usage. Keep this file focused on how Codex should edit and verify the vault.

## Working Rules

- Check `git status --short` before editing. The user may make changes between turns or run multiple threads in this repository.
- Do not overwrite, revert, or reformat unrelated changes.
- Prefer small, scoped edits that preserve the current asset layout and manifest style.

## Vault Structure

- `sx.toml` is the root vault manifest. Every asset added to the vault must have a matching `[[assets]]` entry.
- Versioned assets live under `assets/<asset-name>/<version>/`.
- Each asset directory has `assets/<asset-name>/list.txt` containing available versions.
- Keep asset names, version directories, metadata names, and `sx.toml` manifest entries in sync.

## Asset Types

- Skills use `SKILL.md` plus `metadata.toml`.
- Codex agents use `<agent-name>.toml` plus `metadata.toml`; keep Codex-specific agent assets scoped with `clients = ["codex"]` in the root manifest when appropriate.
- The standalone `council-*` agent assets duplicate the role prompts in `assets/agents-council/1/references/agents/`. Keep those files byte-for-byte aligned unless intentionally versioning the standalone agents separately.
- Rules use `RULE.md`, `metadata.toml`, and an asset-local `sx.toml` with a `[rule]` section.
- `assets/codex-global-agents/1/RULE.md` is the sx-managed copy of the global Codex `~/.codex/AGENTS.md` guidance. Compare it with `/Users/pme/.codex/AGENTS.md` before changing either file.
- Do not delete or overwrite `/Users/pme/.codex/AGENTS.md` unless the user explicitly asks for that live-file change.

## Documentation

- Update `README.md` only for human-facing usage, install, or catalog changes.
- Put Codex-specific handling rules in this `AGENTS.md`, not in `README.md`.
- When adding a new public asset, update the README catalog if it should be visible to human users.

## Verification

- For manifest changes, run `sx install --dry-run --target /Users/pme/src/pmenglund/skills` when feasible.
- If `sx` needs to refresh its Git vault cache and sandboxing blocks it, rerun the same command with escalation rather than claiming validation from local inspection alone.
- For captured global instructions, verify with:

```sh
diff -u /Users/pme/.codex/AGENTS.md assets/codex-global-agents/1/RULE.md
```

## Prompting Feedback

- If the user could have prompted more precisely during the session, include concise, actionable prompt-improvement feedback in the final response.
