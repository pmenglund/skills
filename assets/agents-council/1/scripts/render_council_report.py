#!/usr/bin/env python3
"""Render Agents Council HTML and Markdown artifacts from a JSON payload."""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return json.dumps(value, ensure_ascii=False, indent=2).strip()


def context_line(item: Any) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        path = as_text(item.get("path"))
        note = as_text(item.get("note"))
        if path and note:
            return f"{path} - {note}"
        return path or note
    return as_text(item)


def normalize_items(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    items: list[dict[str, str]] = []
    for index, item in enumerate(value, start=1):
        if isinstance(item, dict):
            name = as_text(item.get("name") or item.get("reviewer") or f"Item {index}")
            response = as_text(item.get("response") or item.get("content") or item.get("text"))
        else:
            name = f"Item {index}"
            response = as_text(item)
        if response:
            items.append({"name": name, "response": response})
    return items


def markdown(data: dict[str, Any], timestamp: str) -> str:
    context_files = [context_line(item) for item in data.get("context_files", [])]
    advisors = normalize_items(data.get("advisors", []))
    peer_reviews = normalize_items(data.get("peer_reviews", []))
    anonymization = data.get("anonymization", {})

    lines = [
        "# Agents Council Transcript",
        "",
        f"Generated: {timestamp}",
        "",
        "## Original Question",
        "",
        as_text(data.get("original_question")),
        "",
        "## Framed Question",
        "",
        as_text(data.get("framed_question")),
        "",
        "## Context Files Used",
        "",
    ]

    if context_files:
        lines.extend(f"- {item}" for item in context_files if item)
    else:
        lines.append("- None recorded")

    lines.extend(["", "## Advisor Responses", ""])
    for advisor in advisors:
        lines.extend([f"### {advisor['name']}", "", advisor["response"], ""])

    lines.extend(["## Anonymization Map", ""])
    if isinstance(anonymization, dict) and anonymization:
        for label, advisor_name in anonymization.items():
            lines.append(f"- {label}: {advisor_name}")
    else:
        lines.append("- None recorded")

    lines.extend(["", "## Peer Reviews", ""])
    for review in peer_reviews:
        lines.extend([f"### {review['name']}", "", review["response"], ""])

    lines.extend([
        "## Chairman Synthesis",
        "",
        as_text(data.get("chairman_synthesis")),
        "",
    ])
    return "\n".join(lines).rstrip() + "\n"


INLINE_RE = re.compile(r"(`[^`\n]+`)|(\*\*([^*\n]+(?:\*[^*\n]+)*)\*\*)")


def inline_markdown(text: str) -> str:
    parts: list[str] = []
    position = 0
    for match in INLINE_RE.finditer(text):
        parts.append(html.escape(text[position : match.start()]))
        if match.group(1):
            code_text = match.group(1)[1:-1]
            parts.append(f"<code>{html.escape(code_text)}</code>")
        else:
            parts.append(f"<strong>{html.escape(match.group(3))}</strong>")
        position = match.end()
    parts.append(html.escape(text[position:]))
    return "".join(parts)


def paragraphs(text: str) -> str:
    return "<br>\n".join(inline_markdown(line) for line in text.split("\n"))


def markdown_blocks(text: str) -> str:
    blocks: list[str] = []
    paragraph_lines: list[str] = []

    def flush_paragraph() -> None:
        if not paragraph_lines:
            return
        blocks.append(f"<p>{paragraphs(chr(10).join(paragraph_lines))}</p>")
        paragraph_lines.clear()

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line:
            flush_paragraph()
            continue

        stripped = line.lstrip()
        heading_prefix = len(stripped) - len(stripped.lstrip("#"))
        if (
            1 <= heading_prefix <= 6
            and len(stripped) > heading_prefix
            and stripped[heading_prefix] == " "
        ):
            flush_paragraph()
            heading_text = stripped[heading_prefix + 1 :].strip()
            blocks.append(f"<h{heading_prefix}>{inline_markdown(heading_text)}</h{heading_prefix}>")
            continue

        paragraph_lines.append(line)

    flush_paragraph()
    return "\n".join(blocks)


def html_doc(data: dict[str, Any], timestamp: str) -> str:
    title = html.escape(as_text(data.get("title")) or "Agents Council Report")
    recommendation = as_text(data.get("recommendation"))
    one_next_step = as_text(data.get("one_next_step"))
    advisors = normalize_items(data.get("advisors", []))
    peer_reviews = normalize_items(data.get("peer_reviews", []))
    context_files = [context_line(item) for item in data.get("context_files", [])]
    anonymization = data.get("anonymization", {})

    advisor_cards = "\n".join(
        f"""<details><summary>{html.escape(advisor['name'])}</summary><p>{paragraphs(advisor['response'])}</p></details>"""
        for advisor in advisors
    )
    review_cards = "\n".join(
        f"""<details><summary>{html.escape(review['name'])}</summary><p>{paragraphs(review['response'])}</p></details>"""
        for review in peer_reviews
    )
    context_items = "\n".join(f"<li>{html.escape(item)}</li>" for item in context_files if item)
    if not context_items:
        context_items = "<li>None recorded</li>"

    map_items = ""
    if isinstance(anonymization, dict):
        map_items = "\n".join(
            f"<li><strong>{html.escape(str(label))}</strong>: {html.escape(str(name))}</li>"
            for label, name in anonymization.items()
        )
    if not map_items:
        map_items = "<li>None recorded</li>"

    recommendation_block = (
        f"<section class=\"callout\"><h2>Recommendation</h2><p>{paragraphs(recommendation)}</p></section>"
        if recommendation
        else ""
    )
    next_step_block = (
        f"<section class=\"callout next\"><h2>One Thing to Do First</h2><p>{paragraphs(one_next_step)}</p></section>"
        if one_next_step
        else ""
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f7f4;
      --paper: #ffffff;
      --ink: #202124;
      --muted: #666b73;
      --line: #d9d9d2;
      --accent: #245c73;
      --accent-soft: #e8f1f4;
      --warn-soft: #fff4df;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    main {{
      width: min(980px, calc(100% - 32px));
      margin: 32px auto;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 28px;
    }}
    h1, h2, h3 {{ line-height: 1.2; margin: 0 0 12px; }}
    h1 {{ font-size: 32px; }}
    h2 {{ font-size: 20px; margin-top: 28px; }}
    p {{ margin: 0 0 16px; }}
    code {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", monospace;
      font-size: 0.95em;
      background: #f1f1ed;
      border: 1px solid #dfdfd7;
      border-radius: 4px;
      padding: 0 3px;
    }}
    .synthesis h2:first-child {{ margin-top: 0; }}
    .meta {{ color: var(--muted); margin-bottom: 24px; }}
    .question {{
      border-left: 4px solid var(--accent);
      padding: 12px 16px;
      background: var(--accent-soft);
      margin: 16px 0;
    }}
    .callout {{
      background: var(--accent-soft);
      border: 1px solid #c7dde5;
      border-radius: 8px;
      padding: 16px;
      margin: 20px 0;
    }}
    .next {{
      background: var(--warn-soft);
      border-color: #ead9ad;
    }}
    details {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px 14px;
      margin: 10px 0;
      background: #fff;
    }}
    summary {{
      cursor: pointer;
      font-weight: 700;
      color: var(--accent);
    }}
    ul {{ padding-left: 22px; }}
    footer {{
      margin-top: 32px;
      color: var(--muted);
      font-size: 13px;
      border-top: 1px solid var(--line);
      padding-top: 16px;
    }}
  </style>
</head>
<body>
  <main>
    <h1>{title}</h1>
    <p class="meta">Generated {html.escape(timestamp)}</p>

    <h2>Original Question</h2>
    <div class="question">{paragraphs(as_text(data.get("original_question")))}</div>

    <h2>Framed Question</h2>
    <div class="question">{paragraphs(as_text(data.get("framed_question")))}</div>

    {recommendation_block}
    {next_step_block}

    <h2>Chairman Synthesis</h2>
    <section class="synthesis">{markdown_blocks(as_text(data.get("chairman_synthesis")))}</section>

    <h2>Advisor Responses</h2>
    {advisor_cards}

    <h2>Peer Reviews</h2>
    {review_cards}

    <h2>Context Files Used</h2>
    <ul>{context_items}</ul>

    <h2>Anonymization Map</h2>
    <ul>{map_items}</ul>

    <footer>Agents Council report. Review the Markdown transcript for the complete reasoning record.</footer>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Agents Council report artifacts.")
    parser.add_argument("payload", type=Path, help="JSON payload produced by the council run")
    parser.add_argument("--output-dir", type=Path, default=Path("."), help="Directory for generated artifacts")
    parser.add_argument("--timestamp", help="Timestamp override, formatted as YYYYMMDD-HHMMSS")
    args = parser.parse_args()

    data = json.loads(args.payload.read_text(encoding="utf-8"))
    stamp = args.timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    human_stamp = datetime.now().isoformat(timespec="seconds")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.output_dir / f"council-report-{stamp}.html"
    transcript_path = args.output_dir / f"council-transcript-{stamp}.md"

    report_path.write_text(html_doc(data, human_stamp), encoding="utf-8")
    transcript_path.write_text(markdown(data, human_stamp), encoding="utf-8")

    print(json.dumps({
        "report": str(report_path.resolve()),
        "transcript": str(transcript_path.resolve()),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
