---
name: goth-web-ui
description: Build a Go net/http web UI using gomponents + htmx + Tailwind(daisyUI), with embedded assets and unit/integration/e2e tests (Playwright). Use when asked to implement a Go web UI with gomponents/htmx/Tailwind+daisyUI, embed browser assets in the binary, and include unit, integration, or Playwright tests.
---

## Goal
Implement a Go web UI:
- stdlib net/http
- gomponents for HTML
- htmx for partial updates
- Tailwind + daisyUI compiled CSS
- embed all browser-served files into the binary
- include unit + integration + e2e tests

## Workflow
1) Clarify routes, HTMX interaction, and test expectations.
2) Scaffold server package with `internal/app.NewServer() (http.Handler, error)`.
3) Add gomponents render helpers and HTMX-aware full/fragment rendering.
4) Vendor assets and embed them under `/assets/`.
5) Ask whether to add Playwright boilerplate.
6) Implement unit, integration, and Playwright tests.
7) Run required verification commands and fix flakiness.

## Implementation rules
1) Provide `internal/app.NewServer() (http.Handler, error)` so tests can start the app easily.
2) Serve embedded static assets under `/assets/`:
   - `app.css` (compiled Tailwind + daisyUI)
   - `htmx.min.js` (vendored)
3) Pages:
   - Full-page render for normal requests
   - Fragment render when `HX-Request: true`
4) Include at least one HTMX interaction suitable for e2e testing.
5) Avoid runtime file reads for templates/assets.

## Project layout guidance
- Keep HTML building blocks in `internal/ui` or similar.
- Store assets in `assets/` (or `internal/assets/`) and use `//go:embed` to serve them.
- Add `data-testid` attributes to anchor Playwright selectors.

## AGENTS.md
- Copy `assets/AGENTS.md` into the generated Go package directory (default `./internal/ui`).

## HTMX guidance
- Check for `HX-Request: true` to switch to fragment render.
- Provide at least one interaction such as:
  - Button with `hx-get` to `/time` that replaces a `<div id="result">`
  - Form with `hx-post` returning a fragment
- Ensure fragment response omits the document shell (`html/head/body`).

## Tests
- Unit: render gomponents nodes to strings and assert key HTML snippets.
- Integration: `httptest.NewServer`; verify routes, embedded assets, and fragment behavior.
- E2E: Playwright tests verifying initial render and HTMX interaction.

## Playwright boilerplate
- Ask the user if they want Playwright boilerplate added.
- If yes, copy `assets/playwright/` into the repo root (or `./e2e/` if requested).
- Update `E2E_BASE_URL` and `data-testid` selectors to match the UI.

## Verification steps (required)
- `go test ./...`
- run Playwright tests (headless)
- if Playwright fails: fix selectors, timing, or markup until stable

## Optional (nice to have)
- graceful shutdown
- CSP headers
- cache headers for assets
