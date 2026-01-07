# skills
Local Codex skills. This repo currently provides:

- `goth-web-ui`: build a Go net/http web UI using gomponents + htmx + Tailwind (daisyUI), with embedded assets and unit/integration/e2e tests.

## Install a skill with `skill-installer`
Use the `skill-installer` skill to install from this repo. Example using the helper script it wraps:

```sh
$skill-installer install from repo pmenglund/skills the skill goth-web-ui
```

If you are using a fork, replace `pmenglund/skills` with your `OWNER/REPO`. Restart Codex to pick up new skills.
