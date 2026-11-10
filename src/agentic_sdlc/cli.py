"""Command-line interface for Agentic SDLC (`asdlc` / `agentic-sdlc`)."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

from agentic_sdlc import __version__

VALID_MODES = ("sdd", "add", "full")
VALID_AGENTS = ("universal", "claude", "cursor", "copilot", "windsurf", "all")
VALID_TASK_STATUSES = {"pending", "in_progress", "completed", "blocked"}

COMMON_TEMPLATES: tuple[tuple[str, str], ...] = (
    ("common/CONSTITUTION.md", "docs/sdlc/CONSTITUTION.md"),
    ("common/TASKS.md", "docs/sdlc/TASKS.md"),
    ("common/TASK_PROGRESS.json", "docs/sdlc/TASK_PROGRESS.json"),
    ("common/adr/ADR-0001-architecture.md", "docs/sdlc/adr/ADR-0001-architecture.md"),
)

SDD_TEMPLATES: tuple[tuple[str, str], ...] = (
    ("sdd/SPEC.md", "docs/sdlc/SPEC.md"),
    ("sdd/PLAN.md", "docs/sdlc/PLAN.md"),
)

ADD_TEMPLATES: tuple[tuple[str, str], ...] = (
    ("add/AGENT_SPEC.md", "docs/sdlc/AGENT_SPEC.md"),
    ("add/TOOLS_AND_MCP.md", "docs/sdlc/TOOLS_AND_MCP.md"),
    ("add/EVAL_AND_SAFETY.md", "docs/sdlc/EVAL_AND_SAFETY.md"),
)


def _safe_within(base: Path, relative_or_target: Path | str) -> Path:
    """Resolve a target path and guarantee it stays strictly inside ``base``."""
    base_resolved = base.resolve()
    rel_path = Path(relative_or_target)
    if rel_path.is_absolute():
        candidate = rel_path.resolve()
    else:
        candidate = (base_resolved / rel_path).resolve()

    if not candidate.is_relative_to(base_resolved):
        raise ValueError(
            f"Refusing path outside project root '{base_resolved}': '{relative_or_target}'"
        )

    # Guard against pre-existing intermediate symlinks inside base pointing elsewhere
    current = base_resolved
    for part in candidate.relative_to(base_resolved).parts:
        current = current / part
        if current.is_symlink():
            resolved_hop = current.resolve()
            if not resolved_hop.is_relative_to(base_resolved):
                raise ValueError(
                    f"Refusing symlink traversal outside project root: '{current}'"
                )
    return candidate


def _resolve_bundle_root() -> Path:
    """Locate bundled skills, agents, and templates for wheel or editable installs."""
    pkg_dir = Path(__file__).resolve().parent
    bundled = pkg_dir / "_bundle"
    if (bundled / "skills").is_dir() and (bundled / "templates").is_dir():
        return bundled

    repo_root = pkg_dir.parent.parent
    if (repo_root / "skills").is_dir() and (repo_root / "templates").is_dir():
        return repo_root

    raise FileNotFoundError(
        "Unable to locate Agentic SDLC bundle assets (skills, agents, templates)."
    )


def _parse_frontmatter(markdown_text: str) -> tuple[dict[str, str], str]:
    """Parse minimal YAML frontmatter (key: value) without external dependencies."""
    lines = markdown_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, markdown_text

    meta: dict[str, str] = {}
    end_idx = None
    for idx in range(1, len(lines)):
        stripped = lines[idx].strip()
        if stripped == "---":
            end_idx = idx
            break
        if ":" in stripped:
            key, raw_val = stripped.split(":", 1)
            meta[key.strip()] = raw_val.strip().strip('"').strip("'")

    if end_idx is None:
        return {}, markdown_text

    body = "\n".join(lines[end_idx + 1 :]).lstrip("\n")
    return meta, body


def _discover_skills(bundle_root: Path) -> list[dict[str, str]]:
    """Return sorted metadata + content for all bundled skills."""
    skills_dir = bundle_root / "skills"
    results: list[dict[str, str]] = []
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            continue
        raw = skill_file.read_text(encoding="utf-8")
        meta, body = _parse_frontmatter(raw)
        results.append(
            {
                "name": meta.get("name", skill_dir.name),
                "description": meta.get("description", ""),
                "raw": raw,
                "body": body,
            }
        )
    return results


def _discover_agents(bundle_root: Path) -> list[dict[str, str]]:
    """Return sorted metadata + content for all bundled reviewer/coordinator personas."""
    agents_dir = bundle_root / "agents"
    results: list[dict[str, str]] = []
    for agent_file in sorted(agents_dir.glob("*.md")):
        if agent_file.name.endswith(".metadata.json"):
            continue
        raw = agent_file.read_text(encoding="utf-8")
        meta, body = _parse_frontmatter(raw)
        results.append(
            {
                "name": meta.get("name", agent_file.stem),
                "description": meta.get("description", ""),
                "raw": raw,
                "body": body,
            }
        )
    return results


def _render_template(text: str, variables: dict[str, str]) -> str:
    rendered = text
    for key, val in variables.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", val)
    return rendered


def _write_file(
    project_root: Path,
    rel_dest: str,
    content: str,
    *,
    force: bool,
    created: list[str],
    skipped: list[str],
) -> None:
    dest = _safe_within(project_root, rel_dest)
    if dest.exists() and not force:
        skipped.append(rel_dest)
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    created.append(rel_dest)


def _build_agents_markdown(
    *,
    project_name: str,
    mode: str,
    stack: str,
    llm_provider: str,
    skills: list[dict[str, str]],
    agents: list[dict[str, str]],
) -> str:
    mode_label = {
        "sdd": "Spec-Driven Development (SDD — Deterministic Software)",
        "add": "Agent-Driven Development (ADD — Deterministic AI Agents)",
        "full": "Unified SDD + ADD (Full-Stack Software + AI Agents)",
    }[mode]

    skill_rows = "\n".join(
        f"| `{s['name']}` | {s['description']} |" for s in skills
    )
    agent_rows = "\n".join(
        f"| `{a['name']}` | {a['description']} |" for a in agents
    )

    return f"""# Agentic SDLC Instructions — {project_name}

This repository follows **Agentic SDLC** in **`{mode}`** mode ({mode_label}).
All architectural specifications, agent contracts, and task execution states live in `docs/sdlc/`.

- **Primary Stack**: {stack}
- **Model / LLM Strategy**: {llm_provider}

## Non-Negotiable Engineering Rules

1. **Specs Before Code**: Read `docs/sdlc/CONSTITUTION.md` before making changes. Keep `docs/sdlc/` specifications synchronized with code—never introduce undocumented APIs, state keys, or LLM tools.
2. **Incremental TDD Execution**: Work one task at a time from `docs/sdlc/TASK_PROGRESS.json` and `docs/sdlc/TASKS.md`. Write/update automated tests first, verify they pass, then mark the task `"completed"`.
3. **Zero Hardcoded Secrets & Safe Defaults**: Load credentials, model IDs, and endpoints from environment variables. Bind local development servers to `127.0.0.1` by default and enforce explicit timeouts and path/input validation.
4. **Bounded AI Loops (ADD)**: Every AI agent or tool loop must enforce `max_iterations`, typed tool schemas, timeouts, and structured error payloads as specified in `docs/sdlc/AGENT_SPEC.md` and `docs/sdlc/TOOLS_AND_MCP.md`.
5. **Context-Isolated Review**: Do not self-certify specifications or security in the authoring context. Use isolated fresh-context reviewers (`spec-critic`, `security-redteam`, `eval-verifier`).

## Available Skills

| Skill | Purpose |
| :--- | :--- |
{skill_rows}

## Context-Isolated Personas

| Persona | Role |
| :--- | :--- |
{agent_rows}

## CLI Quick Check

- Check progress: `asdlc status`
- Validate `docs/sdlc/` contracts & task graph: `asdlc validate`
"""


def cmd_init(args: argparse.Namespace) -> int:
    target_root = Path(args.path).resolve()
    target_root.mkdir(parents=True, exist_ok=True)

    mode: str = args.mode
    agent_target: str = args.agent
    force: bool = args.force
    project_name: str = args.project_name or target_root.name
    today = dt.date.today().isoformat()

    variables = {
        "PROJECT_NAME": project_name,
        "MODE": mode,
        "STACK": args.stack,
        "LLM_PROVIDER": args.llm,
        "DATE": today,
    }

    bundle_root = _resolve_bundle_root()
    skills = _discover_skills(bundle_root)
    agents = _discover_agents(bundle_root)

    created: list[str] = []
    skipped: list[str] = []

    # 1. Scaffold docs/sdlc/ living state templates
    selected_templates = list(COMMON_TEMPLATES)
    if mode in ("sdd", "full"):
        selected_templates.extend(SDD_TEMPLATES)
    if mode in ("add", "full"):
        selected_templates.extend(ADD_TEMPLATES)

    for src_rel, dest_rel in selected_templates:
        raw_tpl = (bundle_root / "templates" / src_rel).read_text(encoding="utf-8")
        rendered = _render_template(raw_tpl, variables)
        _write_file(
            target_root,
            dest_rel,
            rendered,
            force=force,
            created=created,
            skipped=skipped,
        )

    instructions_md = _build_agents_markdown(
        project_name=project_name,
        mode=mode,
        stack=args.stack,
        llm_provider=args.llm,
        skills=skills,
        agents=agents,
    )

    install_universal = agent_target in ("universal", "cursor", "windsurf", "all")
    install_claude = agent_target in ("claude", "all")
    install_cursor = agent_target in ("cursor", "all")
    install_copilot = agent_target in ("copilot", "all")
    install_windsurf = agent_target in ("windsurf", "all")

    # 2. Universal Open Agent Skills (.agents/skills + .agents/agents + AGENTS.md)
    if install_universal:
        _write_file(
            target_root,
            "AGENTS.md",
            instructions_md,
            force=force,
            created=created,
            skipped=skipped,
        )
        for skill in skills:
            _write_file(
                target_root,
                f".agents/skills/{skill['name']}/SKILL.md",
                skill["raw"],
                force=force,
                created=created,
                skipped=skipped,
            )
        for persona in agents:
            _write_file(
                target_root,
                f".agents/agents/{persona['name']}.md",
                persona["raw"],
                force=force,
                created=created,
                skipped=skipped,
            )

    # 3. Claude Code adapter (CLAUDE.md + .claude/commands + .claude/agents)
    if install_claude:
        _write_file(
            target_root,
            "CLAUDE.md",
            instructions_md,
            force=force,
            created=created,
            skipped=skipped,
        )
        for skill in skills:
            cmd_doc = (
                f"---\ndescription: \"{skill['description']}\"\n---\n\n{skill['body']}"
            )
            _write_file(
                target_root,
                f".claude/commands/{skill['name']}.md",
                cmd_doc,
                force=force,
                created=created,
                skipped=skipped,
            )
        for persona in agents:
            _write_file(
                target_root,
                f".claude/agents/{persona['name']}.md",
                persona["raw"],
                force=force,
                created=created,
                skipped=skipped,
            )

    # 4. Cursor adapter (.cursor/rules/agentic-sdlc.mdc)
    if install_cursor:
        cursor_rule = (
            "---\n"
            "description: Agentic SDLC (SDD + ADD) living specification and TDD guardrails\n"
            "alwaysApply: true\n"
            "---\n\n"
            f"{instructions_md}"
        )
        _write_file(
            target_root,
            ".cursor/rules/agentic-sdlc.mdc",
            cursor_rule,
            force=force,
            created=created,
            skipped=skipped,
        )

    # 5. GitHub Copilot adapter (.github/copilot-instructions.md + .github/prompts/*.prompt.md)
    if install_copilot:
        _write_file(
            target_root,
            ".github/copilot-instructions.md",
            instructions_md,
            force=force,
            created=created,
            skipped=skipped,
        )
        for skill in skills:
            prompt_doc = (
                "---\n"
                "mode: 'agent'\n"
                f"description: \"{skill['description']}\"\n"
                "---\n\n"
                f"{skill['body']}"
            )
            _write_file(
                target_root,
                f".github/prompts/{skill['name']}.prompt.md",
                prompt_doc,
                force=force,
                created=created,
                skipped=skipped,
            )

    # 6. Windsurf adapter (.windsurfrules)
    if install_windsurf:
        _write_file(
            target_root,
            ".windsurfrules",
            instructions_md,
            force=force,
            created=created,
            skipped=skipped,
        )

    print(
        f"Initialized Agentic SDLC in '{target_root}' "
        f"(mode={mode}, agent={agent_target})."
    )
    print(f"  Created/updated files: {len(created)}")
    if skipped:
        print(
            f"  Preserved existing files: {len(skipped)} (pass --force to overwrite)"
        )
    return 0


def _required_docs_for_mode(mode: str) -> list[str]:
    docs = [
        "docs/sdlc/CONSTITUTION.md",
        "docs/sdlc/TASKS.md",
        "docs/sdlc/TASK_PROGRESS.json",
    ]
    if mode in ("sdd", "full"):
        docs.extend(["docs/sdlc/SPEC.md", "docs/sdlc/PLAN.md"])
    if mode in ("add", "full"):
        docs.extend(
            [
                "docs/sdlc/AGENT_SPEC.md",
                "docs/sdlc/TOOLS_AND_MCP.md",
                "docs/sdlc/EVAL_AND_SAFETY.md",
            ]
        )
    return docs


def _detect_cycle(tasks: list[dict[str, Any]]) -> str | None:
    graph: dict[str, list[str]] = {
        str(t["id"]): [str(dep) for dep in t.get("depends_on", [])] for t in tasks
    }
    state: dict[str, int] = {}  # 0=unvisited, 1=visiting, 2=visited

    def dfs(node: str) -> str | None:
        state[node] = 1
        for dep in graph.get(node, []):
            dep_state = state.get(dep, 0)
            if dep_state == 1:
                return f"{node} -> {dep}"
            if dep_state == 0 and dep in graph:
                found = dfs(dep)
                if found:
                    return found
        state[node] = 2
        return None

    for task_id in graph:
        if state.get(task_id, 0) == 0:
            cycle = dfs(task_id)
            if cycle:
                return cycle
    return None


def cmd_status(args: argparse.Namespace) -> int:
    target_root = Path(args.path).resolve()
    progress_path = _safe_within(target_root, "docs/sdlc/TASK_PROGRESS.json")
    if not progress_path.is_file():
        print(
            f"No docs/sdlc/TASK_PROGRESS.json found in '{target_root}'. "
            "Run `asdlc init` first.",
            file=sys.stderr,
        )
        return 1

    try:
        data = json.loads(progress_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {progress_path}: {exc}", file=sys.stderr)
        return 1

    mode = str(data.get("mode", "full"))
    project = str(data.get("project", target_root.name))
    tasks: list[dict[str, Any]] = list(data.get("tasks", []))

    counts = {status: 0 for status in sorted(VALID_TASK_STATUSES)}
    for task in tasks:
        st = str(task.get("status", "pending"))
        counts[st] = counts.get(st, 0) + 1

    total = len(tasks)
    completed = counts.get("completed", 0)
    pct = round((completed / total) * 100, 1) if total else 0.0

    required_docs = _required_docs_for_mode(mode)
    doc_states = {
        rel: _safe_within(target_root, rel).is_file() for rel in required_docs
    }

    summary = {
        "project": project,
        "mode": mode,
        "total_tasks": total,
        "completed": completed,
        "in_progress": counts.get("in_progress", 0),
        "pending": counts.get("pending", 0),
        "blocked": counts.get("blocked", 0),
        "completion_pct": pct,
        "documents": doc_states,
    }

    if args.json:
        print(json.dumps(summary, indent=2))
        return 0

    print(f"Project: {project} (mode: {mode})")
    print(
        f"Tasks  : {completed}/{total} completed ({pct}%) | "
        f"in_progress={summary['in_progress']} | "
        f"pending={summary['pending']} | "
        f"blocked={summary['blocked']}"
    )
    print("Living Contracts:")
    for rel, exists in doc_states.items():
        marker = "[OK]" if exists else "[MISSING]"
        print(f"  {marker} {rel}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    target_root = Path(args.path).resolve()
    errors: list[str] = []

    progress_path = _safe_within(target_root, "docs/sdlc/TASK_PROGRESS.json")
    mode = "full"
    data: dict[str, Any] | None = None

    if not progress_path.is_file():
        errors.append("Missing required file: docs/sdlc/TASK_PROGRESS.json")
    else:
        try:
            loaded = json.loads(progress_path.read_text(encoding="utf-8"))
            if not isinstance(loaded, dict):
                errors.append("docs/sdlc/TASK_PROGRESS.json root must be a JSON object.")
            else:
                data = loaded
                raw_mode = str(loaded.get("mode", "full"))
                if raw_mode not in VALID_MODES:
                    errors.append(
                        f"Invalid mode '{raw_mode}' in TASK_PROGRESS.json; "
                        f"expected one of {VALID_MODES}."
                    )
                else:
                    mode = raw_mode
        except json.JSONDecodeError as exc:
            errors.append(f"Malformed JSON in docs/sdlc/TASK_PROGRESS.json: {exc}")

    for rel in _required_docs_for_mode(mode):
        doc_path = _safe_within(target_root, rel)
        if not doc_path.is_file():
            if rel != "docs/sdlc/TASK_PROGRESS.json":
                errors.append(f"Missing required specification for mode '{mode}': {rel}")
        elif doc_path.stat().st_size == 0:
            errors.append(f"Specification file is empty: {rel}")

    if data is not None:
        tasks = data.get("tasks")
        if not isinstance(tasks, list):
            errors.append("TASK_PROGRESS.json field 'tasks' must be a list.")
        else:
            seen_ids: set[str] = set()
            valid_task_dicts: list[dict[str, Any]] = []
            for idx, item in enumerate(tasks):
                if not isinstance(item, dict):
                    errors.append(f"Task at index {idx} must be an object.")
                    continue
                task_id = str(item.get("id", "")).strip()
                if not task_id:
                    errors.append(f"Task at index {idx} is missing non-empty 'id'.")
                    continue
                if task_id in seen_ids:
                    errors.append(f"Duplicate task id '{task_id}' in TASK_PROGRESS.json.")
                seen_ids.add(task_id)

                status = str(item.get("status", ""))
                if status not in VALID_TASK_STATUSES:
                    errors.append(
                        f"Task '{task_id}' has invalid status '{status}'; "
                        f"expected one of {sorted(VALID_TASK_STATUSES)}."
                    )
                deps = item.get("depends_on", [])
                if not isinstance(deps, list):
                    errors.append(f"Task '{task_id}' field 'depends_on' must be a list.")
                else:
                    valid_task_dicts.append(item)

            for item in valid_task_dicts:
                task_id = str(item["id"])
                for dep in item.get("depends_on", []):
                    if str(dep) not in seen_ids:
                        errors.append(
                            f"Task '{task_id}' depends on unknown task '{dep}'."
                        )

            cycle = _detect_cycle(valid_task_dicts)
            if cycle:
                errors.append(f"Dependency cycle detected in TASK_PROGRESS.json: {cycle}")

    if errors:
        print("Validation FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"Validation PASSED for '{target_root}' (mode={mode}).")
    return 0


def cmd_list_skills(_args: argparse.Namespace) -> int:
    bundle_root = _resolve_bundle_root()
    skills = _discover_skills(bundle_root)
    agents = _discover_agents(bundle_root)

    print(f"Bundled Skills ({len(skills)}):")
    for skill in skills:
        print(f"  - {skill['name']:<18} {skill['description']}")

    print(f"\nContext-Isolated Personas ({len(agents)}):")
    for persona in agents:
        print(f"  - {persona['name']:<18} {persona['description']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="asdlc",
        description=(
            "Agentic SDLC: Unified Spec-Driven Development (SDD) & "
            "Agent-Driven Development (ADD) across any LLM, cloud, and coding agent."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_p = subparsers.add_parser(
        "init",
        help="Scaffold docs/sdlc/ living specs and coding-agent skills/adapters.",
    )
    init_p.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Target project directory (default: current directory).",
    )
    init_p.add_argument(
        "--mode",
        choices=VALID_MODES,
        default="full",
        help="Workflow track: 'sdd' (software), 'add' (AI agents), or 'full' (both).",
    )
    init_p.add_argument(
        "--agent",
        choices=VALID_AGENTS,
        default="universal",
        help="Coding agent adapter to install (default: universal AGENTS.md + .agents/).",
    )
    init_p.add_argument(
        "--llm",
        default="Model-agnostic (Gemini / Claude / OpenAI / Kimi / DeepSeek / Local)",
        help="Primary LLM/model provider note for CONSTITUTION.md and AGENT_SPEC.md.",
    )
    init_p.add_argument(
        "--stack",
        default="Language & cloud agnostic",
        help="Primary language/cloud stack note for CONSTITUTION.md and PLAN.md.",
    )
    init_p.add_argument(
        "--project-name",
        default=None,
        help="Override project display name (defaults to directory name).",
    )
    init_p.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files instead of preserving them.",
    )
    init_p.set_defaults(func=cmd_init)

    status_p = subparsers.add_parser(
        "status",
        help="Show task completion progress and living contract status.",
    )
    status_p.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Target project directory (default: current directory).",
    )
    status_p.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON output.",
    )
    status_p.set_defaults(func=cmd_status)

    val_p = subparsers.add_parser(
        "validate",
        help="Validate docs/sdlc/ specifications and TASK_PROGRESS.json integrity.",
    )
    val_p.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Target project directory (default: current directory).",
    )
    val_p.set_defaults(func=cmd_validate)

    list_p = subparsers.add_parser(
        "list-skills",
        help="List all bundled SDD + ADD skills and reviewer personas.",
    )
    list_p.set_defaults(func=cmd_list_skills)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
