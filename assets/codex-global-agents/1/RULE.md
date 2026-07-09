I sometimes make changes between turns, or run multiple threads in the same repo, so make sure to check what I've changed so you don't clobber any modifcations.

# Review Agents

Use `review-*` agents only when a task has enough risk or ambiguity that an independent review would materially improve the result, and only once the work is otherwise ready to commit. Run review agents after implementation and local verification are complete, just before staging or committing the finished change.

Prefer:

- `review-security` for auth, permissions, secrets, network exposure, command execution, or dependency risk.
- `review-qa` for test strategy, regression risk, fixtures, edge cases, or acceptance criteria.
- `review-architecture` for maintainability, boundaries, data flow, concurrency, or long-term operability.
- `review-ux-specialist` for CLI/UI flows, wording, accessibility, error states, or workflow friction.
- `review-sre` for deployment safety, observability, rollback, alerts, incidents, scaling, or production readiness.

Do not use review agents for tiny mechanical edits or when they would add delay without reducing risk.

When a review agent finds actionable issues, address them before handing control back to the user. If you intentionally do not address a finding, explain why. In the final response, summarize which review agents ran, what they found, and what changed because of the review.

# Model Routing

The main Codex session is configured to use GPT-5.6 Terra and normally owns implementation, testing, and delivery.

When the `plans-md` skill applies in the root session:

- Inspect the current repository state first.
- Spawn exactly one `planner` agent and wait for its result.
- Use the planner's result as evidence, not as unquestioned authority.
- Validate its proposed files, commands, and assumptions against the current repository before presenting or executing the plan.
- Create or update the plan files according to the `plans-md` skill after reviewing the planner's result.
- Do not start implementation until required user decisions are resolved or explicitly recorded as assumptions.

Do not spawn `planner` for tiny mechanical edits, simple factual questions, or an already approved plan that needs no revision.

The `planner` agent is planning-only and must not spawn subagents.

For a quick response that needs bounded, read-only exploration, use `explorer`.
Use it to locate relevant files, trace a narrow code path, summarize local
evidence, or answer a focused repository question. Do not use it for
implementation, substantial planning, security review, broad research, or work
where a missed detail would be costly.

During implementation, use the main Terra session. Escalate to a Sol agent when the work involves security boundaries, destructive migrations, subtle concurrency, major architectural choices, repeated failed attempts, or evidence that invalidates the approved plan.

Use Sol-backed `review-*` agents near completion when an independent review would materially reduce risk.

# Prompting

- If you detect a way I could have better prompted during the session, provide concise, actionable feedback prefixed with 💡.
