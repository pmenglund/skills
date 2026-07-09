---
name: agents-council
description: "Run important decisions, tradeoffs, plans, proposals, or uncertain judgment calls through a Codex subagent council with independent advisor analysis, anonymized peer review, chairman synthesis, and saved HTML and Markdown reasoning artifacts. Use when the user says council this, run the council, pressure-test this, stress-test this, debate this, war room this, get multiple perspectives, I am torn between, should I choose X or Y, or asks for a high-stakes general-purpose decision to be challenged from several angles. Do not use for simple factual lookups, routine implementation, summarization, one-right-answer questions, or low-stakes yes/no preferences."
---

# Agents Council

## Overview

Run a general-purpose council with Codex subagents. The method is adapted from LLM Council: collect independent first-pass answers, anonymize them for peer review, then synthesize a final verdict with a chairman pass.

The council must produce two durable artifacts for every full run:

- `council-report-YYYYMMDD-HHMMSS.html`
- `council-transcript-YYYYMMDD-HHMMSS.md`

## Before Running

Use the council only when several perspectives can materially improve the answer. If the task is factual, mechanical, or better solved by direct implementation, answer directly and explain that a council would add overhead.

If the user gives a vague decision, ask one clarifying question, then proceed. Do not ask a long questionnaire.

If subagent tools are not already available, search for multi-agent or subagent tools before continuing. If no subagent capability exists in the current surface, state that the skill is blocked because this skill requires Codex subagents; do not simulate five advisors with one model pass.

Read `references/prompts.md` and the role files in `references/agents/` before starting the council. Use `scripts/render_council_report.py` after synthesis to write the report and transcript.

## Workflow

1. Restate the decision in neutral terms.
2. Scan for relevant local context for about 30 seconds. Prefer explicitly referenced files, repo guidance files, plan files, recent related transcripts, and small documents that directly affect the decision. Do not do broad research unless the user asks.
3. Write a framed question that includes the core decision, options, stakes, constraints, and context files used. Do not include your own recommendation.
4. Spawn all five advisor subagents in parallel. If the matching Codex custom agents are installed, use them by name. Otherwise spawn generic subagents with the `developer_instructions` from the matching file in `references/agents/`. Each advisor receives only the framed question and its role prompt.
5. Collect advisor responses before starting review. Keep each response focused and direct.
6. Randomize advisor responses into `Response A` through `Response E`. Keep the mapping private until the transcript.
7. Spawn peer-review subagents in parallel. Reviewers see the framed question and anonymized responses, not the advisor identities.
8. Run the chairman synthesis using the framed question, de-anonymized advisor responses, anonymized peer reviews, and the anonymization map.
9. Create a JSON payload and run `scripts/render_council_report.py` to generate the HTML report and Markdown transcript.
10. Reply with the recommendation, main agreement, main clash, blind spot, one next action, and links to both artifacts.

## Advisors

Use these five advisors unless the user explicitly asks for a different council. The TOML files are bundled role definitions for review and reuse; they are not active Codex custom agents unless copied to `~/.codex/agents/` or `.codex/agents/`.

- `references/agents/contrarian.toml`
- `references/agents/first-principles.toml`
- `references/agents/operator.toml`
- `references/agents/user-advocate.toml`
- `references/agents/systems-thinker.toml`

Use `references/agents/peer-reviewer.toml` for anonymized review and `references/agents/chairman.toml` for final synthesis when spawning those roles as subagents.

## Artifact Payload

Pass a JSON file to `scripts/render_council_report.py` with these fields:

- `original_question`: the user's raw request.
- `framed_question`: the neutral council prompt.
- `context_files`: strings or objects with `path` and `note`.
- `advisors`: objects with `name` and `response`.
- `anonymization`: object mapping `Response A` style labels to advisor names.
- `peer_reviews`: objects with `reviewer` and `response`.
- `chairman_synthesis`: final synthesis text.
- `recommendation`: optional short recommendation for the report header.
- `one_next_step`: optional single next action.

Run:

```bash
python3 /path/to/agents-council/scripts/render_council_report.py council-payload.json --output-dir .
```

## Output Rules

Keep the chat answer concise. The report and transcript hold the detail.

The chairman synthesis must include:

- where the council agrees
- where the council clashes
- blind spots caught by review
- recommendation
- one thing to do first

The recommendation must be direct. It may be conditional only when the condition is concrete and testable.
