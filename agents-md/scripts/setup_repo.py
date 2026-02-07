#!/usr/bin/env python3
"""Install the pmenglund/agents template files into a target repository."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
import urllib.error
import urllib.request
from pathlib import Path


LANGUAGE_SOURCES = {
    "go": "languages/GO.md",
    "python": "languages/PYTHON.md",
}

WORKFLOW_SOURCES = {
    "beads": "workflows/BEADS.md",
    "github": "workflows/GITHUB.md",
    "linear": "workflows/LINEAR.md",
    "markdown": "workflows/MARKDOWN.md",
    "template": "workflows/TEMPLATE.md",
}

TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
TICKET_RE = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b")

WORKFLOW_TRACKER_NAME = {
    "beads": "Beads",
    "github": "GitHub Issues",
    "linear": "Linear",
    "markdown": "Markdown tracker",
    "template": "Linear",
}

LANGUAGE_DISPLAY_NAME = {
    "go": "Go",
    "python": "Python",
}


def parse_key_value(items: list[str]) -> dict[str, str]:
    pairs: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Invalid --set value '{item}'. Expected KEY=VALUE.")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Invalid --set value '{item}'. Key is empty.")
        pairs[key] = value
    return pairs


def fetch_text(owner: str, repo: str, ref: str, source_path: str) -> str:
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{source_path}"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Failed to fetch {source_path} ({exc.code}) from {url}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed to fetch {source_path} from {url}: {exc.reason}") from exc


def collect_sources(language: str, workflow: str) -> list[tuple[str, str]]:
    return [
        ("_AGENTS.md", "AGENTS.md"),
        ("APP.md", "APP.md"),
        ("PLANS.md", "PLANS.md"),
        (LANGUAGE_SOURCES[language], "LANGUAGE.md"),
        (WORKFLOW_SOURCES[workflow], "WORKFLOW.md"),
    ]


def unresolved_tokens(contents: str) -> list[str]:
    return sorted(set(TOKEN_RE.findall(contents)))


def read_text_if_exists(path: Path) -> str | None:
    try:
        if path.exists() and path.is_file():
            return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    return None


def infer_from_existing_agents(target: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    text = read_text_if_exists(target / "AGENTS.md")
    if not text:
        return values

    language_match = re.search(r"LANGUAGE\.md[^\n]*for ([^)]+)\)\.", text)
    if language_match:
        values["LANGUAGE_NAME"] = language_match.group(1).strip()

    app_match = re.search(r"APP\.md[^\n]*for ([^.]+)\.", text)
    if app_match:
        candidate = app_match.group(1).strip()
        if candidate and "{{" not in candidate:
            values["APP_NAME"] = candidate

    tracker_match = re.search(r"Track all work in ([^:]+):", text)
    if tracker_match:
        values["TRACKER_NAME"] = tracker_match.group(1).strip()

    test_match = re.search(r"test suite locally \(`([^`]+)`\)", text)
    if test_match:
        values["TEST_COMMAND"] = test_match.group(1).strip()

    epic_match = re.search(r"plans/([A-Z][A-Z0-9]+-\d+)\.md", text)
    if epic_match:
        values["EPIC_ID"] = epic_match.group(1)

    tracker_id_match = re.search(r'"([A-Z][A-Z0-9]+-\d+):', text)
    if tracker_id_match:
        values["TRACKER_ID"] = tracker_id_match.group(1)

    return values


def infer_app_name(target: Path) -> str | None:
    app_md = read_text_if_exists(target / "APP.md")
    if app_md:
        heading = re.search(r"^#\s+(.+?)\s+Architecture Notes\s*$", app_md, re.MULTILINE)
        if heading and "{{" not in heading.group(1):
            return heading.group(1).strip()

    package_json = read_text_if_exists(target / "package.json")
    if package_json:
        try:
            package_data = json.loads(package_json)
            name = package_data.get("name")
            if isinstance(name, str) and name.strip():
                return name.strip()
        except json.JSONDecodeError:
            pass

    pyproject_text = read_text_if_exists(target / "pyproject.toml")
    if pyproject_text:
        try:
            pyproject_data = tomllib.loads(pyproject_text)
            project_name = pyproject_data.get("project", {}).get("name")
            if isinstance(project_name, str) and project_name.strip():
                return project_name.strip()
        except tomllib.TOMLDecodeError:
            pass

    cargo_text = read_text_if_exists(target / "Cargo.toml")
    if cargo_text:
        try:
            cargo_data = tomllib.loads(cargo_text)
            crate_name = cargo_data.get("package", {}).get("name")
            if isinstance(crate_name, str) and crate_name.strip():
                return crate_name.strip()
        except tomllib.TOMLDecodeError:
            pass

    go_mod = read_text_if_exists(target / "go.mod")
    if go_mod:
        module_match = re.search(r"^module\s+(\S+)\s*$", go_mod, re.MULTILINE)
        if module_match:
            module = module_match.group(1)
            return module.rstrip("/").split("/")[-1]

    if target.name:
        return target.name
    return None


def infer_language_name(target: Path, language_choice: str) -> str:
    language_md = read_text_if_exists(target / "LANGUAGE.md")
    if language_md:
        if re.search(r"\bGo\b", language_md):
            return "Go"
        if re.search(r"\bPython\b", language_md):
            return "Python"

    if (target / "go.mod").exists():
        return "Go"
    if (target / "pyproject.toml").exists() or (target / "requirements.txt").exists():
        return "Python"

    return LANGUAGE_DISPLAY_NAME[language_choice]


def infer_tracker_name(target: Path, workflow_choice: str) -> str:
    workflow_md = read_text_if_exists(target / "WORKFLOW.md")
    if workflow_md:
        if "Linear" in workflow_md:
            return "Linear"
        if "GitHub" in workflow_md:
            return "GitHub Issues"
        if "Beads" in workflow_md:
            return "Beads"
        if "Markdown" in workflow_md:
            return "Markdown tracker"

    if (target / ".github").exists():
        return "GitHub Issues"

    return WORKFLOW_TRACKER_NAME[workflow_choice]


def infer_test_command(target: Path, language_choice: str) -> str | None:
    app_md = read_text_if_exists(target / "APP.md")
    if app_md:
        match = re.search(r"Run tests locally:\s*`([^`]+)`", app_md)
        if match:
            candidate = match.group(1).strip()
            if candidate and "{{" not in candidate:
                return candidate

    makefile = read_text_if_exists(target / "Makefile")
    if makefile and re.search(r"^test\s*:", makefile, re.MULTILINE):
        return "make test"

    package_json = read_text_if_exists(target / "package.json")
    if package_json:
        try:
            package_data = json.loads(package_json)
            scripts = package_data.get("scripts", {})
            if isinstance(scripts, dict) and isinstance(scripts.get("test"), str):
                return "npm test"
        except json.JSONDecodeError:
            pass

    if (target / "go.mod").exists():
        return "go test ./..."

    if (target / "pyproject.toml").exists() or (target / "pytest.ini").exists():
        return "pytest"

    if language_choice == "go":
        return "go test ./..."
    if language_choice == "python":
        return "pytest"
    return None


def infer_ids(target: Path) -> dict[str, str]:
    values: dict[str, str] = {}

    plans_dir = target / "plans"
    if plans_dir.exists() and plans_dir.is_dir():
        for plan_file in sorted(plans_dir.glob("*.md")):
            match = TICKET_RE.fullmatch(plan_file.stem)
            if match:
                values["EPIC_ID"] = match.group(1)
                break

    try:
        branch = subprocess.check_output(
            ["git", "-C", str(target), "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        match = TICKET_RE.search(branch)
        if match:
            values.setdefault("TRACKER_ID", match.group(1))
            values.setdefault("EPIC_ID", match.group(1))
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    if "TRACKER_ID" not in values:
        agents_md = read_text_if_exists(target / "AGENTS.md")
        if agents_md:
            match = re.search(r"\b([A-Z][A-Z0-9]+-\d+)\b", agents_md)
            if match:
                values["TRACKER_ID"] = match.group(1)

    return values


def infer_replacements(target: Path, language_choice: str, workflow_choice: str) -> dict[str, str]:
    values: dict[str, str] = {}
    values.update(infer_from_existing_agents(target))

    app_name = infer_app_name(target)
    if app_name:
        values.setdefault("APP_NAME", app_name)

    values.setdefault("LANGUAGE_NAME", infer_language_name(target, language_choice))
    values.setdefault("TRACKER_NAME", infer_tracker_name(target, workflow_choice))

    test_command = infer_test_command(target, language_choice)
    if test_command:
        values.setdefault("TEST_COMMAND", test_command)

    values.update({k: v for k, v in infer_ids(target).items() if v})
    return values


def print_placeholder_plan(tokens: list[str], replacements: dict[str, str]) -> list[str]:
    missing: list[str] = []
    print("AGENTS.md placeholder plan:")
    for token in tokens:
        value = replacements.get(token, "").strip()
        if value:
            print(f"- {token} = {value}")
        else:
            print(f"- {token} = <MISSING>")
            missing.append(token)
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install template files from pmenglund/agents into a repository.",
    )
    parser.add_argument(
        "--target",
        default=".",
        help="Target repository directory (default: current directory).",
    )
    parser.add_argument(
        "--language",
        choices=sorted(LANGUAGE_SOURCES.keys()),
        default="go",
        help="Language template selection (default: go).",
    )
    parser.add_argument(
        "--workflow",
        choices=sorted(WORKFLOW_SOURCES.keys()),
        default="linear",
        help="Workflow template selection (default: linear).",
    )
    parser.add_argument("--owner", default="pmenglund", help="GitHub owner (default: pmenglund).")
    parser.add_argument("--repo", default="agents", help="GitHub repo name (default: agents).")
    parser.add_argument("--ref", default="master", help="Git ref/branch/tag (default: master).")
    parser.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Replace template token {{KEY}} with VALUE. Repeatable.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite destination files if they already exist.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without writing files.",
    )
    parser.add_argument(
        "--infer-only",
        action="store_true",
        help="Infer AGENTS.md placeholder values and print them without writing files.",
    )
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if not target.exists() or not target.is_dir():
        print(f"ERROR: target directory does not exist: {target}", file=sys.stderr)
        return 1

    try:
        explicit_replacements = parse_key_value(args.set)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    try:
        agents_template = fetch_text(args.owner, args.repo, args.ref, "_AGENTS.md")
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    agents_tokens = unresolved_tokens(agents_template)
    inferred = infer_replacements(target, args.language, args.workflow)
    replacements = dict(inferred)
    replacements.update(explicit_replacements)

    missing_agents_tokens = print_placeholder_plan(agents_tokens, replacements)
    if args.infer_only:
        if missing_agents_tokens:
            print("\nMissing AGENTS.md placeholders:")
            for token in missing_agents_tokens:
                print(f"- {token}")
        return 0

    if missing_agents_tokens:
        print(
            "\nERROR: missing required AGENTS.md placeholder values. "
            "Provide them with --set KEY=VALUE.",
            file=sys.stderr,
        )
        return 1

    sources = collect_sources(args.language, args.workflow)
    existing = [dest for _, dest in sources if (target / dest).exists()]
    if existing and not args.force:
        print("ERROR: destination file(s) already exist. Use --force to overwrite:", file=sys.stderr)
        for dest in existing:
            print(f"  - {target / dest}", file=sys.stderr)
        return 1

    rendered_files: list[tuple[Path, str]] = []
    unresolved_by_file: dict[str, list[str]] = {}

    for source_path, dest_name in sources:
        if source_path == "_AGENTS.md":
            contents = agents_template
        else:
            try:
                contents = fetch_text(args.owner, args.repo, args.ref, source_path)
            except RuntimeError as exc:
                print(f"ERROR: {exc}", file=sys.stderr)
                return 1

        for token, value in replacements.items():
            contents = contents.replace(f"{{{{{token}}}}}", value)

        unresolved = unresolved_tokens(contents)
        if dest_name == "AGENTS.md" and unresolved:
            print(
                "ERROR: AGENTS.md still has unresolved placeholders after replacement: "
                + ", ".join(f"{{{{{token}}}}}" for token in unresolved),
                file=sys.stderr,
            )
            return 1
        if unresolved and dest_name != "AGENTS.md":
            unresolved_by_file[dest_name] = unresolved

        rendered_files.append((target / dest_name, contents))

    plans_dir = target / "plans"

    if args.dry_run:
        print(f"[DRY RUN] Target: {target}")
        for path, _ in rendered_files:
            action = "overwrite" if path.exists() else "create"
            print(f"[DRY RUN] Would {action}: {path}")
        print(f"[DRY RUN] Would ensure directory exists: {plans_dir}")
    else:
        plans_dir.mkdir(parents=True, exist_ok=True)
        for path, contents in rendered_files:
            path.write_text(contents, encoding="utf-8")
            print(f"[OK] Wrote: {path}")
        print(f"[OK] Ensured directory exists: {plans_dir}")

    if unresolved_by_file:
        print("\nUnresolved placeholders in non-AGENTS files:")
        for file_name in sorted(unresolved_by_file):
            tokens = ", ".join(f"{{{{{token}}}}}" for token in unresolved_by_file[file_name])
            print(f"- {file_name}: {tokens}")
    else:
        print("\nAll detected placeholders were filled in all written files.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
