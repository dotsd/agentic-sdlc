---
name: sdd-tasks
description: Decompose docs/sdlc/PLAN.md and/or docs/sdlc/AGENT_SPEC.md + TOOLS_AND_MCP.md into small, dependency-ordered TDD engineering tasks in docs/sdlc/TASKS.md and machine-readable state in docs/sdlc/TASK_PROGRESS.json.
---

# Skill: Dependency-Ordered Task Decomposition (`sdd-tasks`)

## Purpose
Convert approved software (`PLAN.md`) and/or AI agent (`AGENT_SPEC.md`, `TOOLS_AND_MCP.md`, `EVAL_AND_SAFETY.md`) designs into atomic, verifiable tasks with both human-readable checklists (`docs/sdlc/TASKS.md`) and machine-readable execution state (`docs/sdlc/TASK_PROGRESS.json`).

## Prerequisites & Outputs
- **Reads**: `docs/sdlc/CONSTITUTION.md`, plus `SPEC.md`/`PLAN.md` (SDD) and/or `AGENT_SPEC.md`/`TOOLS_AND_MCP.md`/`EVAL_AND_SAFETY.md` (ADD)
- **Writes**: `docs/sdlc/TASKS.md`, `docs/sdlc/TASK_PROGRESS.json`

## Workflow

1. **Structure Implementation Phases**
   - **Phase 1 — Setup & Scaffolding**: Project structure, dependency lockfile, configuration/`.env.example`, lint/test runner wiring.
   - **Phase 2 — Foundational Schemas & Contracts**: Shared domain types, database schemas, structured error models, session state models.
   - **Phase 3 — Deterministic Services / Tools & MCP (`[P]` parallelizable where file-disjoint)**: Core business logic, API endpoints, typed LLM tools, and MCP adapters—each paired with unit/contract tests.
   - **Phase 4 — Agent Orchestration / Application Wiring**: UI/API integration, agent prompts, subagent routing, loop bounds (`max_iterations`), guardrails.
   - **Phase 5 — End-to-End Verification, Trajectory Evals & Hardening**: Golden trajectory harness, adversarial prompt-injection/security tests, observability, deployment packaging.

2. **Format Every Task Atomically in `docs/sdlc/TASKS.md`**
   - Use sequential IDs (`T-001`, `T-002`, ...), optional `[P]` markers for tasks touching disjoint files that can run concurrently in parallel subagents, requirement/spec links (`[US-001]`, `[TOOL-01]`), target file paths, and an explicit verification command:
     ```markdown
     - [ ] **T-003** `[P]` `[US-001]` Implement order validation schema and unit tests in `src/models/order.py` and `tests/test_order.py` — Verify: `pytest tests/test_order.py`
     ```

3. **Synchronize `docs/sdlc/TASK_PROGRESS.json`**
   Maintain valid JSON with exact task metadata so any coding agent or CI check can resume deterministically across sessions:
   ```json
   {
     "schema_version": "1.0",
     "mode": "full",
     "updated_at": "2026-01-01T00:00:00Z",
     "tasks": [
       {
         "id": "T-001",
         "phase": 1,
         "title": "Initialize package configuration and test runner",
         "parallel": false,
         "depends_on": [],
         "spec_refs": ["CONSTITUTION"],
         "files": ["pyproject.toml", "tests/"],
         "verify_cmd": "pytest",
         "status": "pending"
       }
     ]
   }
   ```

4. **Verification Gate**
   - Validate `docs/sdlc/TASK_PROGRESS.json` parses as valid JSON, has zero circular `depends_on` references, and covers 100% of components/tools/evals in the design docs.
