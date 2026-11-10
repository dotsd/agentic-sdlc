---
name: sdd-converge
description: Audit the implemented codebase and test suite against docs/sdlc/SPEC.md, PLAN.md, AGENT_SPEC.md, and TOOLS_AND_MCP.md, identify unbuilt or partially verified requirements, and append delta tasks to TASKS.md and TASK_PROGRESS.json until 100% converged.
---

# Skill: Spec-to-Code Convergence Audit (`sdd-converge`)

## Purpose
Close the "last 15%" gap where coding sessions mark tasks done while subtle acceptance scenarios, error paths, tool timeouts, or documentation remain incomplete.

## Prerequisites & Outputs
- **Reads**: All `docs/sdlc/*.md` files, `docs/sdlc/TASK_PROGRESS.json`, source files, and automated tests
- **Updates**: `docs/sdlc/TASKS.md`, `docs/sdlc/TASK_PROGRESS.json` (when gaps exist)

## Workflow

1. **Build Full Traceability Matrix**
   - Map every requirement/Gherkin scenario in `SPEC.md`, module/API in `PLAN.md`, and agent/tool/eval in `AGENT_SPEC.md` + `TOOLS_AND_MCP.md` + `EVAL_AND_SAFETY.md` against real implementation files and passing tests.

2. **Classify Every Item**
   - `CONVERGED`: Implemented cleanly + covered by automated tests + passes verification.
   - `PARTIAL`: Implemented on happy path, but missing validation, error contract, timeout, or edge-case test.
   - `MISSING`: Not yet implemented or stubbed/mocked (`TODO`, `NotImplementedError`, hardcoded placeholder).
   - `DRIFTED`: Code behavior diverges from the spec contract.

3. **Generate Convergence Tasks (If Not 100% `CONVERGED`)**
   - Append a `## Convergence Delta Tasks` section in `docs/sdlc/TASKS.md` and corresponding `pending` entries in `docs/sdlc/TASK_PROGRESS.json` so `sdd-implement` can finish them deterministically.
   - Report the exact convergence percentage (`converged / total`) to the user.
