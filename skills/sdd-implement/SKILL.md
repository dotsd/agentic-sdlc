---
name: sdd-implement
description: Execute pending engineering tasks from docs/sdlc/TASK_PROGRESS.json and docs/sdlc/TASKS.md incrementally using test-driven development (TDD), updating living state after every verified task.
---

# Skill: Incremental Test-Driven Implementation (`sdd-implement`)

## Purpose
Execute `docs/sdlc/TASKS.md` and `docs/sdlc/TASK_PROGRESS.json` deterministically without context drift, giant unreviewed diffs, or untested code—applicable to both software modules (SDD) and AI agent tools/orchestrators (ADD).

## Prerequisites & Outputs
- **Reads**: `docs/sdlc/CONSTITUTION.md`, `SPEC.md`/`PLAN.md`, `AGENT_SPEC.md`/`TOOLS_AND_MCP.md` (if present), `TASKS.md`, `TASK_PROGRESS.json`
- **Updates**: Source code, test suite, `docs/sdlc/TASKS.md`, `docs/sdlc/TASK_PROGRESS.json`

## Workflow

1. **Pre-Flight Check**
   - Load `docs/sdlc/TASK_PROGRESS.json` and identify the next eligible `pending` task whose `depends_on` tasks are all `completed`.
   - If tasks marked `"parallel": true` (`[P]`) touch completely disjoint files and subagents are available, they may be dispatched concurrently; otherwise execute sequentially.

2. **Red → Green → Refactor Loop (Per Task)**
   - **Mark `in_progress`**: Update the task's `status` in `TASK_PROGRESS.json`.
   - **Write Failing Tests First**: Create unit/contract tests covering the task's happy path, edge cases, input validation, and structured error handling.
   - **Implement Minimal Clean Code**:
     - Follow `CONSTITUTION.md` typing, security, and style rules.
     - For ADD tools: include type annotations, explicit routing docstrings, input bounds, timeouts, and structured recoverable error payloads.
     - For ADD agents: enforce configured model env vars, explicit state keys from `AGENT_SPEC.md`, and `max_iterations` termination bounds.
   - **Run Verification Command**: Execute the task's `verify_cmd` plus project-wide regression tests. Never mark a task complete while tests fail.

3. **Synchronize Living State**
   - Mark the task `[x]` in `docs/sdlc/TASKS.md` and `"status": "completed"` (with updated `updated_at` timestamp) in `docs/sdlc/TASK_PROGRESS.json`.
   - If implementation uncovers a necessary contract adjustment, update `PLAN.md` or `AGENT_SPEC.md`/`TOOLS_AND_MCP.md` immediately so specs never drift from code.

4. **Post-Implementation Gate**
   - Once all tasks reach `completed`, recommend running `add-critic` / `add-eval` (fresh-context review & verification) and `sdd-converge`.
