---
name: add-critic
description: Run a context-isolated Quality & Security Gate by delegating docs/sdlc/ specs, prompts, tools, and source code to fresh-context spec-critic and security-redteam subagents (or clean review sessions), then remediate all P0 and P1 defects.
---

# Skill: Context-Isolated Architecture & Security Gate (`add-critic`)

## Purpose
Eliminate **LLM self-grading bias**. When the same context window both authors a design/codebase and reviews it, subtle routing collisions, missing error contracts, prompt-injection vectors, and security flaws get rationalized away. `add-critic` enforces independent, fresh-context review.

## Reviewer Personas Used
- `agents/spec-critic.md` — Architecture, API/schema completeness, multi-agent routing disjointness, state hygiene, bounded loops.
- `agents/security-redteam.md` — OWASP Web/API Top 10 + OWASP Top 10 for LLM & Agentic Applications (prompt injection, excessive agency, SSRF, path traversal, secret exposure).

## Workflow

1. **Dispatch Isolated Reviews**
   - **If your coding agent supports subagents** (e.g., Claude Code Task/subagents, Codex/Antigravity subagents, Cursor background agents, Kimi subagents):
     - Spawn `spec-critic` and `security-redteam` **concurrently** in fresh contexts.
     - Pass **only** file paths (`docs/sdlc/*` and relevant `src/` paths)—do **not** paste your authoring rationale or chat history.
   - **If running in a single-session harness**:
     - Adopt the `spec-critic` checklist and `security-redteam` checklist sequentially from cold file reads of `docs/sdlc/` and `src/`, treating all existing artifacts as untrusted third-party submissions, or prompt the user to run a parallel fresh session.

2. **Synthesize & Triage Findings**
   - Consolidate findings by severity (`P0` Critical, `P1` Major, `P2` Minor).
   - **Hard Gate**: Any `P0` or `P1` defect sets gate status to `BLOCKED`.

3. **Remediate & Re-Verify**
   - Fix every `P0` and `P1` defect directly in `docs/sdlc/` specifications and/or source code + unit tests.
   - Re-run the isolated critic check on modified files until both Architecture and Security gates return `PASS`.
