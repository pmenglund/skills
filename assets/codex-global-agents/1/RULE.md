I sometimes make changes between turns, or run multiple threads in the same repo, so make sure to check what I've changed so you don't clobber any modifcations.

# Review Agents

Use `review-*` agents when a task has enough risk or ambiguity that an independent review would materially improve the result.

Prefer:

- `review-security` for auth, permissions, secrets, network exposure, command execution, or dependency risk.
- `review-qa` for test strategy, regression risk, fixtures, edge cases, or acceptance criteria.
- `review-architecture` for maintainability, boundaries, data flow, concurrency, or long-term operability.
- `review-ux-specialist` for CLI/UI flows, wording, accessibility, error states, or workflow friction.
- `review-sre` for deployment safety, observability, rollback, alerts, incidents, scaling, or production readiness.

Do not use review agents for tiny mechanical edits or when they would add delay without reducing risk. When you use one, summarize the findings and say what changed because of the review.

# Prompting

- If you detect a way I could have better prompted during the session. I want you to give me advice on how I can improve my prompt engineering with actionable feedback if available.
