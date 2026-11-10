---
name: sdlc-sync
description: Onboard existing brownfield software or AI agent repositories by reverse-engineering docs/sdlc/ living specifications from code, or synchronize docs/sdlc/ artifacts when code and specs drift apart.
---

# Skill: Brownfield Onboarding & Drift Synchronization (`sdlc-sync`)

## Purpose
Most real-world engineering happens in existing repositories that lack up-to-date specs. `sdlc-sync` inspects an existing codebase (services, APIs, UIs, AI agents, prompts, tools, MCP servers, and tests) to populate accurate `docs/sdlc/` contracts and highlight architectural or test gaps—without breaking working code.

## Outputs
- Creates or updates `docs/sdlc/CONSTITUTION.md`, `SPEC.md`, `PLAN.md`, `AGENT_SPEC.md`, `TOOLS_AND_MCP.md`, `EVAL_AND_SAFETY.md`, `TASKS.md`, and `TASK_PROGRESS.json` according to detected project components.

## Workflow

1. **Inventory the Repository (Read-Only Discovery)**
   - **Stack & Build**: Inspect dependency manifests, CI workflows, linters, Dockerfiles, and IaC configs -> synthesize `CONSTITUTION.md`.
   - **Software Architecture (SDD)**: Map entrypoints, API routes, CLI commands, database models, and background workers -> synthesize `SPEC.md` and `PLAN.md`.
   - **AI Agent & Tooling Footprint (ADD, if present)**: Locate system prompts, agent graphs/loops, subagent definitions, tool functions, MCP client/server configs, and eval scripts -> synthesize `AGENT_SPEC.md`, `TOOLS_AND_MCP.md`, and `EVAL_AND_SAFETY.md`.

2. **Ground Every Statement in Real Code**
   - Cite actual module paths, classes, and functions—never invent aspirational architecture as if it already exists.
   - Distinguish clearly between **Implemented Behavior** and **Detected Gaps / Risks** (e.g., missing timeouts, unbounded agent loops, undocumented env vars, untested endpoints).

3. **Populate Remediation Backlog**
   - Record existing verified modules as `"completed"` baseline items or record detected gaps as prioritized `"pending"` tasks in `docs/sdlc/TASKS.md` and `docs/sdlc/TASK_PROGRESS.json` so the team can immediately adopt `sdd-implement` and `add-critic`.
